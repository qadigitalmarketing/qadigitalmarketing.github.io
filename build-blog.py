#!/usr/bin/env python3
"""
Somaia Mohamed static blog builder.

Usage:
    python build-blog.py

It reads blog-data.js and generates:
    blog/<slug>/index.html

The generated article pages inherit the exact CSS/header/footer/CTA
structure from blog-post.html, but use clean folder URLs.
"""

from pathlib import Path
import re, json, html

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "blog-data.js"
TEMPLATE = ROOT / "blog-post.html"
BLOG_DIR = ROOT / "blog"

text = DATA.read_text(encoding="utf-8")
template = TEMPLATE.read_text(encoding="utf-8")

# Extract the BLOG_POSTS array by using the JS as a data file.
# This system intentionally supports the simple object format used by the
# reusable blog system: strings + a template-literal content field.
match = re.search(r"const\s+BLOG_POSTS\s*=\s*\[(.*)\]\s*;\s*$", text, re.S)
if not match:
    raise SystemExit("Could not find BLOG_POSTS in blog-data.js")

body = match.group(1)

# Split top-level objects safely, respecting strings/template literals.
objects = []
start = None
depth = 0
quote = None
escape = False
for i, ch in enumerate(body):
    if quote:
        if escape:
            escape = False
        elif ch == "\\":
            escape = True
        elif ch == quote:
            quote = None
        continue
    if ch in ("'", '"', '`'):
        quote = ch
        continue
    if ch == "{":
        if depth == 0:
            start = i
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0 and start is not None:
            objects.append(body[start:i+1])
            start = None

def get_string(obj, key):
    m = re.search(rf'{key}\s*:\s*"((?:\\.|[^"])*)"', obj, re.S)
    if not m:
        raise ValueError(f"Missing {key}")
    return json.loads('"' + m.group(1) + '"')

def get_content(obj):
    m = re.search(r'content\s*:\s*`(.*?)`\s*(?:,|\n?\})', obj, re.S)
    if not m:
        raise ValueError("Missing content")
    return m.group(1)

# Extract the reusable article shell from the current template.
# We only replace the dynamic article-loading script; the rest of the
# HTML/CSS/embedded logo/header/footer stays unchanged.
script_start = template.find('<script src="blog-data.js"></script><script>')
script_end = template.find('</script></body></html>', script_start)
if script_start == -1 or script_end == -1:
    raise SystemExit("Could not locate the article script in blog-post.html")

prefix = template[:script_start]
suffix = template[script_end + len("</script>"):]

generated = 0
for obj in objects:
    slug = get_string(obj, "slug")
    title = get_string(obj, "title")
    category = get_string(obj, "category")
    date = get_string(obj, "date")
    author = get_string(obj, "author")
    description = get_string(obj, "description")
    content = get_content(obj)

    # Basic slug safety: only URL-safe path segments.
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError(f"Invalid slug: {slug}")

    article_meta = (
        '<script>\n'
        'document.addEventListener("DOMContentLoaded",function(){\n'
        f'document.title={json.dumps(title + " | Somaia Mohamed")};\n'
        f'document.querySelector(\'meta[name="description"]\').setAttribute("content",{json.dumps(description)});\n'
        'var root=document.getElementById("article");\n'
        f'root.innerHTML={json.dumps(f"""<span class="eyebrow">{category}</span><h1>{title}</h1><p class="article-meta">By {author} · {date} · Qatar & GCC</p><p class="article-lead">{description}</p>{content}<section class="cta"><h2>Want to improve your visibility?</h2><p>I help businesses across Qatar, Saudi Arabia and the GCC with digital marketing, SEO and search-led marketing strategy.</p><div class="cta-actions"><a class="cta-wa" href="https://wa.me/201145654675" target="_blank" rel="noopener">WhatsApp Me →</a><a class="cta-li" href="https://www.linkedin.com/" target="_blank" rel="noopener">LinkedIn →</a><a class="cta-li" href="/contact.html">Contact →</a></div></section><p style="margin-top:28px"><a class="read" href="/blog.html">← Back to all articles</a></p>""")};\n'
        '});\n'
        '</script>'
    )

    out = prefix + article_meta + suffix
    out_dir = BLOG_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(out, encoding="utf-8")
    generated += 1

print(f"Generated {generated} article page(s).")
