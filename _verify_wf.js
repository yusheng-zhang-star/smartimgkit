const fs = require('fs');
const files = ['blog-image-pack', 'youtube-thumbnail-suite', 'real-estate-photo-pack', 'food-photography-bundle', 'podcast-cover-suite', 'email-signature-pack', 'freelancer-portfolio-pack', 'event-photography-bundle', 'print-ready-prep', 'app-store-screenshot-suite', 'course-tutorial-pack', 'resume-cv-photo'];
let ok = 0, fail = 0;
for (const f of files) {
  try {
    const content = fs.readFileSync('workflows/' + f + '.html', 'utf8');
    const scripts = content.match(/<script(?![^>]*src=)(?![^>]*type\s*=\s*["']application\/ld\+json)[^>]*>([\s\S]*?)<\/script>/g) || [];
    for (const s of scripts) {
      const code = s.replace(/<\/?script[^>]*>/g, '');
      if (code.trim().length > 50) new Function(code);
    }
    ok++;
    console.log('✅ ' + f);
  } catch(e) {
    console.log('❌ ' + f + ': ' + e.message);
    fail++;
  }
}
console.log('\nTotal: ✅ OK: ' + ok + ' / ❌ Fail: ' + fail);
