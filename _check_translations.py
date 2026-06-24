"""Check which fields need translation in each language's tools_data.json."""
import json
import re

def has_accented_chars(text):
    """Check if text contains non-English accented characters."""
    accented = set('áéíóúñüçãõêôàèìòùÁÉÍÓÚÑÜÇÃÕÊÔÀÈÌÒÙ')
    return any(c in text for c in accented)

for lang in ['es', 'pt', 'id']:
    with open(f'_tools_data_{lang}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    tools = data['tools']
    total_kw = total_howto = total_guide = total_related = 0
    print(f'\n=== {lang.upper()} === {len(tools)} tools ===')
    for t in tools:
        slug = t['slug']
        issues = []
        
        # keywords
        kw = t.get('keywords', '')
        if kw and not has_accented_chars(kw):
            issues.append('keywords')
            total_kw += 1
        
        # howto: check h4 and p for English
        howto = t.get('howto_html', '')
        if howto:
            h4s = re.findall(r'<h4>(.*?)</h4>', howto)
            ps = re.findall(r'<p>(.*?)</p>', howto)
            en_h4 = sum(1 for h in h4s if not has_accented_chars(h))
            en_p = sum(1 for p in ps if not has_accented_chars(p))
            if en_h4 > 0 or en_p > 0:
                issues.append(f'howto({en_h4}h4+{en_p}p EN)')
                total_howto += 1
        
        # guide
        guide = t.get('guide_html', '')
        if guide:
            h3s = re.findall(r'<h3>(.*?)</h3>', guide)
            ps = re.findall(r'<p>(.*?)</p>', guide)
            en_h3 = sum(1 for h in h3s if not has_accented_chars(h))
            en_p = sum(1 for p in ps if not has_accented_chars(p))
            if en_h3 > 0 or en_p > 0:
                issues.append(f'guide({en_h3}h3+{en_p}p EN)')
                total_guide += 1
        
        # related
        related = t.get('related_html', '')
        if related:
            en_title = 'You Might Also Like' in related
            strongs = re.findall(r'<strong>(.*?)</strong>', related)
            spans = re.findall(r'<span class="tool-desc">(.*?)</span>', related)
            en_strong = sum(1 for s in strongs if not has_accented_chars(s))
            en_span = sum(1 for s in spans if not has_accented_chars(s))
            if en_title or en_strong > 0 or en_span > 0:
                issues.append(f'related(title={"EN" if en_title else "OK"}+{en_strong}s+{en_span}d EN)')
                total_related += 1
        
        if issues:
            print(f'  [{slug}] {"; ".join(issues)}')
    
    print(f'  Summary: keywords={total_kw}, howto={total_howto}, guide={total_guide}, related={total_related}')
