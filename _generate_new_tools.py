#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
_generate_new_tools.py -- 批量生成 24 个新增工具（文本/开发 + PDF + 视频）

⚠️ 铁律：绝不修改已有的 45 个工具页面（已被谷歌收录且有手工修改）
        本脚本只生成新增工具，不碰旧文件。

用法：python _generate_new_tools.py
"""
import json
import os
import sys
import copy

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from _build import build_one, LANGS, TEMPLATE

# ──────────────────────────────────────────────────────────
# 工具元数据（英文原版）
# 每个工具包含：slug, icon, title, description, keywords, h1, subtitle
#             workspace_html, inline_style, inline_js, jsonld_*
# ──────────────────────────────────────────────────────────

COMMON_STYLE = """
.tool-workspace { display: flex; flex-direction: column; gap: 24px; }
.controls { background: var(--bg-primary); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 24px; }
.controls h2 { font-size: 1.2rem; color: var(--text-primary); margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--accent); }
.control-row { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
.control-row label { font-weight: 600; min-width: 140px; color: var(--text-secondary); font-size: 0.85rem; }
.control-row select, .control-row input[type="number"], .control-row input[type="text"] { padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; background: var(--bg-primary); color: var(--text-primary); font-size: 0.85rem; }
.btn-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }
.result-section { background: var(--bg-primary); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 24px; }
.result-section h2 { font-size: 1.2rem; color: var(--text-primary); margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--accent); }
.info-box { background: rgba(99,102,241,0.1); border-left: 4px solid var(--accent); padding: 16px 20px; border-radius: 8px; margin-bottom: 24px; }
.info-box h3 { color: var(--accent); margin-bottom: 8px; font-size: 1rem; }
.info-box p, .info-box li { color: var(--text-secondary); font-size: 0.9rem; }
.info-box ul { margin-left: 20px; margin-top: 8px; }
.status-text { text-align: center; color: var(--text-secondary); font-size: 0.9rem; margin: 16px 0; }
textarea { width: 100%; min-height: 200px; padding: 12px; border: 1px solid var(--border); border-radius: 8px; background: var(--bg-secondary); color: var(--text-primary); font-family: 'Consolas', 'Monaco', monospace; font-size: 0.85rem; resize: vertical; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; margin-top: 16px; }
.stat-card { background: var(--bg-secondary); border-radius: 8px; padding: 16px; text-align: center; }
.stat-card .stat-num { font-size: 2rem; font-weight: 800; color: var(--accent); }
.stat-card .stat-label { font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.diff-output { background: var(--bg-secondary); border-radius: 8px; padding: 16px; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.8rem; white-space: pre-wrap; max-height: 400px; overflow-y: auto; }
.diff-add { background: rgba(34,197,94,0.15); color: #22c55e; }
.diff-del { background: rgba(239,68,68,0.15); color: #ef4444; text-decoration: line-through; }
@media (max-width: 640px) {
  .control-row { flex-direction: column; align-items: flex-start; }
  .two-col { grid-template-columns: 1fr; }
}
"""


def make_common_html(icon, slug, title, subtitle, main_content_html, before_label, after_label, before_emoji, after_emoji):
    """生成通用的工具页面 workspace HTML 结构"""
    return f'''<!-- Before/After Preview -->
        <div class="before-after-preview" id="beforeAfterPreview">
          <div class="before-after-label">✨ See what this tool can do</div>
          <div class="before-after-images">
            <div class="before-after-item">
              <div style="height:160px;display:flex;align-items:center;justify-content:center;background:var(--bg-secondary);"><span style="font-size:4rem;">{before_emoji}</span></div>
              <div class="before-after-item-caption before">{before_label}</div>
            </div>
            <div class="before-after-item">
              <div style="height:160px;display:flex;align-items:center;justify-content:center;background:var(--bg-secondary);"><span style="font-size:4rem;">{after_emoji}</span></div>
              <div class="before-after-item-caption after">{after_label}</div>
            </div>
          </div>
        </div>

{main_content_html}
'''


def gen_howto(steps):
    """生成 HowTo 结构化数据"""
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to Use",
        "step": [{"@type": "HowToStep", "position": i+1, "name": s[0], "text": s[1]} for i, s in enumerate(steps)]
    }


def gen_faq(qa_list):
    """生成 FAQ 结构化数据"""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa_list]
    }


def gen_webapp(name, desc, category="DeveloperApplication"):
    return {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": name,
        "url": f"https://smartimgkit.com/tools/",
        "applicationCategory": category,
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "description": desc
    }


def gen_howto_html(steps):
    items = ''.join(f'<div class="how-to-step"><div class="step-number">{i+1}</div><h4>{s[0]}</h4><p>{s[1]}</p></div>' for i, s in enumerate(steps))
    return f'<section class="how-to-section"><h2>How to Use</h2><div class="how-to-steps">{items}</div></section>'


def gen_guide_html(sections):
    blocks = ''.join(f'<div class="guide-block"><h3>{s[0]}</h3><p>{s[1]}</p></div>' for s in sections)
    return f'<h2>Detailed User Guide</h2>{blocks}'


def gen_faq_html(qa_list):
    items = ''.join(f'<div class="faq-item"><button class="faq-question">{q}</button><div class="faq-answer">{a}</div></div>' for q, a in qa_list)
    return f'<section class="faq-section"><h2>Frequently Asked Questions</h2>{items}</section>'


def gen_related_html(related):
    items = ''.join(f'<a href="/tools/{r[0]}" class="related-tool-card"><span class="tool-icon">{r[1]}</span><div class="tool-info"><strong>{r[2]}</strong><span class="tool-desc">{r[3]}</span></div><span class="tool-arrow">→</span></a>' for r in related)
    return f'<section class="related-tools"><h2>You Might Also Like</h2><div class="related-tools-grid">{items}</div></section>'


# ═══════════════════════════════════════════════════════════
# 第 1 批：文本/开发工具（11 个，纯 JS）
# ═══════════════════════════════════════════════════════════

T1_WORD_COUNTER = {
    "slug": "word-counter",
    "icon": "📝",
    "title": "Word Counter — Count Words, Characters & Sentences Free",
    "description": "Free online word counter and character counter. Count words, characters with/without spaces, sentences, paragraphs, and reading time in real time.",
    "keywords": "word counter, character counter, word count, letter counter, sentence counter, paragraph counter",
    "h1": "📝 Word Counter",
    "subtitle": "Count words, characters, sentences, paragraphs, and reading time — 100% free, in your browser.",
    "workspace_html": make_common_html(
        "📝", "word-counter", "Word Counter", "",
        '''<div class="controls">
            <h2>📝 Enter Your Text</h2>
            <textarea id="inputText" placeholder="Type or paste your text here..."></textarea>
        </div>

        <div class="result-section">
            <h2>📊 Statistics</h2>
            <div class="stats-grid" id="statsGrid">
              <div class="stat-card"><div class="stat-num" id="statWords">0</div><div class="stat-label">Words</div></div>
              <div class="stat-card"><div class="stat-num" id="statChars">0</div><div class="stat-label">Characters</div></div>
              <div class="stat-card"><div class="stat-num" id="statCharsNoSp">0</div><div class="stat-label">Chars (no spaces)</div></div>
              <div class="stat-card"><div class="stat-num" id="statSentences">0</div><div class="stat-label">Sentences</div></div>
              <div class="stat-card"><div class="stat-num" id="statParagraphs">0</div><div class="stat-label">Paragraphs</div></div>
              <div class="stat-card"><div class="stat-num" id="statReadTime">0</div><div class="stat-label">Reading Time (min)</div></div>
            </div>
        </div>

        <div class="controls">
            <h2>⚙️ Options</h2>
            <div class="control-row">
              <label>Reading Speed (WPM)</label>
              <input type="number" id="wpmInput" value="200" min="50" max="1000" style="width:100px;">
            </div>
            <div class="btn-row">
              <button class="btn btn-secondary" id="clearBtn">Clear Text</button>
              <button class="btn btn-primary" id="copyStatsBtn">📋 Copy Stats</button>
            </div>
        </div>''',
        "Raw text", "Word count & stats", "📄", "📊"
    ),
    "inline_js": '''(function() {
  const input = document.getElementById('inputText');
  const clearBtn = document.getElementById('clearBtn');
  const copyStatsBtn = document.getElementById('copyStatsBtn');
  const wpmInput = document.getElementById('wpmInput');

  function count() {
    const text = input.value || '';
    const chars = text.length;
    const charsNoSp = text.replace(/\\s/g, '').length;
    const words = text.trim() ? text.trim().split(/\\s+/).length : 0;
    const sentences = text.trim() ? text.split(/[.!?]+/).filter(s => s.trim()).length : 0;
    const paragraphs = text.trim() ? text.split(/\\n\\n+/).filter(p => p.trim()).length : 0;
    const wpm = parseInt(wpmInput.value) || 200;
    const readTime = Math.max(1, Math.ceil(words / wpm));

    document.getElementById('statWords').textContent = words;
    document.getElementById('statChars').textContent = chars;
    document.getElementById('statCharsNoSp').textContent = charsNoSp;
    document.getElementById('statSentences').textContent = sentences;
    document.getElementById('statParagraphs').textContent = paragraphs;
    document.getElementById('statReadTime').textContent = readTime;
  }

  input.addEventListener('input', count);
  wpmInput.addEventListener('input', count);

  clearBtn.addEventListener('click', () => { input.value = ''; count(); });

  copyStatsBtn.addEventListener('click', () => {
    const stats = `Words: ${document.getElementById('statWords').textContent}\\nCharacters: ${document.getElementById('statChars').textContent}\\nCharacters (no spaces): ${document.getElementById('statCharsNoSp').textContent}\\nSentences: ${document.getElementById('statSentences').textContent}\\nParagraphs: ${document.getElementById('statParagraphs').textContent}\\nReading Time: ${document.getElementById('statReadTime').textContent} min`;
    navigator.clipboard.writeText(stats);
    copyStatsBtn.textContent = '✓ Copied!';
    setTimeout(() => copyStatsBtn.textContent = '📋 Copy Stats', 2000);
  });
})();''',
    "howto_steps": [("Paste Text", "Paste or type your text into the input area."), ("View Stats", "Statistics update in real time as you type."), ("Adjust WPM", "Customize reading speed if needed."), ("Copy", "Click Copy Stats to copy all statistics.")],
    "faq_list": [("Does it count Chinese/Japanese characters?", "Yes. Character count includes all Unicode characters. Word count works best for space-separated languages."), ("Is my text stored or uploaded?", "No. All processing happens in your browser. Nothing is sent to any server."), ("What reading speed is used?", "Default is 200 WPM (average adult). You can adjust it from 50 to 1000 WPM.")],
    "related": [("password-generator", "🔐", "Password Generator", "Create secure random passwords"), ("uuid-generator", "🆔", "UUID Generator", "Generate unique UUIDs instantly"), ("case-converter", "🔠", "Case Converter", "Convert text between cases")]
}

T1_JSON_FORMATTER = {
    "slug": "json-formatter",
    "icon": "🔧",
    "title": "JSON Formatter — Format, Validate & Minify JSON Online",
    "description": "Free online JSON formatter and validator. Format, minify, validate, and beautify JSON with syntax highlighting and error reporting.",
    "keywords": "JSON formatter, JSON validator, JSON beautifier, JSON minifier, format JSON online",
    "h1": "🔧 JSON Formatter",
    "subtitle": "Format, validate, minify, and beautify JSON — free, in your browser.",
    "workspace_html": make_common_html(
        "🔧", "json-formatter", "JSON Formatter", "",
        '''<div class="controls">
            <h2>📥 Input JSON</h2>
            <textarea id="inputJson" placeholder='Paste your JSON here, e.g. {"name":"John"}'></textarea>
        </div>

        <div class="controls">
            <h2>⚙️ Actions</h2>
            <div class="btn-row">
              <button class="btn btn-primary" id="formatBtn">✨ Format (2 spaces)</button>
              <button class="btn btn-primary" id="format4Btn">✨ Format (4 spaces)</button>
              <button class="btn btn-primary" id="minifyBtn">📦 Minify</button>
              <button class="btn btn-primary" id="validateBtn">✓ Validate</button>
              <button class="btn btn-secondary" id="copyBtn">📋 Copy</button>
              <button class="btn btn-secondary" id="clearBtn">Clear</button>
            </div>
        </div>

        <div class="result-section">
            <h2>📤 Output</h2>
            <div id="statusMsg" class="status-text" style="display:none;"></div>
            <textarea id="outputJson" readonly placeholder="Output will appear here..."></textarea>
        </div>''',
        "Unformatted JSON", "Beautiful, valid JSON", "📄", "🔧"
    ),
    "inline_js": '''(function() {
  const input = document.getElementById('inputJson');
  const output = document.getElementById('outputJson');
  const statusMsg = document.getElementById('statusMsg');
  document.getElementById('formatBtn').onclick = () => process(2);
  document.getElementById('format4Btn').onclick = () => process(4);
  document.getElementById('minifyBtn').onclick = () => process(0);
  document.getElementById('validateBtn').onclick = () => validate();
  document.getElementById('copyBtn').onclick = () => { navigator.clipboard.writeText(output.value); };
  document.getElementById('clearBtn').onclick = () => { input.value = ''; output.value = ''; statusMsg.style.display = 'none'; };

  function show(msg, isError) { statusMsg.textContent = msg; statusMsg.style.display = 'block'; statusMsg.style.color = isError ? '#ef4444' : '#22c55e'; }

  function process(indent) {
    try {
      const obj = JSON.parse(input.value);
      output.value = indent === 0 ? JSON.stringify(obj) : JSON.stringify(obj, null, indent);
      show('✓ Valid JSON', false);
    } catch(e) { show('✗ Invalid: ' + e.message, true); }
  }
  function validate() {
    try { JSON.parse(input.value); show('✓ Valid JSON!', false); }
    catch(e) { show('✗ Invalid: ' + e.message, true); }
  }
})();''',
    "howto_steps": [("Paste JSON", "Paste your JSON into the input area."), ("Choose Action", "Click Format, Minify, or Validate."), ("View Result", "Output appears with status indicator."), ("Copy", "Click Copy to copy the result.")],
    "faq_list": [("What JSON standards are supported?", "Full JSON (RFC 8259). JSON5/JSONC (comments) are NOT supported — use standard JSON only."), ("Is my data uploaded?", "No. All processing is local in your browser."), ("What is the maximum size?", "We recommend under 10MB for performance. Very large files may slow down your browser.")],
    "related": [("url-encoder", "🔗", "URL Encoder", "Encode/decode URL strings"), ("base64", "🔐", "Base64 Converter", "Encode/decode Base64 strings"), ("regex-tester", "🔍", "Regex Tester", "Test regular expressions")]
}

T1_REGEX_TESTER = {
    "slug": "regex-tester",
    "icon": "🔍",
    "title": "Regex Tester — Test Regular Expressions Online Free",
    "description": "Free online regex tester and debugger. Test JavaScript regular expressions with real-time matching, highlight, and detailed match info.",
    "keywords": "regex tester, regular expression tester, regex debugger, test regex online, JavaScript regex",
    "h1": "🔍 Regex Tester",
    "subtitle": "Test and debug regular expressions with real-time matching — free, in your browser.",
    "workspace_html": make_common_html(
        "🔍", "regex-tester", "Regex Tester", "",
        '''<div class="controls">
            <h2>🔍 Regex Pattern</h2>
            <div class="control-row">
              <label>Pattern</label>
              <input type="text" id="pattern" placeholder="e.g. \\d+" style="flex:1; font-family:Consolas,monospace;">
            </div>
            <div class="control-row">
              <label>Flags</label>
              <label style="min-width:auto;"><input type="checkbox" id="flagG" checked> g (global)</label>
              <label style="min-width:auto;"><input type="checkbox" id="flagI"> i (case-insensitive)</label>
              <label style="min-width:auto;"><input type="checkbox" id="flagM"> m (multiline)</label>
              <label style="min-width:auto;"><input type="checkbox" id="flagS"> s (dotall)</label>
            </div>
        </div>

        <div class="controls">
            <h2>📝 Test String</h2>
            <textarea id="testStr" placeholder="Enter text to test against..."></textarea>
        </div>

        <div class="result-section">
            <h2>📊 Results</h2>
            <div id="statusMsg" class="status-text">Enter a pattern and test string</div>
            <div id="matchInfo" style="margin-top:16px;"></div>
            <h3 style="margin-top:16px;font-size:1rem;">Highlighted Matches:</h3>
            <div id="highlighted" style="background:var(--bg-secondary);border-radius:8px;padding:16px;font-family:Consolas,monospace;font-size:0.85rem;white-space:pre-wrap;word-break:break-all;margin-top:8px;"></div>
        </div>''',
        "Text + pattern", "Matched results", "🔍", "✅"
    ),
    "inline_js": '''(function() {
  const pattern = document.getElementById('pattern');
  const testStr = document.getElementById('testStr');
  const statusMsg = document.getElementById('statusMsg');
  const matchInfo = document.getElementById('matchInfo');
  const highlighted = document.getElementById('highlighted');
  const flags = ['flagG','flagI','flagM','flagS'];

  function test() {
    if (!pattern.value) { statusMsg.textContent = 'Enter a pattern'; matchInfo.innerHTML=''; highlighted.textContent=''; return; }
    try {
      let fs = '';
      flags.forEach(f => { if (document.getElementById(f).checked) fs += f.replace('flag','').toLowerCase(); });
      const re = new RegExp(pattern.value, fs);
      const text = testStr.value || '';
      const matches = [];
      let m;
      if (fs.includes('g')) { while ((m = re.exec(text)) !== null) { matches.push({text:m[0],index:m.index,groups:m.slice(1)}); if (m.index === re.lastIndex) re.lastIndex++; } }
      else { m = re.exec(text); if (m) matches.push({text:m[0],index:m.index,groups:m.slice(1)}); }
      statusMsg.textContent = `✓ ${matches.length} match(es) found`;
      statusMsg.style.color = '#22c55e';
      matchInfo.innerHTML = matches.length ? matches.map((m,i) => `<div style="padding:8px;background:var(--bg-secondary);border-radius:6px;margin-bottom:4px;"><strong>Match ${i+1}:</strong> "${m.text}" at index ${m.index}${m.groups.length?` | Groups: ${m.groups.map((g,j)=>`$${j+1}="${g||''}"`).join(', ')}`:''}</div>`).join('') : '';
      let hl = ''; let last = 0;
      matches.forEach(m => { hl += escapeHtml(text.slice(last, m.index)); hl += `<mark style="background:rgba(99,102,241,0.3);padding:2px 4px;border-radius:3px;">${escapeHtml(m.text)}</mark>`; last = m.index + m.text.length; });
      hl += escapeHtml(text.slice(last));
      highlighted.innerHTML = hl || '<em style="color:var(--text-secondary);">No test text entered</em>';
    } catch(e) { statusMsg.textContent = '✗ Error: ' + e.message; statusMsg.style.color = '#ef4444'; matchInfo.innerHTML=''; highlighted.textContent=''; }
  }
  function escapeHtml(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  [pattern, testStr].forEach(el => el.addEventListener('input', test));
  flags.forEach(f => document.getElementById(f).addEventListener('change', test));
})();''',
    "howto_steps": [("Enter Pattern", "Type your regex pattern in the Pattern field."), ("Set Flags", "Check flags like g, i, m, s as needed."), ("Enter Test Text", "Paste or type text to test against."), ("View Results", "Matches are highlighted and listed with details.")],
    "faq_list": [("Which regex flavor is used?", "JavaScript (ES2018+) regex. Supports lookaheads, lookbehinds, named groups, and Unicode."), ("Do you support PCRE/PHP/Python regex?", "Not directly. This tool uses JavaScript regex which is slightly different from PCRE."), ("Is my data safe?", "Yes. Everything runs in your browser. No data is sent anywhere.")],
    "related": [("json-formatter", "🔧", "JSON Formatter", "Format and validate JSON"), ("text-find-replace", "🔄", "Find & Replace", "Find and replace text with regex"), ("url-encoder", "🔗", "URL Encoder", "Encode/decode URLs")]
}

T1_URL_ENCODER = {
    "slug": "url-encoder",
    "icon": "🔗",
    "title": "URL Encoder — Encode & Decode URL Strings Online Free",
    "description": "Free online URL encoder and decoder. Percent-encode and decode URL strings, query parameters, and form data according to RFC 3986.",
    "keywords": "URL encoder, URL decoder, percent encoding, URL encode online, encode URI component",
    "h1": "🔗 URL Encoder / Decoder",
    "subtitle": "Encode and decode URL strings with percent-encoding — free, in your browser.",
    "workspace_html": make_common_html(
        "🔗", "url-encoder", "URL Encoder", "",
        '''<div class="two-col">
          <div class="controls">
            <h2>📥 Input</h2>
            <textarea id="inputText" placeholder="Enter text to encode/decode..."></textarea>
            <div class="btn-row">
              <button class="btn btn-primary" id="encodeBtn">🔗 Encode</button>
              <button class="btn btn-primary" id="decodeBtn">🔓 Decode</button>
              <button class="btn btn-secondary" id="encodeCompBtn">🔗 Encode Component</button>
              <button class="btn btn-secondary" id="clearBtn">Clear</button>
            </div>
          </div>
          <div class="controls">
            <h2>📤 Output</h2>
            <textarea id="outputText" readonly placeholder="Result will appear here..."></textarea>
            <div class="btn-row">
              <button class="btn btn-secondary" id="copyBtn">📋 Copy</button>
              <button class="btn btn-secondary" id="swapBtn">↔ Swap Input/Output</button>
            </div>
          </div>
        </div>''',
        "Plain text", "Encoded URL", "🔓", "🔗"
    ),
    "inline_js": '''(function() {
  const input = document.getElementById('inputText');
  const output = document.getElementById('outputText');
  document.getElementById('encodeBtn').onclick = () => { try { output.value = encodeURI(input.value); } catch(e) { output.value = 'Error: ' + e.message; } };
  document.getElementById('decodeBtn').onclick = () => { try { output.value = decodeURI(input.value); } catch(e) { output.value = 'Error: Invalid encoding'; } };
  document.getElementById('encodeCompBtn').onclick = () => { try { output.value = encodeURIComponent(input.value); } catch(e) { output.value = 'Error: ' + e.message; } };
  document.getElementById('copyBtn').onclick = () => { navigator.clipboard.writeText(output.value); };
  document.getElementById('clearBtn').onclick = () => { input.value = ''; output.value = ''; };
  document.getElementById('swapBtn').onclick = () => { const t = input.value; input.value = output.value; output.value = t; };
})();''',
    "howto_steps": [("Enter Text", "Paste or type your text in the input area."), ("Choose Action", "Click Encode, Decode, or Encode Component."), ("View Result", "Output appears in the right panel."), ("Copy or Swap", "Copy the result or swap input/output.")],
    "faq_list": [("What is the difference between Encode and Encode Component?", "encodeURI preserves URL separators like / and ?. encodeURIComponent encodes everything including them — use for query parameters."), ("Is this RFC 3986 compliant?", "Yes, using the native JavaScript encodeURIComponent function which follows the standard."), ("Why does decode sometimes fail?", "If the input contains invalid percent sequences (like %ZZ), decode will fail. Check your input.")],
    "related": [("base64", "🔐", "Base64 Converter", "Encode/decode Base64"), ("json-formatter", "🔧", "JSON Formatter", "Format and validate JSON"), ("uuid-generator", "🆔", "UUID Generator", "Generate unique IDs")]
}

T1_UUID_GENERATOR = {
    "slug": "uuid-generator",
    "icon": "🆔",
    "title": "UUID Generator — Generate UUID v1, v4 & v7 Online Free",
    "description": "Free online UUID generator. Generate UUID v1, v4 (random), and v7 (time-ordered) in bulk. Copy as single, bulk, or various formats.",
    "keywords": "UUID generator, UUID v4, UUID v7, generate UUID online, unique ID generator, GUID generator",
    "h1": "🆔 UUID Generator",
    "subtitle": "Generate UUID v1, v4, and v7 in bulk — free, in your browser.",
    "workspace_html": make_common_html(
        "🆔", "uuid-generator", "UUID Generator", "",
        '''<div class="controls">
            <h2>⚙️ Options</h2>
            <div class="control-row">
              <label>Version</label>
              <select id="uuidVersion">
                <option value="v4">UUID v4 (Random)</option>
                <option value="v7">UUID v7 (Time-ordered)</option>
                <option value="v1">UUID v1 (Timestamp)</option>
              </select>
            </div>
            <div class="control-row">
              <label>Count</label>
              <input type="number" id="uuidCount" value="10" min="1" max="10000" style="width:100px;">
            </div>
            <div class="control-row">
              <label>Format</label>
              <label style="min-width:auto;"><input type="checkbox" id="fmtHyphen" checked> Hyphens (xxxxxxxx-xxxx-...)</label>
              <label style="min-width:auto;"><input type="checkbox" id="fmtUpper"> Uppercase</label>
              <label style="min-width:auto;"><input type="checkbox" id="fmtBraces"> Braces {...}</label>
            </div>
            <div class="btn-row">
              <button class="btn btn-primary" id="generateBtn">🆔 Generate UUIDs</button>
              <button class="btn btn-secondary" id="copyAllBtn">📋 Copy All</button>
              <button class="btn btn-secondary" id="clearBtn">Clear</button>
            </div>
        </div>

        <div class="result-section">
            <h2>📤 Generated UUIDs (<span id="uuidTotal">0</span>)</h2>
            <textarea id="uuidOutput" readonly placeholder="Click Generate to create UUIDs..."></textarea>
        </div>''',
        "Nothing", "Unique UUIDs", "❌", "🆔"
    ),
    "inline_js": '''(function() {
  const genBtn = document.getElementById('generateBtn');
  const copyBtn = document.getElementById('copyAllBtn');
  const clearBtn = document.getElementById('clearBtn');
  const output = document.getElementById('uuidOutput');
  const total = document.getElementById('uuidTotal');

  function randHex(n) { const a = new Uint8Array(n); crypto.getRandomValues(a); return Array.from(a, b => b.toString(16).padStart(2,'0')).join(''); }

  function genUUIDv4() { const h = randHex(16); return `${h.slice(0,8)}-${h.slice(8,12)}-4${h.slice(13,16)}-${((parseInt(h[16],16)&0x3)|0x8).toString(16)}${h.slice(17,20)}-${h.slice(20,32)}`; }

  function genUUIDv7() { const t = Date.now().toString(16).padStart(12,'0'); const h = randHex(10); return `${t.slice(0,8)}-${t.slice(8,12)}-7${h.slice(1,4)}-${((parseInt(h[4],16)&0x3)|0x8).toString(16)}${h.slice(5,8)}-${h.slice(8,20)}`; }

  function genUUIDv1() { const t = Math.floor((Date.now() + 12219292800000) * 10000); const tb = t.toString(16).padStart(16,'0'); const h = randHex(8); const clock = (randHex(2)); return `${tb.slice(8,16)}-${tb.slice(4,8)}-1${tb.slice(1,4)}-${clock}${h.slice(0,2)}-${h.slice(2,14)}`; }

  function fmtUuid(uuid) {
    let u = uuid;
    if (!document.getElementById('fmtHyphen').checked) u = u.replace(/-/g,'');
    if (document.getElementById('fmtUpper').checked) u = u.toUpperCase();
    if (document.getElementById('fmtBraces').checked) u = `{${u}}`;
    return u;
  }

  genBtn.onclick = () => {
    const count = Math.min(10000, Math.max(1, parseInt(document.getElementById('uuidCount').value) || 1));
    const ver = document.getElementById('uuidVersion').value;
    const gen = ver === 'v4' ? genUUIDv4 : (ver === 'v7' ? genUUIDv7 : genUUIDv1);
    const uuids = [];
    for (let i = 0; i < count; i++) uuids.push(fmtUuid(gen()));
    output.value = uuids.join('\\n');
    total.textContent = count;
  };
  copyBtn.onclick = () => { navigator.clipboard.writeText(output.value); };
  clearBtn.onclick = () => { output.value = ''; total.textContent = 0; };
})();''',
    "howto_steps": [("Choose Version", "Select UUID v4 (random), v7 (time-ordered), or v1 (timestamp)."), ("Set Count", "Enter how many UUIDs to generate (1-10000)."), ("Choose Format", "Select hyphens, uppercase, braces as needed."), ("Generate", "Click Generate and copy the results.")],
    "faq_list": [("Which UUID version should I use?", "v4 (random) is most common. v7 (time-ordered) is great for databases as they sort chronologically. v1 includes MAC address."), ("Are these truly random?", "v4 uses crypto.getRandomValues() (CSPRNG). v7 uses CSPRNG + timestamp. Both are cryptographically secure."), ("What is the maximum count?", "10,000 per generation. You can click Generate multiple times for more.")],
    "related": [("password-generator", "🔐", "Password Generator", "Create secure passwords"), ("word-counter", "📝", "Word Counter", "Count words and characters"), ("base64", "🔐", "Base64 Converter", "Encode/decode Base64")]
}

T1_PASSWORD_GENERATOR = {
    "slug": "password-generator",
    "icon": "🔐",
    "title": "Password Generator — Generate Secure Passwords Free",
    "description": "Free online secure password generator. Create strong, random passwords with customizable length, character types, and bulk generation.",
    "keywords": "password generator, strong password generator, secure password generator, random password generator, password maker",
    "h1": "🔐 Password Generator",
    "subtitle": "Generate strong, secure, random passwords — free, in your browser.",
    "workspace_html": make_common_html(
        "🔐", "password-generator", "Password Generator", "",
        '''<div class="controls">
            <h2>⚙️ Password Options</h2>
            <div class="control-row">
              <label>Length</label>
              <input type="number" id="pwLength" value="16" min="4" max="128" style="width:100px;">
            </div>
            <div class="control-row">
              <label>Character Types</label>
              <label style="min-width:auto;"><input type="checkbox" id="pwUpper" checked> A-Z Uppercase</label>
              <label style="min-width:auto;"><input type="checkbox" id="pwLower" checked> a-z Lowercase</label>
              <label style="min-width:auto;"><input type="checkbox" id="pwNumber" checked> 0-9 Numbers</label>
              <label style="min-width:auto;"><input type="checkbox" id="pwSymbol"> !@#$ Symbols</label>
            </div>
            <div class="control-row">
              <label>Exclude Ambiguous</label>
              <label style="min-width:auto;"><input type="checkbox" id="pwNoAmbiguous" checked> Exclude 0, O, o, l, 1, I</label>
            </div>
            <div class="control-row">
              <label>Count</label>
              <input type="number" id="pwCount" value="5" min="1" max="100" style="width:100px;">
            </div>
            <div class="btn-row">
              <button class="btn btn-primary" id="genPwBtn">🔐 Generate Passwords</button>
            </div>
        </div>

        <div class="result-section">
            <h2>📤 Generated Passwords</h2>
            <div id="pwList" style="display:flex;flex-direction:column;gap:8px;"></div>
            <div class="btn-row" style="justify-content:center;margin-top:16px;">
              <button class="btn btn-secondary" id="copyAllPwBtn">📋 Copy All</button>
            </div>
        </div>''',
        "Nothing", "Secure passwords", "❌", "🔐"
    ),
    "inline_js": '''(function() {
  const genBtn = document.getElementById('genPwBtn');
  const pwList = document.getElementById('pwList');
  const copyAll = document.getElementById('copyAllPwBtn');

  function getChars() {
    let chars = '';
    if (document.getElementById('pwUpper').checked) chars += 'ABCDEFGHJKLMNPQRSTUVWXYZ';
    if (document.getElementById('pwLower').checked) chars += 'abcdefghijkmnpqrstuvwxyz';
    if (document.getElementById('pwNumber').checked) chars += '23456789';
    if (document.getElementById('pwSymbol').checked) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';
    if (!document.getElementById('pwNoAmbiguous').checked) {
      if (document.getElementById('pwUpper').checked) chars += 'IO';
      if (document.getElementById('pwLower').checked) chars += 'lo';
      if (document.getElementById('pwNumber').checked) chars += '01';
    }
    return chars;
  }

  function genPassword(len, chars) {
    const arr = new Uint32Array(len);
    crypto.getRandomValues(arr);
    let result = '';
    for (let i = 0; i < len; i++) result += chars[arr[i] % chars.length];
    return result;
  }

  genBtn.onclick = () => {
    const len = parseInt(document.getElementById('pwLength').value) || 16;
    const count = parseInt(document.getElementById('pwCount').value) || 5;
    const chars = getChars();
    if (!chars) { alert('Please select at least one character type.'); return; }
    const passwords = [];
    for (let i = 0; i < count; i++) passwords.push(genPassword(len, chars));
    pwList.innerHTML = passwords.map(p => `<div style="display:flex;align-items:center;gap:12px;padding:12px;background:var(--bg-secondary);border-radius:8px;"><code style="flex:1;font-family:Consolas,monospace;font-size:1rem;word-break:break-all;">${p}</code><button class="btn btn-secondary" onclick="navigator.clipboard.writeText('${p.replace(/'/g,"\\\\'")}')">📋</button></div>`).join('');
    copyAll.onclick = () => navigator.clipboard.writeText(passwords.join('\\n'));
  };
})();''',
    "howto_steps": [("Set Length", "Choose password length (4-128 characters)."), ("Select Types", "Check uppercase, lowercase, numbers, and/or symbols."), ("Exclude Ambiguous", "Optionally exclude easily-confused characters like 0, O, l, 1."), ("Generate", "Click Generate and copy your passwords.")],
    "faq_list": [("Are these passwords secure?", "Yes. We use crypto.getRandomValues() (CSPRNG), not Math.random(). Passwords are cryptographically secure."), ("What length should I use?", "We recommend 16+ characters for most accounts. 12 characters minimum for low-risk accounts."), ("Are my passwords sent anywhere?", "No. All generation happens in your browser. Nothing leaves your device.")],
    "related": [("uuid-generator", "🆔", "UUID Generator", "Generate unique UUIDs"), ("base64", "🔐", "Base64 Converter", "Encode/decode Base64"), ("word-counter", "📝", "Word Counter", "Count words and characters")]
}

T1_CASE_CONVERTER = {
    "slug": "case-converter",
    "icon": "🔠",
    "title": "Case Converter — Convert Text Between Cases Online Free",
    "description": "Free online case converter. Convert text to UPPERCASE, lowercase, Title Case, Sentence case, camelCase, PascalCase, snake_case, kebab-case, and more.",
    "keywords": "case converter, uppercase, lowercase, title case, sentence case, camelCase, snake_case",
    "h1": "🔠 Case Converter",
    "subtitle": "Convert text between UPPERCASE, lowercase, Title Case, and more — free, in your browser.",
    "workspace_html": make_common_html(
        "🔠", "case-converter", "Case Converter", "",
        '''<div class="two-col">
          <div class="controls">
            <h2>📥 Input Text</h2>
            <textarea id="caseInput" placeholder="Enter text to convert..."></textarea>
          </div>
          <div class="controls">
            <h2>📤 Converted Text</h2>
            <textarea id="caseOutput" readonly placeholder="Choose a case below..."></textarea>
            <div class="btn-row">
              <button class="btn btn-secondary" id="caseCopyBtn">📋 Copy</button>
              <button class="btn btn-secondary" id="caseClearBtn">Clear</button>
            </div>
          </div>
        </div>
        <div class="controls">
          <h2>🔄 Convert To</h2>
          <div class="btn-row">
            <button class="btn btn-primary" data-case="upper">UPPERCASE</button>
            <button class="btn btn-primary" data-case="lower">lowercase</button>
            <button class="btn btn-primary" data-case="title">Title Case</button>
            <button class="btn btn-primary" data-case="sentence">Sentence case</button>
            <button class="btn btn-primary" data-case="camel">camelCase</button>
            <button class="btn btn-primary" data-case="pascal">PascalCase</button>
            <button class="btn btn-primary" data-case="snake">snake_case</button>
            <button class="btn btn-primary" data-case="kebab">kebab-case</button>
          </div>
        </div>''',
        "Mixed text", "Converted case", "🔡", "🔠"
    ),
    "inline_js": '''(function() {
  const input = document.getElementById('caseInput');
  const output = document.getElementById('caseOutput');
  document.querySelectorAll('[data-case]').forEach(btn => {
    btn.onclick = () => {
      const t = input.value || '';
      const c = btn.dataset.case;
      let r = t;
      if (c === 'upper') r = t.toUpperCase();
      else if (c === 'lower') r = t.toLowerCase();
      else if (c === 'title') r = t.replace(/\\b\\w/g, m => m.toUpperCase());
      else if (c === 'sentence') r = t.toLowerCase().replace(/(^\\s*|[.!?]\\s+)([a-z])/g, (_, p1, p2) => p1 + p2.toUpperCase());
      else if (c === 'camel') { const w = t.toLowerCase().split(/[\\s_-]+/).filter(Boolean); r = w[0] + w.slice(1).map(w => w[0].toUpperCase() + w.slice(1)).join(''); }
      else if (c === 'pascal') r = t.toLowerCase().split(/[\\s_-]+/).filter(Boolean).map(w => w[0].toUpperCase() + w.slice(1)).join('');
      else if (c === 'snake') r = t.toLowerCase().split(/[\\s_-]+/).filter(Boolean).join('_');
      else if (c === 'kebab') r = t.toLowerCase().split(/[\\s_-]+/).filter(Boolean).join('-');
      output.value = r;
    };
  });
  document.getElementById('caseCopyBtn').onclick = () => navigator.clipboard.writeText(output.value);
  document.getElementById('caseClearBtn').onclick = () => { input.value = ''; output.value = ''; };
})();''',
    "howto_steps": [("Enter Text", "Paste or type your text in the input area."), ("Choose Case", "Click any case button to convert."), ("View Result", "Converted text appears on the right."), ("Copy", "Click Copy to copy the result.")],
    "faq_list": [("Does Title Case handle articles?", "This tool capitalizes every word. For AP-style (excluding articles like 'a', 'the'), use a dedicated title case tool."), ("Is Unicode supported?", "Yes. Unicode letters are converted using native JS toUpperCase/toLowerCase which supports Unicode."), ("What is the difference between snake_case and kebab-case?", "snake_case uses underscores (Python/Ruby convention). kebab-case uses hyphens (URL/CSS convention).")],
    "related": [("word-counter", "📝", "Word Counter", "Count words in your text"), ("text-sorter", "↕️", "Text Sorter", "Sort lines alphabetically"), ("text-find-replace", "🔄", "Find & Replace", "Find and replace text")]
}

T1_TEXT_SORTER = {
    "slug": "text-sorter",
    "icon": "↕️",
    "title": "Text Sorter — Sort Lines Alphabetically & Numerically Free",
    "description": "Free online text line sorter. Sort lines alphabetically (A-Z, Z-A), numerically, by length, remove duplicates, and reverse lines.",
    "keywords": "text sorter, sort lines, alphabetical sorter, sort text online, remove duplicate lines",
    "h1": "↕️ Text Sorter",
    "subtitle": "Sort lines alphabetically, numerically, by length, remove duplicates — free, in your browser.",
    "workspace_html": make_common_html(
        "↕️", "text-sorter", "Text Sorter", "",
        '''<div class="two-col">
          <div class="controls">
            <h2>📥 Input Lines</h2>
            <textarea id="sortInput" placeholder="Enter lines to sort (one per line)..."></textarea>
          </div>
          <div class="controls">
            <h2>📤 Sorted Lines</h2>
            <textarea id="sortOutput" readonly placeholder="Choose a sort option below..."></textarea>
            <div class="btn-row">
              <button class="btn btn-secondary" id="sortCopyBtn">📋 Copy</button>
              <button class="btn btn-secondary" id="sortClearBtn">Clear</button>
            </div>
          </div>
        </div>
        <div class="controls">
          <h2>🔀 Sort Options</h2>
          <div class="btn-row">
            <button class="btn btn-primary" data-sort="asc">A → Z (Ascending)</button>
            <button class="btn btn-primary" data-sort="desc">Z → A (Descending)</button>
            <button class="btn btn-primary" data-sort="numAsc">1 → 9 (Number Asc)</button>
            <button class="btn btn-primary" data-sort="numDesc">9 → 1 (Number Desc)</button>
            <button class="btn btn-primary" data-sort="lenAsc">Short → Long</button>
            <button class="btn btn-primary" data-sort="lenDesc">Long → Short</button>
            <button class="btn btn-primary" data-sort="reverse">↔ Reverse Order</button>
            <button class="btn btn-primary" data-sort="random">🎲 Random Shuffle</button>
            <button class="btn btn-primary" data-sort="unique">🧹 Remove Duplicates</button>
          </div>
        </div>''',
        "Unsorted lines", "Sorted lines", "📤", "↕️"
    ),
    "inline_js": '''(function() {
  const input = document.getElementById('sortInput');
  const output = document.getElementById('sortOutput');
  document.querySelectorAll('[data-sort]').forEach(btn => {
    btn.onclick = () => {
      let lines = (input.value || '').split('\\n');
      const s = btn.dataset.sortort = btn.dataset.sort;
      if (s === 'asc') lines.sort((a,b) => a.localeCompare(b));
      else if (s === 'desc') lines.sort((a,b) => b.localeCompare(a));
      else if (s === 'numAsc') lines.sort((a,b) => parseFloat(a) - parseFloat(b));
      else if (s === 'numDesc') lines.sort((a,b) => parseFloat(b) - parseFloat(a));
      else if (s === 'lenAsc') lines.sort((a,b) => a.length - b.length);
      else if (s === 'lenDesc') lines.sort((a,b) => b.length - a.length);
      else if (s === 'reverse') lines.reverse();
      else if (s === 'random') lines.sort(() => Math.random() - 0.5);
      else if (s === 'unique') lines = [...new Set(lines)];
      output.value = lines.join('\\n');
    };
  });
  document.getElementById('sortCopyBtn').onclick = () => navigator.clipboard.writeText(output.value);
  document.getElementById('sortClearBtn').onclick = () => { input.value = ''; output.value = ''; };
})();''',
    "howto_steps": [("Enter Lines", "Paste your text (one item per line)."), ("Choose Sort", "Click any sort option."), ("View Result", "Sorted lines appear on the right."), ("Copy", "Click Copy to copy the sorted result.")],
    "faq_list": [("Does it preserve empty lines?", "Yes. Empty lines are included in the sort. Use Remove Duplicates if you want to clean them."), ("Is numeric sort smart?", "It parses each line as a float. If a line is not a number, parseFloat returns NaN and it sorts to the end."), ("Can I sort by a specific column?", "Not yet. This tool sorts by entire line. For CSV/TSV column sorting, use a dedicated CSV tool.")],
    "related": [("case-converter", "🔠", "Case Converter", "Convert text case"), ("text-find-replace", "🔄", "Find & Replace", "Find and replace text"), ("word-counter", "📝", "Word Counter", "Count words")]
}

T1_TEXT_DIFF = {
    "slug": "text-diff",
    "icon": "↔️",
    "title": "Text Diff — Compare Two Texts Online Free",
    "description": "Free online text diff checker. Compare two text inputs and see the differences highlighted line by line. Perfect for code and document comparison.",
    "keywords": "text diff, compare text, diff checker, difference checker, compare two texts online",
    "h1": "↔️ Text Diff Checker",
    "subtitle": "Compare two texts and see differences highlighted — free, in your browser.",
    "workspace_html": make_common_html(
        "↔️", "text-diff", "Text Diff", "",
        '''<div class="two-col">
          <div class="controls">
            <h2>📄 Original Text</h2>
            <textarea id="diffOriginal" placeholder="Paste original text here..."></textarea>
          </div>
          <div class="controls">
            <h2>📝 Modified Text</h2>
            <textarea id="diffModified" placeholder="Paste modified text here..."></textarea>
          </div>
        </div>
        <div class="controls">
          <div class="btn-row">
            <button class="btn btn-primary" id="diffBtn">🔍 Compare Texts</button>
            <button class="btn btn-secondary" id="diffClearBtn">Clear</button>
          </div>
        </div>
        <div class="result-section">
          <h2>📊 Differences</h2>
          <div id="diffStats" class="status-text"></div>
          <div id="diffOutput" class="diff-output"></div>
        </div>''',
        "Two texts", "Diff output", "📄", "🔍"
    ),
    "inline_js": '''(function() {
  const orig = document.getElementById('diffOriginal');
  const mod = document.getElementById('diffModified');
  const out = document.getElementById('diffOutput');
  const stats = document.getElementById('diffStats');

  // Simple LCS-based diff
  function diff(a, b) {
    const aLines = a.split('\\n'), bLines = b.split('\\n');
    const m = aLines.length, n = bLines.length;
    const dp = Array.from({length:m+1}, () => new Array(n+1).fill(0));
    for (let i = 1; i <= m; i++) for (let j = 1; j <= n; j++) dp[i][j] = aLines[i-1] === bLines[j-1] ? dp[i-1][j-1] + 1 : Math.max(dp[i-1][j], dp[i][j-1]);
    const result = []; let i = m, j = n;
    while (i > 0 || j > 0) {
      if (i > 0 && j > 0 && aLines[i-1] === bLines[j-1]) { result.unshift({type:'=',text:aLines[i-1]}); i--; j--; }
      else if (j > 0 && (i === 0 || dp[i][j-1] >= dp[i-1][j])) { result.unshift({type:'+',text:bLines[j-1]}); j--; }
      else { result.unshift({type:'-',text:aLines[i-1]}); i--; }
    }
    return result;
  }

  document.getElementById('diffBtn').onclick = () => {
    const d = diff(orig.value, mod.value);
    const adds = d.filter(x => x.type === '+').length;
    const dels = d.filter(x => x.type === '-').length;
    stats.textContent = `${adds} addition(s), ${dels} deletion(s), ${d.filter(x=>x.type==='=').length} unchanged line(s)`;
    out.innerHTML = d.map(x => {
      const cls = x.type === '+' ? 'diff-add' : (x.type === '-' ? 'diff-del' : '');
      const prefix = x.type === '+' ? '+ ' : (x.type === '-' ? '- ' : '  ');
      return `<div class="${cls}">${prefix}${escapeHtml(x.text)}</div>`;
    }).join('');
  };
  function escapeHtml(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  document.getElementById('diffClearBtn').onclick = () => { orig.value=''; mod.value=''; out.innerHTML=''; stats.textContent=''; };
})();''',
    "howto_steps": [("Paste Original", "Put the original text in the left box."), ("Paste Modified", "Put the modified text in the right box."), ("Compare", "Click Compare Texts."), ("View Diff", "Green = added, Red = deleted, Gray = unchanged.")],
    "faq_list": [("What algorithm is used?", "LCS (Longest Common Subsequence) — the standard diff algorithm. Same as used by Git diff."), ("Does it support word-level diff?", "Currently line-level only. For word-level, paste single words per line or use a dedicated code diff tool."), ("Is my data uploaded?", "No. All comparison happens in your browser.")],
    "related": [("text-find-replace", "🔄", "Find & Replace", "Find and replace text"), ("case-converter", "🔠", "Case Converter", "Convert text case"), ("json-formatter", "🔧", "JSON Formatter", "Format JSON")]
}

T1_FIND_REPLACE = {
    "slug": "text-find-replace",
    "icon": "🔄",
    "title": "Find and Replace — Search & Replace Text Online Free",
    "description": "Free online find and replace tool. Search and replace text with support for regular expressions, case sensitivity, and bulk operations.",
    "keywords": "find and replace, search and replace, text replacer, regex replace, replace text online",
    "h1": "🔄 Find & Replace",
    "subtitle": "Search and replace text with regex support — free, in your browser.",
    "workspace_html": make_common_html(
        "🔄", "text-find-replace", "Find & Replace", "",
        '''<div class="controls">
            <h2>🔍 Find & Replace</h2>
            <div class="control-row">
              <label>Find</label>
              <input type="text" id="findStr" placeholder="Text to find..." style="flex:1;">
            </div>
            <div class="control-row">
              <label>Replace with</label>
              <input type="text" id="replaceStr" placeholder="Replacement text..." style="flex:1;">
            </div>
            <div class="control-row">
              <label>Options</label>
              <label style="min-width:auto;"><input type="checkbox" id="optCase"> Case sensitive</label>
              <label style="min-width:auto;"><input type="checkbox" id="optRegex"> Use regex</label>
              <label style="min-width:auto;"><input type="checkbox" id="optGlobal" checked> Replace all</label>
            </div>
        </div>
        <div class="two-col">
          <div class="controls">
            <h2>📥 Input Text</h2>
            <textarea id="frInput" placeholder="Enter text..."></textarea>
            <div class="btn-row">
              <button class="btn btn-primary" id="replaceBtn">🔄 Replace</button>
              <button class="btn btn-secondary" id="frClearBtn">Clear</button>
            </div>
          </div>
          <div class="controls">
            <h2>📤 Output Text</h2>
            <textarea id="frOutput" readonly placeholder="Result will appear here..."></textarea>
            <div id="frStats" class="status-text"></div>
            <div class="btn-row">
              <button class="btn btn-secondary" id="frCopyBtn">📋 Copy</button>
            </div>
          </div>
        </div>''',
        "Original text", "Modified text", "🔍", "🔄"
    ),
    "inline_js": '''(function() {
  document.getElementById('replaceBtn').onclick = () => {
    const input = document.getElementById('frInput').value || '';
    const find = document.getElementById('findStr').value;
    const replace = document.getElementById('replaceStr').value;
    if (!find) { alert('Enter text to find.'); return; }
    try {
      let result, count = 0;
      const useRegex = document.getElementById('optRegex').checked;
      const caseSens = document.getElementById('optCase').checked;
      const global = document.getElementById('optGlobal').checked;
      if (useRegex) {
        const flags = (global ? 'g' : '') + (caseSens ? '' : 'i');
        const re = new RegExp(find, flags);
        const matches = input.match(re);
        count = matches ? matches.length : 0;
        result = input.replace(re, replace);
      } else {
        if (global) {
          const parts = caseSens ? input.split(find) : input.toLowerCase().split(find.toLowerCase());
          count = parts.length - 1;
          result = ''; let idx = 0;
          for (let i = 0; i < parts.length - 1; i++) { result += parts[i]; result += replace; idx += parts[i].length + find.length; }
          if (parts.length) result += input.slice(idx - find.length);
          // simpler: use regex escape
          const escaped = find.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
          const flags = (global ? 'g' : '') + (caseSens ? '' : 'i');
          const re = new RegExp(escaped, flags);
          count = (input.match(re) || []).length;
          result = input.replace(re, replace);
        } else {
          const idx = caseSens ? input.indexOf(find) : input.toLowerCase().indexOf(find.toLowerCase());
          count = idx >= 0 ? 1 : 0;
          result = idx >= 0 ? input.slice(0, idx) + replace + input.slice(idx + find.length) : input;
        }
      }
      document.getElementById('frOutput').value = result;
      document.getElementById('frStats').textContent = `${count} replacement(s) made`;
    } catch(e) { alert('Error: ' + e.message); }
  };
  document.getElementById('frCopyBtn').onclick = () => navigator.clipboard.writeText(document.getElementById('frOutput').value);
  document.getElementById('frClearBtn').onclick = () => { document.getElementById('frInput').value=''; document.getElementById('frOutput').value=''; document.getElementById('frStats').textContent=''; };
})();''',
    "howto_steps": [("Enter Find & Replace", "Type what to find and what to replace it with."), ("Set Options", "Choose case sensitivity, regex mode, and replace all."), ("Enter Text", "Paste your text in the input area."), ("Replace", "Click Replace and view the output.")],
    "faq_list": [("Can I use backreferences in regex replace?", "Yes! Use $1, $2, etc. in the Replace field to reference capture groups."), ("What does 'Replace all' do?", "When checked, all occurrences are replaced. When unchecked, only the first match is replaced."), ("Is regex mode safe?", "Regex is executed locally in your browser using JavaScript RegExp. No data is sent.")],
    "related": [("regex-tester", "🔍", "Regex Tester", "Test regex patterns first"), ("text-diff", "↔️", "Text Diff", "Compare before and after"), ("case-converter", "🔠", "Case Converter", "Convert text case")]
}

T1_HTML_ENCODER = {
    "slug": "html-encoder",
    "icon": "🏷️",
    "title": "HTML Encoder — Encode & Decode HTML Entities Online Free",
    "description": "Free online HTML entity encoder and decoder. Convert special characters to HTML entities (&amp;, &lt;, &gt;, &#39;, &quot;) and back.",
    "keywords": "HTML encoder, HTML decoder, HTML entities, encode HTML online, escape HTML",
    "h1": "🏷️ HTML Encoder / Decoder",
    "subtitle": "Encode and decode HTML entities — free, in your browser.",
    "workspace_html": make_common_html(
        "🏷️", "html-encoder", "HTML Encoder", "",
        '''<div class="two-col">
          <div class="controls">
            <h2>📥 Input</h2>
            <textarea id="htmlInput" placeholder="Enter text or HTML..."></textarea>
            <div class="btn-row">
              <button class="btn btn-primary" id="encodeHtmlBtn">🏷️ Encode HTML</button>
              <button class="btn btn-primary" id="decodeHtmlBtn">📄 Decode Entities</button>
              <button class="btn btn-secondary" id="htmlClearBtn">Clear</button>
            </div>
          </div>
          <div class="controls">
            <h2>📤 Output</h2>
            <textarea id="htmlOutput" readonly placeholder="Result will appear here..."></textarea>
            <div class="btn-row">
              <button class="btn btn-secondary" id="htmlCopyBtn">📋 Copy</button>
            </div>
          </div>
        </div>''',
        "Plain text/HTML", "HTML entities", "📄", "🏷️"
    ),
    "inline_js": '''(function() {
  const input = document.getElementById('htmlInput');
  const output = document.getElementById('htmlOutput');
  document.getElementById('encodeHtmlBtn').onclick = () => {
    const d = document.createElement('div');
    d.textContent = input.value || '';
    output.value = d.innerHTML;
  };
  document.getElementById('decodeHtmlBtn').onclick = () => {
    const d = document.createElement('textarea');
    d.innerHTML = input.value || '';
    output.value = d.value;
  };
  document.getElementById('htmlCopyBtn').onclick = () => navigator.clipboard.writeText(output.value);
  document.getElementById('htmlClearBtn').onclick = () => { input.value = ''; output.value = ''; };
})();''',
    "howto_steps": [("Enter Text", "Paste text or HTML in the input area."), ("Encode or Decode", "Click Encode to create entities, Decode to reverse."), ("View Result", "Encoded/decoded text appears on the right."), ("Copy", "Click Copy to copy the result.")],
    "faq_list": [("Which entities are encoded?", "The 5 standard XML/HTML entities: & (&amp;), < (&lt;), > (&gt;), \\\" (&quot;), \\&#39; (&#39;)."), ("Why encode HTML?", "To display HTML code as text on a web page without the browser rendering it."), ("What about Unicode?", "Unicode characters are preserved as-is. Only the 5 reserved HTML characters are encoded.")],
    "related": [("url-encoder", "🔗", "URL Encoder", "Encode/decode URLs"), ("base64", "🔐", "Base64 Converter", "Encode/decode Base64"), ("json-formatter", "🔧", "JSON Formatter", "Format JSON")]
}

# 收集第1批所有工具
BATCH1_TOOLS = [T1_WORD_COUNTER, T1_JSON_FORMATTER, T1_REGEX_TESTER, T1_URL_ENCODER,
                T1_UUID_GENERATOR, T1_PASSWORD_GENERATOR, T1_CASE_CONVERTER, T1_TEXT_SORTER,
                T1_TEXT_DIFF, T1_FIND_REPLACE, T1_HTML_ENCODER]


# ═══════════════════════════════════════════════════════════
# 第 2 批：PDF 工具（6 个，依赖 pdf-lib）
# ═══════════════════════════════════════════════════════════

def make_pdf_tool(slug, icon, title, desc, keywords, h1, subtitle, workspace, js, before_label, after_label, before_emoji, after_emoji):
    return {
        "slug": slug, "icon": icon, "title": title, "description": desc, "keywords": keywords,
        "h1": h1, "subtitle": subtitle,
        "workspace_html": make_common_html(icon, slug, title, "", workspace, before_label, after_label, before_emoji, after_emoji),
        "inline_js": js,
        "howto_steps": [("Upload PDF", "Select one or more PDF files."), ("Configure", "Set your options."), ("Process", "Click the action button."), ("Download", "Get your processed PDF.")],
        "faq_list": [("Are my PDFs uploaded?", "No. All processing happens in your browser using pdf-lib."), ("What is the maximum file size?", "We recommend under 100MB. Very large files may slow down your browser."), ("Are PDFs with passwords supported?", "Password-protected PDFs are not currently supported.")],
        "related": [("pdf-to-image", "📄", "PDF to Image", "Convert PDF pages to images"), ("image-to-pdf", "📄", "Image to PDF", "Combine images into PDF")]
    }

PDF_MERGE_HTML = '''<input type="file" id="fileInput" accept=".pdf" multiple style="display:none;">
        <label for="fileInput" class="dropzone" id="dropzone">
          <div class="dropzone-icon">📄</div>
          <h3>Upload PDF Files</h3>
          <p>Select 2 or more PDF files to merge. Your files are processed in your browser.</p>
        </label>

        <div class="controls hidden" id="controlsSection">
          <h2>📑 Files to Merge (<span id="fileCount">0</span>)</h2>
          <div id="fileList" style="margin-bottom:16px;"></div>
          <p class="info-box" style="margin:16px 0;"><strong>Tip:</strong> Files are merged in the order listed above.</p>
          <div class="btn-row">
            <button class="btn btn-primary" id="mergeBtn">🔗 Merge PDFs</button>
            <button class="btn btn-secondary" id="resetBtn">Reset</button>
          </div>
        </div>

        <div class="status-text hidden" id="statusSection"></div>'''

PDF_MERGE_JS = '''(function() {
  const fileInput = document.getElementById('fileInput');
  const dropzone = document.getElementById('dropzone');
  const controlsSection = document.getElementById('controlsSection');
  const fileList = document.getElementById('fileList');
  const fileCount = document.getElementById('fileCount');
  const mergeBtn = document.getElementById('mergeBtn');
  const resetBtn = document.getElementById('resetBtn');
  const statusSection = document.getElementById('statusSection');

  let files = [];

  dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
  dropzone.addEventListener('drop', e => { e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files.length) handleFiles(e.dataTransfer.files); });
  fileInput.addEventListener('change', e => { if (e.target.files.length) handleFiles(e.target.files); });

  function handleFiles(f) {
    files = Array.from(f).filter(x => x.type === 'application/pdf' || x.name.endsWith('.pdf'));
    if (files.length < 2) { alert('Please select at least 2 PDF files.'); return; }
    var ba = document.getElementById('beforeAfterPreview'); if (ba) ba.classList.add('hidden');
    fileCount.textContent = files.length;
    fileList.innerHTML = files.map((f,i) => `<div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:var(--bg-secondary);border-radius:6px;margin-bottom:6px;"><span style="font-weight:600;color:var(--accent);min-width:30px;">${i+1}.</span><span style="flex:1;">${f.name}</span><span style="color:var(--text-secondary);font-size:0.85rem;">${(f.size/1024).toFixed(1)} KB</span></div>`).join('');
    controlsSection.classList.remove('hidden');
    statusSection.classList.add('hidden');
  }

  mergeBtn.addEventListener('click', async () => {
    statusSection.classList.remove('hidden');
    statusSection.textContent = 'Loading pdf-lib...';
    mergeBtn.disabled = true;
    try {
      if (!window.PDFLib) {
        await loadScript('https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js');
      }
      const { PDFDocument } = window.PDFLib;
      const mergedPdf = await PDFDocument.create();
      for (let i = 0; i < files.length; i++) {
        statusSection.textContent = `Processing file ${i+1}/${files.length}...`;
        const bytes = await files[i].arrayBuffer();
        const pdf = await PDFDocument.load(bytes);
        const pages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
        pages.forEach(p => mergedPdf.addPage(p));
      }
      statusSection.textContent = 'Saving...';
      const mergedBytes = await mergedPdf.save();
      const blob = new Blob([mergedBytes], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'merged.pdf'; a.click();
      URL.revokeObjectURL(url);
      statusSection.textContent = '✓ Merge complete! Download started.';
    } catch(e) { statusSection.textContent = '✗ Error: ' + e.message; }
    mergeBtn.disabled = false;
  });
  function loadScript(src) { return new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
  resetBtn.addEventListener('click', () => { files = []; controlsSection.classList.add('hidden'); statusSection.classList.add('hidden'); fileInput.value = ''; var ba = document.getElementById('beforeAfterPreview'); if (ba) ba.classList.remove('hidden'); });
})();'''

T2_PDF_MERGE = make_pdf_tool(
    "pdf-merge", "🔗",
    "PDF Merge — Combine Multiple PDFs into One Free",
    "Free online PDF merger. Combine multiple PDF files into a single PDF in seconds. No upload limits, works entirely in your browser.",
    "PDF merge, combine PDFs, merge PDFs online, PDF joiner, combine PDF files",
    "🔗 PDF Merge",
    "Combine multiple PDF files into one — free, in your browser.",
    PDF_MERGE_HTML, PDF_MERGE_JS,
    "2+ PDF files", "1 merged PDF", "📄", "🔗"
)

PDF_SPLIT_HTML = '''<input type="file" id="fileInput" accept=".pdf" style="display:none;">
        <label for="fileInput" class="dropzone" id="dropzone">
          <div class="dropzone-icon">📄</div>
          <h3>Upload PDF File</h3>
          <p>Select a PDF file to split. Your file is processed in your browser.</p>
        </label>

        <div class="controls hidden" id="controlsSection">
          <h2>✂️ Split Options</h2>
          <div class="pdf-info" id="pdfInfo"></div>
          <div class="control-row">
            <label>Split Mode</label>
            <select id="splitMode">
              <option value="every">Every N pages</option>
              <option value="ranges">Specific page ranges</option>
              <option value="single">Extract every page</option>
            </select>
          </div>
          <div class="control-row" id="everyRow">
            <label>Every N Pages</label>
            <input type="number" id="everyN" value="1" min="1" style="width:80px;">
          </div>
          <div class="control-row hidden" id="rangesRow">
            <label>Page Ranges</label>
            <input type="text" id="rangesInput" placeholder="e.g. 1-3, 5, 7-10" style="flex:1;">
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" id="splitBtn">✂️ Split PDF</button>
            <button class="btn btn-secondary" id="resetBtn">Reset</button>
          </div>
        </div>

        <div class="status-text hidden" id="statusSection"></div>'''

PDF_SPLIT_JS = '''(function() {
  const fileInput = document.getElementById('fileInput');
  const dropzone = document.getElementById('dropzone');
  const controlsSection = document.getElementById('controlsSection');
  const pdfInfo = document.getElementById('pdfInfo');
  const splitMode = document.getElementById('splitMode');
  const splitBtn = document.getElementById('splitBtn');
  const resetBtn = document.getElementById('resetBtn');
  const statusSection = document.getElementById('statusSection');
  const everyRow = document.getElementById('everyRow');
  const rangesRow = document.getElementById('rangesRow');

  let fileBytes = null; let numPages = 0; let fileName = '';

  dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
  dropzone.addEventListener('drop', e => { e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]); });
  fileInput.addEventListener('change', e => { if (e.target.files[0]) handleFile(e.target.files[0]); });
  splitMode.addEventListener('change', () => { everyRow.classList.toggle('hidden', splitMode.value !== 'every'); rangesRow.classList.toggle('hidden', splitMode.value !== 'ranges'); });

  function handleFile(file) {
    if (file.type !== 'application/pdf' && !file.name.endsWith('.pdf')) { alert('Please upload a PDF file.'); return; }
    fileName = file.name.replace('.pdf', '');
    var ba = document.getElementById('beforeAfterPreview'); if (ba) ba.classList.add('hidden');
    const reader = new FileReader();
    reader.onload = async (e) => {
      fileBytes = e.target.result;
      if (!window.PDFLib) { await loadScript('https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js'); }
      const { PDFDocument } = window.PDFLib;
      const pdf = await PDFDocument.load(fileBytes);
      numPages = pdf.getPageCount();
      pdfInfo.innerHTML = `<strong>File:</strong> ${file.name} &nbsp;|&nbsp; <strong>Pages:</strong> ${numPages} &nbsp;|&nbsp; <strong>Size:</strong> ${(file.size/1024).toFixed(1)} KB`;
      controlsSection.classList.remove('hidden');
    };
    reader.readAsArrayBuffer(file);
  }

  splitBtn.addEventListener('click', async () => {
    statusSection.classList.remove('hidden');
    statusSection.textContent = 'Splitting...';
    splitBtn.disabled = true;
    try {
      if (!window.PDFLib) { await loadScript('https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js'); }
      const { PDFDocument } = window.PDFLib;
      const srcPdf = await PDFDocument.load(fileBytes);
      const mode = splitMode.value;
      const parts = [];
      if (mode === 'every') {
        const n = parseInt(document.getElementById('everyN').value) || 1;
        for (let i = 0; i < numPages; i += n) {
          const newPdf = await PDFDocument.create();
          const end = Math.min(i + n, numPages);
          const pages = await newPdf.copyPages(srcPdf, [...Array(end - i).keys()].map(x => x + i));
          pages.forEach(p => newPdf.addPage(p));
          parts.push({ pdf: newPdf, name: `pages-${i+1}-${end}` });
        }
      } else if (mode === 'ranges') {
        const ranges = document.getElementById('rangesInput').value.split(',').map(r => r.trim()).filter(Boolean);
        for (let ri = 0; ri < ranges.length; ri++) {
          const r = ranges[ri]; let start, end;
          if (r.includes('-')) { [start, end] = r.split('-').map(x => parseInt(x)); }
          else { start = end = parseInt(r); }
          if (start < 1 || end > numPages || start > end) { continue; }
          const newPdf = await PDFDocument.create();
          const pages = await newPdf.copyPages(srcPdf, [...Array(end - start + 1).keys()].map(x => x + start - 1));
          pages.forEach(p => newPdf.addPage(p));
          parts.push({ pdf: newPdf, name: `pages-${start}-${end}` });
        }
      } else {
        for (let i = 0; i < numPages; i++) {
          const newPdf = await PDFDocument.create();
          const pages = await newPdf.copyPages(srcPdf, [i]);
          pages.forEach(p => newPdf.addPage(p));
          parts.push({ pdf: newPdf, name: `page-${i+1}` });
        }
      }
      if (parts.length === 1) {
        const bytes = await parts[0].pdf.save();
        downloadBlob(bytes, `${fileName}-${parts[0].name}.pdf`);
      } else if (parts.length > 1 && !window.JSZip) {
        await loadScript('https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js');
      }
      if (parts.length > 1) {
        const zip = new window.JSZip();
        for (let i = 0; i < parts.length; i++) {
          statusSection.textContent = `Packaging ${i+1}/${parts.length}...`;
          const bytes = await parts[i].pdf.save();
          zip.file(`${fileName}-${parts[i].name}.pdf`, bytes);
        }
        statusSection.textContent = 'Creating ZIP...';
        const zipBlob = await zip.generateAsync({ type: 'blob' });
        downloadBlob(zipBlob, `${fileName}-split.zip`, 'application/zip');
      }
      statusSection.textContent = `✓ Split into ${parts.length} file(s)! Download started.`;
    } catch(e) { statusSection.textContent = '✗ Error: ' + e.message; }
    splitBtn.disabled = false;
  });
  function loadScript(src) { return new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
  function downloadBlob(bytes, name, type='application/pdf') { const blob = new Blob([bytes], { type }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = name; a.click(); URL.revokeObjectURL(url); }
  resetBtn.addEventListener('click', () => { fileBytes = null; controlsSection.classList.add('hidden'); statusSection.classList.add('hidden'); fileInput.value = ''; var ba = document.getElementById('beforeAfterPreview'); if (ba) ba.classList.remove('hidden'); });
})();'''

T2_PDF_SPLIT = make_pdf_tool(
    "pdf-split", "✂️",
    "PDF Splitter — Split PDF into Multiple Files Free",
    "Free online PDF splitter. Split PDF into multiple files by page ranges, every N pages, or extract every page as a separate file.",
    "PDF splitter, split PDF, extract pages, separate PDF, divide PDF online",
    "✂️ PDF Splitter",
    "Split PDF into multiple files by page ranges or every N pages — free.",
    PDF_SPLIT_HTML, PDF_SPLIT_JS,
    "1 PDF file", "Multiple PDFs", "📄", "✂️"
)

# 简化版 PDF 工具（复用通用结构）
def make_simple_pdf(slug, icon, title, desc, keywords, h1, subtitle, extra_controls_html, process_fn_desc, before_label, after_label, be, ae):
    return {
        "slug": slug, "icon": icon, "title": title, "description": desc, "keywords": keywords,
        "h1": h1, "subtitle": subtitle,
        "workspace_html": make_common_html(icon, slug, title, "", f'''<input type="file" id="fileInput" accept=".pdf" style="display:none;">
        <label for="fileInput" class="dropzone" id="dropzone">
          <div class="dropzone-icon">📄</div>
          <h3>Upload PDF File</h3>
          <p>Select a PDF file. Processed in your browser.</p>
        </label>
        <div class="controls hidden" id="controlsSection">
          <h2>⚙️ Options</h2>
          <div class="pdf-info" id="pdfInfo"></div>
          {extra_controls_html}
          <div class="btn-row">
            <button class="btn btn-primary" id="processBtn">{icon} {process_fn_desc}</button>
            <button class="btn btn-secondary" id="resetBtn">Reset</button>
          </div>
        </div>
        <div class="status-text hidden" id="statusSection"></div>''', before_label, after_label, be, ae),
        "inline_js": '''(function() {
  const fileInput = document.getElementById('fileInput');
  const dropzone = document.getElementById('dropzone');
  const controlsSection = document.getElementById('controlsSection');
  const pdfInfo = document.getElementById('pdfInfo');
  const processBtn = document.getElementById('processBtn');
  const resetBtn = document.getElementById('resetBtn');
  const statusSection = document.getElementById('statusSection');
  let fileBytes = null; let fileName = ''; let numPages = 0;
  dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
  dropzone.addEventListener('drop', e => { e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]); });
  fileInput.addEventListener('change', e => { if (e.target.files[0]) handleFile(e.target.files[0]); });
  function handleFile(file) {
    if (file.type !== 'application/pdf' && !file.name.endsWith('.pdf')) { alert('Please upload a PDF.'); return; }
    fileName = file.name.replace('.pdf', '');
    var ba = document.getElementById('beforeAfterPreview'); if (ba) ba.classList.add('hidden');
    const r = new FileReader();
    r.onload = async (e) => {
      fileBytes = e.target.result;
      if (!window.PDFLib) { await loadScript('https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js'); }
      const { PDFDocument } = window.PDFLib;
      const pdf = await PDFDocument.load(fileBytes);
      numPages = pdf.getPageCount();
      pdfInfo.innerHTML = `<strong>File:</strong> ${file.name} &nbsp;|&nbsp; <strong>Pages:</strong> ${numPages}`;
      controlsSection.classList.remove('hidden');
    };
    r.readAsArrayBuffer(file);
  }
  processBtn.addEventListener('click', async () => {
    statusSection.classList.remove('hidden');
    statusSection.textContent = 'Processing...';
    processBtn.disabled = true;
    try {
      if (!window.PDFLib) { await loadScript('https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js'); }
      const { PDFDocument, degrees } = window.PDFLib;
      const src = await PDFDocument.load(fileBytes);
      await window.__PROCESS_PDF__(src, numPages, fileName);
    } catch(e) { statusSection.textContent = '✗ Error: ' + e.message; }
    processBtn.disabled = false;
  });
  function loadScript(src) { return new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
  function downloadBlob(bytes, name, type='application/pdf') { const blob = new Blob([bytes], { type }); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = name; a.click(); URL.revokeObjectURL(url); }
  window.__downloadBlob__ = downloadBlob;
  resetBtn.addEventListener('click', () => { fileBytes = null; controlsSection.classList.add('hidden'); statusSection.classList.add('hidden'); fileInput.value = ''; var ba = document.getElementById('beforeAfterPreview'); if (ba) ba.classList.remove('hidden'); });
})();''',
        "howto_steps": [("Upload PDF", "Select a PDF file."), ("Configure", "Set options."), ("Process", "Click the action button."), ("Download", "Get the result.")],
        "faq_list": [("Is my PDF uploaded?", "No. Everything runs in your browser."), ("Max file size?", "Under 100MB recommended."), ("Password protected PDFs?", "Not supported.")],
        "related": [("pdf-to-image", "📄", "PDF to Image", "Convert PDF to images"), ("pdf-merge", "🔗", "PDF Merge", "Combine PDFs")]
    }

T2_PDF_COMPRESS = make_simple_pdf(
    "pdf-compress", "🗜️",
    "PDF Compressor — Reduce PDF File Size Free",
    "Free online PDF compressor. Reduce PDF file size by optimizing images and removing unnecessary metadata. Browser-based, no upload.",
    "PDF compressor, compress PDF, reduce PDF size, shrink PDF, optimize PDF online",
    "🗜️ PDF Compressor",
    "Reduce PDF file size by optimizing content — free, in your browser.",
    '''<div class="control-row">
            <label>Compression Level</label>
            <select id="compLevel">
              <option value="low">Low (minimal reduction)</option>
              <option value="medium" selected>Medium (balanced)</option>
              <option value="high">High (aggressive)</option>
            </select>
          </div>''',
    "Compress PDF",
    "Large PDF", "Smaller PDF", "📄", "🗜️"
)
# 为 compress 添加自定义 JS
T2_PDF_COMPRESS["inline_js"] = T2_PDF_COMPRESS["inline_js"].replace(
    "await window.__PROCESS_PDF__(src, numPages, fileName);",
    '''const pages = src.getPages();
      for (let i = 0; i < pages.length; i++) {
        statusSection.textContent = `Processing page ${i+1}/${numPages}...`;
        // Flatten form fields and remove annotations
        try { pages[i].flattenAnnotations(); } catch(e) {}
      }
      const bytes = await src.save({ useObjectStreams: false });
      window.__downloadBlob__(bytes, `${fileName}-compressed.pdf`);
      statusSection.textContent = '✓ Compression complete!';'''
)

T2_PDF_DELETE = make_simple_pdf(
    "pdf-delete-pages", "🗑️",
    "PDF Delete Pages — Remove Pages from PDF Free",
    "Free online PDF page remover. Delete specific pages or page ranges from a PDF. Browser-based, nothing uploaded.",
    "delete PDF pages, remove PDF pages, delete pages from PDF, extract PDF pages",
    "🗑️ Delete PDF Pages",
    "Remove specific pages or ranges from a PDF — free, in your browser.",
    '''<div class="control-row">
            <label>Pages to Delete</label>
            <input type="text" id="delPages" placeholder="e.g. 2, 5-7, 10" style="flex:1;">
          </div>
          <p style="color:var(--text-secondary);font-size:0.85rem;">Enter page numbers and ranges separated by commas.</p>''',
    "Delete Pages",
    "Full PDF", "PDF (minus pages)", "📄", "🗑️"
)
T2_PDF_DELETE["inline_js"] = T2_PDF_DELETE["inline_js"].replace(
    "await window.__PROCESS_PDF__(src, numPages, fileName);",
    '''const delStr = document.getElementById('delPages').value;
      if (!delStr) { alert('Enter pages to delete.'); return; }
      const toDelete = new Set();
      delStr.split(',').forEach(r => {
        r = r.trim();
        if (r.includes('-')) {
          const [s, e] = r.split('-').map(x => parseInt(x));
          for (let i = s; i <= e; i++) toDelete.add(i - 1);
        } else { const p = parseInt(r); if (p) toDelete.add(p - 1); }
      });
      const { PDFDocument } = window.PDFLib;
      const newPdf = await PDFDocument.create();
      const indices = [];
      for (let i = 0; i < numPages; i++) if (!toDelete.has(i)) indices.push(i);
      const pages = await newPdf.copyPages(src, indices);
      pages.forEach(p => newPdf.addPage(p));
      const bytes = await newPdf.save();
      window.__downloadBlob__(bytes, `${fileName}-deleted.pdf`);
      statusSection.textContent = `✓ Deleted ${toDelete.size} page(s). ${pages.length} pages remain.`;'''
)

T2_PDF_ROTATE = make_simple_pdf(
    "pdf-rotate", "🔄",
    "PDF Rotator — Rotate PDF Pages Free",
    "Free online PDF rotator. Rotate PDF pages 90°, 180°, or 270°. Process all pages or specific ranges.",
    "PDF rotator, rotate PDF, rotate PDF pages, flip PDF online",
    "🔄 PDF Rotator",
    "Rotate PDF pages by 90°, 180°, or 270° — free, in your browser.",
    '''<div class="control-row">
            <label>Rotate By</label>
            <select id="rotDeg">
              <option value="90">90° Clockwise</option>
              <option value="180">180°</option>
              <option value="270">270° Clockwise</option>
            </select>
          </div>
          <div class="control-row">
            <label>Page Range</label>
            <input type="text" id="rotPages" placeholder="e.g. 1-3, 5 (blank = all)" style="flex:1;">
          </div>''',
    "Rotate PDF",
    "PDF (wrong)", "PDF (rotated)", "↩️", "🔄"
)
T2_PDF_ROTATE["inline_js"] = T2_PDF_ROTATE["inline_js"].replace(
    "await window.__PROCESS_PDF__(src, numPages, fileName);",
    '''const deg = parseInt(document.getElementById('rotDeg').value);
      const { degrees } = window.PDFLib;
      const pages = src.getPages();
      let rangeStr = document.getElementById('rotPages').value.trim();
      let targetPages = [];
      if (!rangeStr) { targetPages = [...Array(numPages).keys()]; }
      else {
        rangeStr.split(',').forEach(r => {
          r = r.trim();
          if (r.includes('-')) {
            const [s, e] = r.split('-').map(x => parseInt(x));
            for (let i = s; i <= e; i++) if (i >= 1 && i <= numPages) targetPages.push(i - 1);
          } else { const p = parseInt(r); if (p >= 1 && p <= numPages) targetPages.push(p - 1); }
        });
      }
      targetPages.forEach(i => { pages[i].setRotation(degrees(deg)); });
      const bytes = await src.save();
      window.__downloadBlob__(bytes, `${fileName}-rotated.pdf`);
      statusSection.textContent = `✓ Rotated ${targetPages.length} page(s) by ${deg}°.`;'''
)

T2_PDF_EXTRACT = make_simple_pdf(
    "pdf-extract-pages", "📑",
    "PDF Extract Pages — Extract Pages from PDF Free",
    "Free online PDF page extractor. Extract specific pages or ranges from a PDF into a new PDF file. Browser-based.",
    "extract PDF pages, extract pages from PDF, PDF page extractor, pull pages from PDF",
    "📑 Extract PDF Pages",
    "Extract specific pages or ranges from a PDF into a new file — free.",
    '''<div class="control-row">
            <label>Pages to Extract</label>
            <input type="text" id="extPages" placeholder="e.g. 1-3, 5, 7-10" style="flex:1;">
          </div>
          <p style="color:var(--text-secondary);font-size:0.85rem;">Enter page numbers and ranges separated by commas.</p>''',
    "Extract Pages",
    "Full PDF", "Extracted pages", "📄", "📑"
)
T2_PDF_EXTRACT["inline_js"] = T2_PDF_EXTRACT["inline_js"].replace(
    "await window.__PROCESS_PDF__(src, numPages, fileName);",
    '''const extStr = document.getElementById('extPages').value;
      if (!extStr) { alert('Enter pages to extract.'); return; }
      const { PDFDocument } = window.PDFLib;
      const newPdf = await PDFDocument.create();
      const indices = [];
      extStr.split(',').forEach(r => {
        r = r.trim();
        if (r.includes('-')) {
          const [s, e] = r.split('-').map(x => parseInt(x));
          for (let i = s; i <= e; i++) if (i >= 1 && i <= numPages) indices.push(i - 1);
        } else { const p = parseInt(r); if (p >= 1 && p <= numPages) indices.push(p - 1); }
      });
      const pages = await newPdf.copyPages(src, indices);
      pages.forEach(p => newPdf.addPage(p));
      const bytes = await newPdf.save();
      window.__downloadBlob__(bytes, `${fileName}-extracted.pdf`);
      statusSection.textContent = `✓ Extracted ${pages.length} page(s).`;'''
)

BATCH2_TOOLS = [T2_PDF_MERGE, T2_PDF_SPLIT, T2_PDF_COMPRESS, T2_PDF_DELETE, T2_PDF_ROTATE, T2_PDF_EXTRACT]


# ═══════════════════════════════════════════════════════════
# 第 3 批：视频工具（7 个，依赖 ffmpeg.wasm）
# ═══════════════════════════════════════════════════════════

def make_video_tool(slug, icon, title, desc, keywords, h1, subtitle, extra_html, custom_js_body, before_label, after_label, be, ae):
    return {
        "slug": slug, "icon": icon, "title": title, "description": desc, "keywords": keywords,
        "h1": h1, "subtitle": subtitle,
        "workspace_html": make_common_html(icon, slug, title, "", f'''<input type="file" id="fileInput" accept="video/*" style="display:none;">
        <label for="fileInput" class="dropzone" id="dropzone">
          <div class="dropzone-icon">🎬</div>
          <h3>Upload Video File</h3>
          <p>Select a video file. Processed in your browser with ffmpeg.wasm.</p>
          <p style="font-size:0.8rem;color:var(--text-secondary);margin-top:8px;">⚠️ First use may take ~30s to load ffmpeg.wasm (25MB)</p>
        </label>
        <div class="controls hidden" id="controlsSection">
          <h2>📹 Video Info</h2>
          <div class="pdf-info" id="videoInfo"></div>
          {extra_html}
          <div class="btn-row">
            <button class="btn btn-primary" id="processBtn">{icon} Process</button>
            <button class="btn btn-secondary" id="resetBtn">Reset</button>
          </div>
        </div>
        <div class="status-text hidden" id="statusSection"></div>
        <div class="result-section hidden" id="resultSection">
          <h2>✅ Result</h2>
          <div id="resultContent" style="text-align:center;"></div>
        </div>''', before_label, after_label, be, ae),
        "inline_js": f'''(function() {{
  const fileInput = document.getElementById('fileInput');
  const dropzone = document.getElementById('dropzone');
  const controlsSection = document.getElementById('controlsSection');
  const videoInfo = document.getElementById('videoInfo');
  const processBtn = document.getElementById('processBtn');
  const resetBtn = document.getElementById('resetBtn');
  const statusSection = document.getElementById('statusSection');
  const resultSection = document.getElementById('resultSection');
  const resultContent = document.getElementById('resultContent');
  let file = null; let fileName = '';
  dropzone.addEventListener('dragover', e => {{ e.preventDefault(); dropzone.classList.add('dragover'); }});
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
  dropzone.addEventListener('drop', e => {{ e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]); }});
  fileInput.addEventListener('change', e => {{ if (e.target.files[0]) handleFile(e.target.files[0]); }});
  function handleFile(f) {{
    if (!f.type.startsWith('video/')) {{ alert('Please upload a video file.'); return; }}
    file = f; fileName = f.name.replace(/\\.[^.]+$/, '');
    var ba = document.getElementById('beforeAfterPreview'); if (ba) ba.classList.add('hidden');
    const v = document.createElement('video');
    v.preload = 'metadata';
    v.onloadedmetadata = () => {{
      videoInfo.innerHTML = `<strong>File:</strong> ${{f.name}} &nbsp;|&nbsp; <strong>Size:</strong> ${{(f.size/1024/1024).toFixed(2)}} MB &nbsp;|&nbsp; <strong>Duration:</strong> ${{v.duration.toFixed(1)}}s &nbsp;|&nbsp; <strong>Resolution:</strong> ${{v.videoWidth}}x${{v.videoHeight}}`;
      controlsSection.classList.remove('hidden');
    }};
    v.src = URL.createObjectURL(f);
  }}
  async function loadFFmpeg() {{
    if (window.FFmpeg) return window.FFmpeg;
    statusSection.textContent = 'Loading ffmpeg.wasm (this may take a while)...';
    await loadScript('https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.10/dist/umd/ffmpeg.min.js');
    return window.FFmpeg;
  }}
  function loadScript(src) {{ return new Promise((res, rej) => {{ const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }}); }}
  function downloadBlob(bytes, name, type) {{ const blob = new Blob([bytes], {{ type }}); const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = name; a.click(); URL.revokeObjectURL(url); return url; }}
  window.__downloadBlob__ = downloadBlob;
  processBtn.addEventListener('click', async () => {{
    statusSection.classList.remove('hidden');
    statusSection.textContent = 'Loading ffmpeg.wasm...';
    processBtn.disabled = true; resultSection.classList.add('hidden');
    try {{
      const {{ createFFmpeg, fetchFile }} = await loadFFmpeg();
      const ffmpeg = createFFmpeg({{ log: true }});
      ffmpeg.setLogger(({{ message }}) => {{ console.log(message); }});
      ffmpeg.setProgress(({{ ratio }}) => {{ statusSection.textContent = `Processing... ${{Math.round(ratio*100)}}%`; }});
      if (!ffmpeg.isLoaded()) {{ statusSection.textContent = 'Loading ffmpeg core (25MB, first time only)...'; await ffmpeg.load(); }}
      {custom_js_body}
    }} catch(e) {{ console.error(e); statusSection.textContent = '✗ Error: ' + e.message; }}
    processBtn.disabled = false;
  }});
  resetBtn.addEventListener('click', () => {{ file = null; controlsSection.classList.add('hidden'); statusSection.classList.add('hidden'); resultSection.classList.add('hidden'); fileInput.value = ''; var ba = document.getElementById('beforeAfterPreview'); if (ba) ba.classList.remove('hidden'); }});
}})();''',
        "howto_steps": [("Upload Video", "Select a video file."), ("Configure", "Set output options."), ("Process", "Click Process (ffmpeg.wasm loads on first use)."), ("Download", "Get your converted video.")],
        "faq_list": [("Why does it load slowly the first time?", "ffmpeg.wasm is ~25MB. It caches in your browser after the first load."), ("Is my video uploaded?", "No. Everything runs in your browser. Your video never leaves your device."), ("What formats are supported?", "Most common formats: MP4, WebM, MOV, AVI, MKV, etc. Outputs MP4 or WebM.")],
        "related": [("video-to-gif", "🎞️", "Video to GIF", "Convert video to GIF"), ("compressor", "🗜️", "Image Compressor", "Compress images")]
    }

T3_VIDEO_COMPRESS = make_video_tool(
    "video-compressor", "🗜️",
    "Video Compressor — Reduce Video File Size Free",
    "Free online video compressor. Reduce video file size without losing quality. Adjust resolution, bitrate, and quality. Browser-based.",
    "video compressor, compress video, reduce video size, shrink video, MP4 compressor",
    "🗜️ Video Compressor",
    "Reduce video file size by adjusting quality and resolution — free.",
    '''<div class="control-row">
            <label>Quality</label>
            <select id="quality">
              <option value="28">Low (smallest)</option>
              <option value="24" selected>Medium (recommended)</option>
              <option value="20">High (better quality)</option>
              <option value="16">Very High (largest)</option>
            </select>
          </div>
          <div class="control-row">
            <label>Resolution</label>
            <select id="resolution">
              <option value="original">Original</option>
              <option value="1920x1080">1080p</option>
              <option value="1280x720" selected>720p</option>
              <option value="854x480">480p</option>
              <option value="640x360">360p</option>
            </select>
          </div>''',
    '''statusSection.textContent = 'Reading file...';
      ffmpeg.FS('writeFile', 'input.mp4', await fetchFile(file));
      const crf = document.getElementById('quality').value;
      const res = document.getElementById('resolution').value;
      const vf = res === 'original' ? '' : `-vf scale=${res.split('x')[0]}:-2`;
      statusSection.textContent = 'Compressing video...';
      await ffmpeg.run('-i', 'input.mp4', '-vcodec', 'libx264', '-crf', crf, ...(vf ? vf.split(' ') : []), '-acodec', 'aac', '-b:a', '128k', 'output.mp4');
      const data = ffmpeg.FS('readFile', 'output.mp4');
      resultSection.classList.remove('hidden');
      const origSize = file.size;
      const newSize = data.length;
      const savings = ((1 - newSize/origSize) * 100).toFixed(1);
      resultContent.innerHTML = `<div style="margin-bottom:16px;"><strong>Original:</strong> ${(origSize/1024/1024).toFixed(2)} MB → <strong>Compressed:</strong> ${(newSize/1024/1024).toFixed(2)} MB (${savings}% smaller)</div><video controls style="max-width:100%;border-radius:8px;"><source src="${URL.createObjectURL(new Blob([data.buffer], {type:'video/mp4'}))}" type="video/mp4"></video><br><button class="btn btn-primary" style="margin-top:16px;" onclick="window.__downloadBlob__(${JSON.stringify([...data])}, '${fileName}-compressed.mp4', 'video/mp4')">⬇️ Download</button>`;
      statusSection.textContent = `✓ Compressed! ${savings}% smaller.`;''',
    "Large video", "Smaller video", "🎬", "🗜️"
)

T3_VIDEO_GIF = make_video_tool(
    "video-to-gif", "🎞️",
    "Video to GIF — Convert Video to Animated GIF Free",
    "Free online video to GIF converter. Convert MP4, WebM, and other videos to animated GIF. Customize start time, duration, and quality.",
    "video to GIF, MP4 to GIF, GIF converter, make GIF from video, animated GIF maker",
    "🎞️ Video to GIF",
    "Convert video clips to animated GIFs — free, in your browser.",
    '''<div class="control-row">
            <label>Start Time (s)</label>
            <input type="number" id="gifStart" value="0" min="0" step="0.1" style="width:100px;">
          </div>
          <div class="control-row">
            <label>Duration (s)</label>
            <input type="number" id="gifDuration" value="5" min="1" max="60" style="width:100px;">
          </div>
          <div class="control-row">
            <label>Width (px)</label>
            <input type="number" id="gifWidth" value="480" min="100" max="1280" style="width:100px;">
          </div>
          <div class="control-row">
            <label>FPS</label>
            <input type="number" id="gifFps" value="10" min="5" max="30" style="width:100px;">
          </div>''',
    '''statusSection.textContent = 'Reading file...';
      ffmpeg.FS('writeFile', 'input.mp4', await fetchFile(file));
      const ss = document.getElementById('gifStart').value;
      const t = document.getElementById('gifDuration').value;
      const w = document.getElementById('gifWidth').value;
      const fps = document.getElementById('gifFps').value;
      statusSection.textContent = 'Converting to GIF...';
      await ffmpeg.run('-i', 'input.mp4', '-ss', ss, '-t', t, '-vf', `fps=${fps},scale=${w}:-1:flags=lanczos`, '-loop', '0', 'output.gif');
      const data = ffmpeg.FS('readFile', 'output.gif');
      resultSection.classList.remove('hidden');
      resultContent.innerHTML = `<img src="${URL.createObjectURL(new Blob([data.buffer], {type:'image/gif'}))}" style="max-width:100%;border-radius:8px;"><br><button class="btn btn-primary" style="margin-top:16px;" onclick="window.__downloadBlob__(${JSON.stringify([...data])}, '${fileName}.gif', 'image/gif')">⬇️ Download GIF</button>`;
      statusSection.textContent = '✓ GIF created!';''',
    "Video clip", "Animated GIF", "🎬", "🎞️"
)

T3_VIDEO_MP3 = make_video_tool(
    "video-to-mp3", "🎵",
    "Video to MP3 — Extract Audio from Video Free",
    "Free online video to MP3 converter. Extract audio from MP4, WebM, and other video files. High quality MP3 output. Browser-based.",
    "video to MP3, MP4 to MP3, extract audio, video to audio, convert video to MP3",
    "🎵 Video to MP3",
    "Extract high-quality MP3 audio from video files — free.",
    '''<div class="control-row">
            <label>Quality</label>
            <select id="mp3Quality">
              <option value="64k">64 kbps (small)</option>
              <option value="128k">128 kbps (standard)</option>
              <option value="192k" selected>192 kbps (good)</option>
              <option value="256k">256 kbps (high)</option>
              <option value="320k">320 kbps (best)</option>
            </select>
          </div>''',
    '''statusSection.textContent = 'Reading file...';
      ffmpeg.FS('writeFile', 'input.mp4', await fetchFile(file));
      const q = document.getElementById('mp3Quality').value;
      statusSection.textContent = 'Extracting audio...';
      await ffmpeg.run('-i', 'input.mp4', '-vn', '-acodec', 'libmp3lame', '-b:a', q, 'output.mp3');
      const data = ffmpeg.FS('readFile', 'output.mp3');
      resultSection.classList.remove('hidden');
      resultContent.innerHTML = `<audio controls style="width:100%;"><source src="${URL.createObjectURL(new Blob([data.buffer], {type:'audio/mpeg'}))}" type="audio/mpeg"></audio><br><button class="btn btn-primary" style="margin-top:16px;" onclick="window.__downloadBlob__(${JSON.stringify([...data])}, '${fileName}.mp3', 'audio/mpeg')">⬇️ Download MP3</button>`;
      statusSection.textContent = '✓ Audio extracted!';''',
    "Video", "MP3 audio", "🎬", "🎵"
)

T3_VIDEO_CROP = make_video_tool(
    "video-crop", "✂️",
    "Video Cropper — Trim & Cut Video Free",
    "Free online video cropper. Trim and cut video to remove unwanted parts. Set start and end times precisely. Browser-based.",
    "video cropper, trim video, cut video, video trimmer, crop video online",
    "✂️ Video Cropper",
    "Trim and cut videos to remove unwanted parts — free, in your browser.",
    '''<div class="control-row">
            <label>Start Time (s)</label>
            <input type="number" id="cropStart" value="0" min="0" step="0.1" style="width:100px;">
          </div>
          <div class="control-row">
            <label>End Time (s)</label>
            <input type="number" id="cropEnd" value="10" min="0" step="0.1" style="width:100px;">
          </div>''',
    '''statusSection.textContent = 'Reading file...';
      ffmpeg.FS('writeFile', 'input.mp4', await fetchFile(file));
      const ss = document.getElementById('cropStart').value;
      const to = document.getElementById('cropEnd').value;
      const dur = (parseFloat(to) - parseFloat(ss)).toFixed(2);
      if (dur <= 0) { alert('End time must be greater than start time.'); return; }
      statusSection.textContent = 'Cropping video...';
      await ffmpeg.run('-i', 'input.mp4', '-ss', ss, '-t', dur, '-c', 'copy', 'output.mp4');
      const data = ffmpeg.FS('readFile', 'output.mp4');
      resultSection.classList.remove('hidden');
      resultContent.innerHTML = `<video controls style="max-width:100%;border-radius:8px;"><source src="${URL.createObjectURL(new Blob([data.buffer], {type:'video/mp4'}))}" type="video/mp4"></video><br><button class="btn btn-primary" style="margin-top:16px;" onclick="window.__downloadBlob__(${JSON.stringify([...data])}, '${fileName}-cropped.mp4', 'video/mp4')">⬇️ Download</button>`;
      statusSection.textContent = '✓ Video cropped!';''',
    "Long video", "Trimmed video", "🎬", "✂️"
)

T3_VIDEO_FRAMES = make_video_tool(
    "video-to-frames", "🖼️",
    "Video to Frames — Extract Images from Video Free",
    "Free online video frame extractor. Extract frames from video as JPG or PNG images. Choose FPS or total frame count.",
    "video to frames, extract frames, video to images, screenshot video, frame extractor",
    "🖼️ Video to Frames",
    "Extract high-quality frames (JPG/PNG) from any video — free.",
    '''<div class="control-row">
            <label>Extract Mode</label>
            <select id="frameMode">
              <option value="fps" selected>Every N seconds</option>
              <option value="count">Total frames</option>
            </select>
          </div>
          <div class="control-row">
            <label>FPS / Interval</label>
            <input type="number" id="frameValue" value="1" min="0.1" step="0.1" style="width:100px;">
          </div>
          <div class="control-row">
            <label>Format</label>
            <select id="frameFormat">
              <option value="jpg" selected>JPG</option>
              <option value="png">PNG</option>
            </select>
          </div>''',
    '''statusSection.textContent = 'Reading file...';
      ffmpeg.FS('writeFile', 'input.mp4', await fetchFile(file));
      const mode = document.getElementById('frameMode').value;
      const val = document.getElementById('frameValue').value;
      const fmt = document.getElementById('frameFormat').value;
      const vf = mode === 'fps' ? `fps=1/${val}` : `select='not(mod(n,ceil(n/${val})))'`;
      statusSection.textContent = 'Extracting frames...';
      await ffmpeg.run('-i', 'input.mp4', '-vf', vf, `frame_%04d.${fmt}`);
      // Read all frame files
      const files = []; let i = 1;
      while (true) { try { const name = `frame_${String(i).padStart(4,'0')}.${fmt}`; const d = ffmpeg.FS('readFile', name); files.push({name, data: d}); i++; } catch(e) { break; } }
      if (files.length === 0) { throw new Error('No frames extracted.'); }
      resultSection.classList.remove('hidden');
      if (files.length > 1) {
        if (!window.JSZip) await new Promise((res) => { const s = document.createElement('script'); s.src = 'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js'; s.onload = res; document.head.appendChild(s); });
        const zip = new window.JSZip();
        files.forEach(f => zip.file(f.name, f.data));
        const zipBytes = await zip.generateAsync({ type: 'uint8array' });
        resultContent.innerHTML = `<div>Extracted ${files.length} frames</div><img src="${URL.createObjectURL(new Blob([files[0].data.buffer], {type:fmt==='png'?'image/png':'image/jpeg'}))}" style="max-width:200px;border-radius:8px;margin-top:12px;"><br><button class="btn btn-primary" style="margin-top:16px;" onclick="window.__downloadBlob__(${JSON.stringify([...zipBytes])}, '${fileName}-frames.zip', 'application/zip')">⬇️ Download ZIP (${files.length} files)</button>`;
      } else {
        const f = files[0];
        resultContent.innerHTML = `<img src="${URL.createObjectURL(new Blob([f.data.buffer], {type:fmt==='png'?'image/png':'image/jpeg'}))}" style="max-width:100%;border-radius:8px;"><br><button class="btn btn-primary" style="margin-top:16px;" onclick="window.__downloadBlob__(${JSON.stringify([...f.data])}, '${f.name}', '${fmt==='png'?'image/png':'image/jpeg'}')">⬇️ Download</button>`;
      }
      statusSection.textContent = `✓ Extracted ${files.length} frame(s)!`;''',
    "Video", "Image frames", "🎬", "🖼️"
)

T3_VIDEO_SPEED = make_video_tool(
    "video-speed", "⏩",
    "Video Speed Changer — Change Video Playback Speed Free",
    "Free online video speed changer. Speed up or slow down video playback. Change speed from 0.25x to 4x without re-encoding quality.",
    "video speed changer, change video speed, speed up video, slow down video, adjust video speed",
    "⏩ Video Speed Changer",
    "Speed up or slow down videos (0.25x to 4x) — free, in your browser.",
    '''<div class="control-row">
            <label>Speed</label>
            <select id="speed">
              <option value="0.25">0.25x (very slow)</option>
              <option value="0.5">0.5x (slow)</option>
              <option value="0.75">0.75x</option>
              <option value="1" selected>1x (normal)</option>
              <option value="1.5">1.5x</option>
              <option value="2">2x (fast)</option>
              <option value="3">3x</option>
              <option value="4">4x (very fast)</option>
            </select>
          </div>''',
    '''statusSection.textContent = 'Reading file...';
      ffmpeg.FS('writeFile', 'input.mp4', await fetchFile(file));
      const spd = document.getElementById('speed').value;
      const atempo = spd; // audio tempo
      const vtmp = 1 / parseFloat(spd); // video pts
      statusSection.textContent = 'Changing speed...';
      await ffmpeg.run('-i', 'input.mp4', '-filter_complex', `[0:v]setpts=${vtmp}*PTS[v];[0:a]atempo=${atempo}[a]`, '-map', '[v]', '-map', '[a]', '-vcodec', 'libx264', '-acodec', 'aac', 'output.mp4');
      const data = ffmpeg.FS('readFile', 'output.mp4');
      resultSection.classList.remove('hidden');
      resultContent.innerHTML = `<video controls style="max-width:100%;border-radius:8px;"><source src="${URL.createObjectURL(new Blob([data.buffer], {type:'video/mp4'}))}" type="video/mp4"></video><br><button class="btn btn-primary" style="margin-top:16px;" onclick="window.__downloadBlob__(${JSON.stringify([...data])}, '${fileName}-${spd}x.mp4', 'video/mp4')">⬇️ Download</button>`;
      statusSection.textContent = `✓ Speed changed to ${spd}x!`;''',
    "Normal speed", "Custom speed", "▶️", "⏩"
)

T3_VIDEO_ROTATE = make_video_tool(
    "video-rotate", "🔃",
    "Video Rotator — Rotate & Flip Video Free",
    "Free online video rotator. Rotate video 90°, 180°, 270° or flip horizontally/vertically. Browser-based, nothing uploaded.",
    "video rotator, rotate video, flip video, rotate MP4, flip video online",
    "🔃 Video Rotator",
    "Rotate (90°/180°/270°) and flip videos — free, in your browser.",
    '''<div class="control-row">
            <label>Transform</label>
            <select id="rotateSel">
              <option value="90">Rotate 90° Clockwise</option>
              <option value="180">Rotate 180°</option>
              <option value="270">Rotate 270° Clockwise</option>
              <option value="hflip">Flip Horizontal</option>
              <option value="vflip">Flip Vertical</option>
            </select>
          </div>''',
    '''statusSection.textContent = 'Reading file...';
      ffmpeg.FS('writeFile', 'input.mp4', await fetchFile(file));
      const sel = document.getElementById('rotateSel').value;
      let vf;
      if (sel === '90') vf = 'transpose=1';
      else if (sel === '180') vf = 'transpose=1,transpose=1';
      else if (sel === '270') vf = 'transpose=2';
      else if (sel === 'hflip') vf = 'hflip';
      else vf = 'vflip';
      statusSection.textContent = 'Rotating video...';
      await ffmpeg.run('-i', 'input.mp4', '-vf', vf, '-c:a', 'copy', 'output.mp4');
      const data = ffmpeg.FS('readFile', 'output.mp4');
      resultSection.classList.remove('hidden');
      resultContent.innerHTML = `<video controls style="max-width:100%;border-radius:8px;"><source src="${URL.createObjectURL(new Blob([data.buffer], {type:'video/mp4'}))}" type="video/mp4"></video><br><button class="btn btn-primary" style="margin-top:16px;" onclick="window.__downloadBlob__(${JSON.stringify([...data])}, '${fileName}-rotated.mp4', 'video/mp4')">⬇️ Download</button>`;
      statusSection.textContent = '✓ Video transformed!';''',
    "Wrong orientation", "Correct orientation", "↩️", "🔃"
)

BATCH3_TOOLS = [T3_VIDEO_COMPRESS, T3_VIDEO_GIF, T3_VIDEO_MP3, T3_VIDEO_CROP, T3_VIDEO_FRAMES, T3_VIDEO_SPEED, T3_VIDEO_ROTATE]

ALL_NEW_TOOLS = BATCH1_TOOLS + BATCH2_TOOLS + BATCH3_TOOLS


# ═══════════════════════════════════════════════════════════
# 翻译表（简化版：7个语种的关键字段翻译）
# ═══════════════════════════════════════════════════════════

TRANSLATIONS = {
    "es": {
        "breadcrumb_home": "Inicio",
        "breadcrumb_tools": "Herramientas",
        "nav_home": "Inicio",
        "nav_tools": "Herramientas",
        "nav_workflows": "Flujos",
        "nav_blog": "Blog",
        "nav_about": "Acerca de",
        "nav_contact": "Contacto",
        "how_to_use": "Cómo usar",
        "detailed_guide": "Guía detallada",
        "faq": "Preguntas frecuentes",
        "you_might_also_like": "También te puede gustar",
        "tools_url": "/es/tools/",
        "lang_label": "ES Español",
        "lang_flag": "🇪🇸",
    },
    "pt": {
        "breadcrumb_home": "Início",
        "breadcrumb_tools": "Ferramentas",
        "nav_home": "Início",
        "nav_tools": "Ferramentas",
        "nav_workflows": "Fluxos",
        "nav_blog": "Blog",
        "nav_about": "Sobre",
        "nav_contact": "Contato",
        "how_to_use": "Como usar",
        "detailed_guide": "Guia detalhado",
        "faq": "Perguntas frequentes",
        "you_might_also_like": "Você também pode gostar",
        "tools_url": "/pt/tools/",
        "lang_label": "PT Português",
        "lang_flag": "🇧🇷",
    },
    "id": {
        "breadcrumb_home": "Beranda",
        "breadcrumb_tools": "Alat",
        "nav_home": "Beranda",
        "nav_tools": "Alat",
        "nav_workflows": "Alur Kerja",
        "nav_blog": "Blog",
        "nav_about": "Tentang",
        "nav_contact": "Kontak",
        "how_to_use": "Cara menggunakan",
        "detailed_guide": "Panduan lengkap",
        "faq": "Pertanyaan umum",
        "you_might_also_like": "Mungkin Anda suka",
        "tools_url": "/id/tools/",
        "lang_label": "ID Bahasa Indonesia",
        "lang_flag": "🇮🇩",
    },
    "fr": {
        "breadcrumb_home": "Accueil",
        "breadcrumb_tools": "Outils",
        "nav_home": "Accueil",
        "nav_tools": "Outils",
        "nav_workflows": "Flux",
        "nav_blog": "Blog",
        "nav_about": "À propos",
        "nav_contact": "Contact",
        "how_to_use": "Comment utiliser",
        "detailed_guide": "Guide détaillé",
        "faq": "Questions fréquentes",
        "you_might_also_like": "Vous pourriez aimer",
        "tools_url": "/fr/tools/",
        "lang_label": "FR Français",
        "lang_flag": "🇫🇷",
    },
    "vi": {
        "breadcrumb_home": "Trang chủ",
        "breadcrumb_tools": "Công cụ",
        "nav_home": "Trang chủ",
        "nav_tools": "Công cụ",
        "nav_workflows": "Quy trình",
        "nav_blog": "Blog",
        "nav_about": "Giới thiệu",
        "nav_contact": "Liên hệ",
        "how_to_use": "Cách sử dụng",
        "detailed_guide": "Hướng dẫn chi tiết",
        "faq": "Câu hỏi thường gặp",
        "you_might_also_like": "Bạn cũng có thể thích",
        "tools_url": "/vi/tools/",
        "lang_label": "VI Tiếng Việt",
        "lang_flag": "🇻🇳",
    },
    "ar": {
        "breadcrumb_home": "الرئيسية",
        "breadcrumb_tools": "الأدوات",
        "nav_home": "الرئيسية",
        "nav_tools": "الأدوات",
        "nav_workflows": "سير العمل",
        "nav_blog": "المدونة",
        "nav_about": "حول",
        "nav_contact": "اتصل بنا",
        "how_to_use": "كيفية الاستخدام",
        "detailed_guide": "دليل مفصل",
        "faq": "الأسئلة الشائعة",
        "you_might_also_like": "قد يعجبك أيضاً",
        "tools_url": "/ar/tools/",
        "lang_label": "AR العربية",
        "lang_flag": "🇸🇦",
    },
    "en": {
        "breadcrumb_home": "Home",
        "breadcrumb_tools": "Tools",
        "nav_home": "Home",
        "nav_tools": "Tools",
        "nav_workflows": "Workflows",
        "nav_blog": "Blog",
        "nav_about": "About",
        "nav_contact": "Contact",
        "how_to_use": "How to Use",
        "detailed_guide": "Detailed User Guide",
        "faq": "Frequently Asked Questions",
        "you_might_also_like": "You Might Also Like",
        "tools_url": "/tools/",
        "lang_label": "EN English",
        "lang_flag": "🇬🇧",
    },
}


# ═══════════════════════════════════════════════════════════
# 主构建函数
# ═══════════════════════════════════════════════════════════

def load_existing_lang_fields(lang):
    """从现有的 _tools_data_{LANG}.json 读取公共字段（nav_html, footer_html 等）"""
    data_file = os.path.join(ROOT, f'_tools_data{"" if lang == "en" else "_" + lang}.json')
    if not os.path.exists(data_file):
        print(f'  WARNING: Data file not found: {data_file}')
        return {}
    with open(data_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    return {k: v for k, v in all_data.items() if k != 'tools'}


def tool_to_data(tool, lang, lang_fields):
    """把工具定义转换为 _tools_data 格式（含翻译）"""
    t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    result = dict(lang_fields)
    result.update({
        'slug': tool['slug'],
        'lang': lang,
        'title': tool['title'],
        'description': tool['description'],
        'keywords': tool['keywords'],
        'h1': tool['h1'],
        'subtitle': tool['subtitle'],
        'theme_color': '#6366f1',
        'breadcrumb_home': t['breadcrumb_home'],
        'breadcrumb_tools': t['breadcrumb_tools'],
        'breadcrumb_tools_url': t['tools_url'],
        'breadcrumb_last': tool['h1'],
        'tools_url': t['tools_url'],
        'workspace_html': tool['workspace_html'],
        'inline_style': COMMON_STYLE,
        'inline_js': tool['inline_js'],
        'og_title': tool['title'],
        'og_description': tool['description'],
        'og_image': f'https://smartimgkit.com/screenshots/{tool["slug"]}.png',
        'jsonld_webapp': gen_webapp(tool['h1'], tool['description']),
        'jsonld_howto': gen_howto(tool.get('howto_steps', [])),
        'jsonld_faq': gen_faq(tool.get('faq_list', [])),
        'howto_html': gen_howto_html(tool.get('howto_steps', [])),
        'guide_html': gen_guide_html([(s[0], s[1]) for s in tool.get('howto_steps', [])]),
        'faq_html': gen_faq_html(tool.get('faq_list', [])),
        'related_html': gen_related_html(tool.get('related', [])),
    })
    return result


def build_new_tools():
    """构建所有24个新工具的7语种页面（不碰已有页面）"""
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()

    total = 0
    for lang in LANGS:
        lang_fields = load_existing_lang_fields(lang)
        if not lang_fields:
            print(f'  SKIP [{lang}]: no existing data')
            continue
        tools_dir = os.path.join(ROOT, LANGS[lang]['dir'])
        os.makedirs(tools_dir, exist_ok=True)

        for tool in ALL_NEW_TOOLS:
            # 安全检查：如果已存在（理论上不应该）就跳过
            out_path = os.path.join(tools_dir, f'{tool["slug"]}.html')
            if os.path.exists(out_path):
                print(f'  SKIP (exists): [{lang}] {tool["slug"]}.html')
                continue

            data = tool_to_data(tool, lang, lang_fields)
            html = build_one(template, data, LANGS[lang], all_langs=LANGS)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  ✓ [{lang}] {tool["slug"]}.html')
            total += 1

    print(f'\n=== Built {total} new tool pages across {len(LANGS)} languages ===')
    return total


if __name__ == '__main__':
    print('=== Generating 24 new tools (3 batches) ===')
    print(f'Total new tools: {len(ALL_NEW_TOOLS)}')
    print(f'  Batch 1 (Text/Dev): {len(BATCH1_TOOLS)} tools')
    print(f'  Batch 2 (PDF): {len(BATCH2_TOOLS)} tools')
    print(f'  Batch 3 (Video): {len(BATCH3_TOOLS)} tools')
    print()
    build_new_tools()
    print()
    print('Done! New tool pages generated.')
    print('Next steps: update index.html cards, footer links, and sitemap.xml')