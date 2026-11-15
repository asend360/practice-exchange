<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:atom="http://www.w3.org/2005/Atom">
<xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>
<xsl:template match="/">
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="robots" content="noindex"/>
<title>RSS feed · The Practice Exchange · ASEND360</title>
<style>
:root{--navy:#003574;--text:#1B2333;--muted:#5A6478;--line:#DDE2EA;--bg:#F3F5F8;--link:#0369A8;--teal:#0B7A75;--tint:#E3F5F3}
*{box-sizing:border-box}
body{margin:0;font-family:Inter,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;color:var(--text);background:var(--bg);line-height:1.55}
.bar{height:6px;background:linear-gradient(90deg,#0381CA 0%,#08ACAC 50%,#40CD70 100%)}
header{background:var(--navy);color:#fff;padding:40px 16px 44px}
.wrap{max-width:820px;margin:0 auto;padding:0 16px}
.eyebrow{margin:0 0 8px;font-size:.78rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#8FE3D6}
h1{margin:0;font-size:2rem;line-height:1.15;letter-spacing:-.02em}
header p.lede{margin:10px 0 0;color:#D9E4F2;max-width:60ch}
.note{margin:-24px auto 0;background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 22px;box-shadow:0 10px 30px -18px rgba(0,53,116,.45)}
.note h2{margin:0 0 6px;font-size:1.05rem;color:var(--navy)}
.note p{margin:0 0 10px;font-size:.95rem}
.copy{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:6px}
code{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:.88rem;word-break:break-all}
.home{display:inline-block;margin-top:4px;font-weight:600;color:var(--link)}
main{padding:28px 0 56px}
h2.list{font-size:1.2rem;color:var(--navy);margin:8px 0 14px}
.item{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin-bottom:12px;text-decoration:none;color:inherit}
.item:hover,.item:focus-visible{border-color:#0381CA}
.item:focus-visible{outline:3px solid #0381CA;outline-offset:2px}
.meta{display:flex;gap:10px;align-items:center;font-size:.82rem;color:var(--muted);margin-bottom:6px}
.tag{background:var(--tint);color:var(--teal);font-weight:700;font-size:.7rem;letter-spacing:.05em;text-transform:uppercase;padding:2px 8px;border-radius:999px}
.item h3{margin:0 0 6px;font-size:1.08rem;color:var(--navy);line-height:1.3}
.item p{margin:0;font-size:.94rem;color:var(--muted)}
footer{font-size:.82rem;color:var(--muted);text-align:center;padding:0 16px 40px}
</style>
</head>
<body>
<div class="bar"></div>
<header><div class="wrap">
<p class="eyebrow">RSS feed</p>
<h1><xsl:value-of select="rss/channel/title"/></h1>
<p class="lede"><xsl:value-of select="rss/channel/description"/>. New articles appear here as soon as they're published.</p>
</div></header>
<div class="wrap">
<div class="note">
<h2>What is this page?</h2>
<p>This is an RSS feed. Copy the address below into a feed reader such as Feedly or Inoreader, or into your newsletter tool, and new articles from The Practice Exchange will reach you automatically.</p>
<div class="copy"><code><xsl:value-of select="rss/channel/atom:link/@href"/></code></div>
<p style="margin-top:12px"><a class="home" href="{rss/channel/link}">Go to The Practice Exchange →</a></p>
</div>
</div>
<main class="wrap">
<h2 class="list">Latest articles</h2>
<xsl:for-each select="rss/channel/item">
<a class="item" href="{link}">
<div class="meta"><span class="tag"><xsl:value-of select="category"/></span><span><xsl:value-of select="substring(pubDate,6,11)"/></span></div>
<h3><xsl:value-of select="title"/></h3>
<p><xsl:value-of select="description"/></p>
</a>
</xsl:for-each>
</main>
<footer>© ASEND360 Limited · <a href="https://asend360.co.uk/" style="color:inherit">asend360.co.uk</a></footer>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
