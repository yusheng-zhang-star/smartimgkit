const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/.openclaw/workspace/smartimgkit-main/tools/background-remover.html','utf8');
console.log('Has </main>:', c.includes('</main>'));
console.log('Has hreflang es:', c.includes('hreflang="es"'));
console.log('Has More FAQ:', c.includes('More Frequently'));
console.log('File length:', c.length);
// Show last 300 chars
console.log('---LAST 300---');
console.log(c.slice(-300));
