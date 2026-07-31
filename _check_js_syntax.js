// Node script to batch check all tool HTML files for JS syntax errors
const fs = require('fs');
const path = require('path');

const BASE = process.argv[2] || 'E:\\网站项目\\smartimgkit';
const EXCLUDE_DIRS = ['node_modules', 'i18n', 'src', '_backup', '_old', 'dist'];

function walkDir(dir, results = []) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        if (entry.name.startsWith('.') || EXCLUDE_DIRS.includes(entry.name)) continue;
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            walkDir(fullPath, results);
        } else if (entry.name.endsWith('.html') && fullPath.includes(path.sep + 'tools' + path.sep)) {
            results.push(fullPath);
        }
    }
    return results;
}

const files = walkDir(BASE);
console.log(`Checking ${files.length} tool HTML files...\n`);

let errors = [];
let ok = 0;

for (const fullPath of files) {
    try {
        const content = fs.readFileSync(fullPath, 'utf8');
        const scriptRegex = /<script(?![^>]*src=)(?![^>]*type\s*=\s*["'](?:application\/ld\+json|application\/json))[^>]*>([\s\S]*?)<\/script>/g;
        let match;
        let fileOk = true;
        
        while ((match = scriptRegex.exec(content)) !== null) {
            const code = match[1].trim();
            if (code.length < 100) continue;
            
            try {
                new Function(code);
            } catch (e) {
                const relPath = path.relative(BASE, fullPath).replace(/\\/g, '/');
                errors.push({ file: relPath, error: e.message });
                fileOk = false;
                break;
            }
        }
        
        if (fileOk) ok++;
    } catch (e) {
        // Skip unreadable files
    }
}

console.log(`✅ Syntax OK: ${ok}/${files.length}`);
console.log(`❌ Syntax errors: ${errors.length}`);

if (errors.length > 0) {
    console.log('\n=== ERRORS ===');
    for (const e of errors.slice(0, 30)) {
        console.log(`  ❌ ${e.file}`);
        console.log(`     ${e.error}`);
    }
    if (errors.length > 30) {
        console.log(`\n  ... and ${errors.length - 30} more`);
    }
}
