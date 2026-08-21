SOMAIA MOHAMED — CLEAN REUSABLE BLOG SYSTEM

URL STRUCTURE
==============
Articles now use clean GitHub Pages URLs:

https://qadigitalmarketing.github.io/blog/article-slug/

Example:
https://qadigitalmarketing.github.io/blog/qatar-real-estate-marketing/

There is NO:
?slug=
and no blog-post.html in the public article URL.

FILES
=====
blog.html
    Blog listing page. It automatically creates article cards from blog-data.js.

blog-post.html
    Master article template used by build-blog.py. It is not the public article URL.

blog-data.js
    The only content file you normally edit for new posts.

build-blog.py
    Generates /blog/<slug>/index.html from blog-data.js.

ADDING A NEW ARTICLE
====================
1. Add a new object to BLOG_POSTS in blog-data.js.
2. Give it a unique lowercase hyphenated slug.
3. Run:

   python build-blog.py

4. Upload the generated /blog/<slug>/index.html folder and blog-data.js.

IMPORTANT GITHUB PAGES NOTE
===========================
GitHub Pages is static hosting. It does not execute build-blog.py on the server.

You therefore have two choices:

A) Run build-blog.py locally before each GitHub upload.
   This is the recommended simple workflow.

B) Later, add GitHub Actions to automatically run the builder whenever
   blog-data.js changes. That can make publishing even easier.

EXISTING DESIGN PRESERVED
=========================
The article pages keep the existing reusable system's:
- embedded Somaia Mohamed logo
- navy / cream / gold / beige brand colors
- responsive CSS
- animations
- header/navigation
- footer
- floating WhatsApp Contact Now button
- WhatsApp CTA
- LinkedIn CTA
- Google Search Console verification meta tag
- article typography and layout

OLD URL
=======
Old:
blog-post.html?slug=qatar-real-estate-marketing

NEW:
blog/qatar-real-estate-marketing/

The old blog-post.html remains as the master template; it is not linked publicly
by the blog cards.
