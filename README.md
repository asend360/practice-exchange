# The Practice Exchange

Free SEND and inclusion articles from ASEND360, published at
**https://asend360.co.uk/practice-exchange/**.

This repository builds the blog and publishes it to GitHub Pages. The main
website (on Netlify) shows it under `/practice-exchange/` through a proxy, so
**adding or scheduling posts never needs a Netlify deploy**.

## Add a post

1. In GitHub, open the `posts` folder and choose **Add file → Create new file**.
2. Name it after the article, e.g. `annual-review-checklist.md`.
3. Paste this at the top, then write the article in Markdown underneath:

```
---
title: Your title here
slug: annual-review-checklist
date: 2026-11-23
category: Practice
summary: One or two sentences for the card and for Google.
sources: Title of source|https://www.gov.uk/... ;; Another source|https://...
feature_title: The ASEND360 feature this links to
feature_url: /ehcp-tracking-software.html
feature_text: One sentence on how ASEND360 helps.
---
```

- **category** must be one of: `Practice`, `Policy & Compliance`, `Leadership`, `Inside ASEND360`.
- **date** controls publishing. A future date schedules the post: it goes live
  at about 6am on that day, automatically.
- Use `## Headings`, `- bullet points` and `**bold**` in the article body.
- Aim for 3–8 minute reads (about 650–1,700 words).

4. Click **Commit changes**. The site rebuilds in about a minute.

## Preview locally (optional)

```
pip install markdown
python build.py --preview   # includes scheduled posts, marked "Scheduled"
```

Open `dist/index.html` through any local web server mounted at `/practice-exchange/`.
