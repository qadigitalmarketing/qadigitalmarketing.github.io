#!/usr/bin/env python3
from pathlib import Path
import re, json

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"blog-data.js"
TEMPLATE=ROOT/"blog-post.html"
BLOG_DIR=ROOT/"blog"
text=DATA.read_text(encoding="utf-8")
template=TEMPLATE.read_text(encoding="utf-8")
m=re.search(r"const\s+BLOG_POSTS\s*=\s*\[(.*)\]\s*;\s*$",text,re.S)
if not m: raise SystemExit("Could not find BLOG_POSTS")
body=m.group(1)
objects=[]; start=None; depth=0; quote=None; escape=False
for i,ch in enumerate(body):
    if quote:
        if escape: escape=False
        elif ch=="\\": escape=True
        elif ch==quote: quote=None
        continue
    if ch in ("'",'"','`'): quote=ch; continue
    if ch=="{":
        if depth==0: start=i
        depth+=1
    elif ch=="}":
        depth-=1
        if depth==0 and start is not None:
            objects.append(body[start:i+1]); start=None

def get_string(obj,key):
    m=re.search(rf'{key}\s*:\s*"((?:\\.|[^"])*)"',obj,re.S)
    if not m: raise ValueError("Missing "+key)
    return bytes(m.group(1),"utf-8").decode("unicode_escape")
def get_content(obj):
    m=re.search(r'content\s*:\s*`(.*?)`\s*(?:,|\n?\})',obj,re.S)
    if not m: raise ValueError("Missing content")
    return m.group(1)

a=template.find('<script src="blog-data.js"></script><script>')
b=template.find('</script></body></html>',a)
if a<0 or b<0: raise SystemExit("Could not locate article script")
prefix=template[:a]
suffix=template[b+len("</script>"):]

for obj in objects:
    slug=get_string(obj,"slug")
    title=get_string(obj,"title")
    category=get_string(obj,"category")
    date=get_string(obj,"date")
    author=get_string(obj,"author")
    description=get_string(obj,"description")
    content=get_content(obj)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",slug):
        raise ValueError("Invalid slug: "+slug)
    article=(
        '<span class="eyebrow">'+category+'</span><h1>'+title+'</h1>'
        '<p class="article-meta">بقلم '+author+' · '+date+' · قطر والخليج</p>'
        '<p class="article-lead">'+description+'</p>'+content+
        '<section class="cta"><h2>هل تريد تحسين ظهورك؟</h2>'
        '<p>أساعد الشركات في قطر والسعودية والخليج في التسويق الرقمي وتحسين محركات البحث واستراتيجيات التسويق المعتمدة على البحث.</p>'
        '<div class="cta-actions"><a class="cta-wa" href="https://wa.me/201145654675" target="_blank" rel="noopener">تواصل معي عبر واتساب →</a>'
        '<a class="cta-li" href="https://www.linkedin.com/" target="_blank" rel="noopener">لينكدإن →</a>'
        '<a class="cta-li" href="/ar/contact.html">تواصل →</a></div></section>'
        '<p style="margin-top:28px"><a class="read" href="/ar/blog.html">← العودة إلى جميع المقالات</a></p>'
    )
    js='<script>document.addEventListener("DOMContentLoaded",function(){document.title='+json.dumps(title+" | سُميه محمد",ensure_ascii=False)+';document.querySelector(\'meta[name="description"]\').setAttribute("content",'+json.dumps(description,ensure_ascii=False)+');document.getElementById("article").innerHTML='+json.dumps(article,ensure_ascii=False)+';});</script>'
    d=BLOG_DIR/slug; d.mkdir(parents=True,exist_ok=True)
    (d/"index.html").write_text(prefix+js+suffix,encoding="utf-8")
print("Arabic blog build complete.")
