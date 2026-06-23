const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/.openclaw/workspace/smartimgkit-main/tools/background-remover.html','utf8');
// Extract all FAQ questions from original file
const regex = /<button class="faq-question">([^<]+)<\/button>/g;
let m; let i=0;
while ((m = regex.exec(c)) !== null) {
  i++;
  console.log('FAQ #'+i+': '+m[1]);
}
console.log('\nTotal FAQ items in EN page: '+i);
// Check if there's a "More" section
console.log('\nHas "More Frequently":', c.includes('More Frequently'));
