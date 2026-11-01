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

## Guest posts

Add these lines to the post's header to credit a guest author:

```
guest: yes
author: Victoria Willis
author_role: Teaching Assistant and founder of The Calm Coach
author_photo: /practice-exchange/images/victoria-willis-avatar.jpg
author_bio: One or two sentences about the author.
author_url: https://www.calm-coach.com
author_url_label: calm-coach.com
```

The card shows "Guest spot · Name", the article shows the author's name and photo in the
byline and an "About the author" box at the end. Use a square photo for `author_photo`.
`image_position: 50% 22%` moves the focus of a cover photo (e.g. to keep a face in view).

## Add pictures

**Upload the picture:** in GitHub open `static/images`, choose **Add file → Upload files**,
drag the picture in and commit. Use a short name with no spaces, e.g. `visual-timetable.jpg`.

**Cover picture** (shown on the card and at the top of the article) — add two lines to the
post's header:

```
image: /practice-exchange/images/visual-timetable.jpg
image_alt: A visual timetable on a classroom wall
```

Without these lines the post uses the automatic brand illustration.

**Picture inside the article** — put this on its own line where you want it:

```
![A visual timetable on a classroom wall](/practice-exchange/images/visual-timetable.jpg "Optional caption")
```

Tips:
- Landscape pictures work best. Cover pictures are cropped to roughly 16:7 on cards, 3:1 on the article.
- Aim for about 1600 pixels wide and under 300 KB (JPG or WebP). Squoosh.app shrinks files for free.
- Always write the description (alt text) — it is read aloud to people using screen readers.
- Only use pictures you have the rights to. Never use photos of pupils without written consent
  for this specific use; photos of resources, classrooms (empty) or staff with permission are safer.

See `posts/_example-with-pictures.md.txt` for a full example.

## Preview locally (optional)

```
pip install markdown
python build.py --preview   # includes scheduled posts, marked "Scheduled"
```

Open `dist/index.html` through any local web server mounted at `/practice-exchange/`.
