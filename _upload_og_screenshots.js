// Batch upload OG screenshots to GitHub via Contents API
const https = require('https');
const fs = require('fs');
const path = require('path');

// Read PAT from file (gitignored) or env var
const PAT = process.env.GH_PAT || (() => { try { return require('fs').readFileSync('.gh_pat', 'utf8').trim(); } catch(e) { return null; } })();
if (!PAT) { console.error('Error: Set GH_PAT env var or create .gh_pat file'); process.exit(1); }
const OWNER = 'yusheng-zhang-star';
const REPO = 'smartimgkit';
const BRANCH = 'main';
const SCREENSHOTS_DIR = path.join(__dirname, 'screenshots');

const langs = ['fr', 'vi', 'ar'];

function apiRequest(method, apiPath, body) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      path: apiPath,
      method: method,
      headers: {
        'Authorization': `Bearer ${PAT}`,
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'smartimgkit-deploy'
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(data));
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data.substring(0, 200)}`));
        }
      });
    });
    
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function uploadFile(localPath, repoPath) {
  const content = fs.readFileSync(localPath);
  const base64 = content.toString('base64');
  
  const apiPath = `/repos/${OWNER}/${REPO}/contents/${repoPath}`;
  
  // Check if file exists
  let sha = null;
  try {
    const existing = await apiRequest('GET', apiPath);
    sha = existing.sha;
  } catch (e) {
    // File doesn't exist, will create
  }
  
  const body = {
    message: `Add ${repoPath}`,
    content: base64,
    branch: BRANCH
  };
  if (sha) body.sha = sha;
  
  await apiRequest('PUT', apiPath, body);
  return { path: repoPath, size: content.length };
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  // Get list of screenshots to upload
  const files = [];
  for (const lang of langs) {
    const prefix = `${lang}-`;
    const dirFiles = fs.readdirSync(SCREENSHOTS_DIR).filter(f => f.startsWith(prefix) && f.endsWith('.png'));
    for (const f of dirFiles) {
      files.push({ localPath: path.join(SCREENSHOTS_DIR, f), repoPath: `screenshots/${f}`, lang });
    }
  }
  
  console.log(`Total screenshots to upload: ${files.length}`);
  
  let ok = 0, fail = 0;
  for (let i = 0; i < files.length; i++) {
    const f = files[i];
    try {
      const result = await uploadFile(f.localPath, f.repoPath);
      ok++;
      if ((i + 1) % 10 === 0 || i === files.length - 1) {
        const pct = Math.round((i + 1) / files.length * 100);
        console.log(`  [${i + 1}/${files.length}] ${pct}% - OK: ${ok}, FAIL: ${fail}`);
      }
    } catch (e) {
      fail++;
      console.log(`  FAIL ${f.repoPath}: ${e.message}`);
    }
    // Rate limit: GitHub allows ~5000/hr, 500ms = 7200/hr is safe
    await delay(500);
  }
  
  console.log(`\nDONE: ${ok} uploaded, ${fail} failed`);
}

main().catch(console.error);
