# Task for Claude Code: full update of The Practice Exchange (SEO refresh, Disability History Month post, guest posts by Conor Govey and Michelle Woodward)

Repository: `practice-exchange` (GitHub, branch `main`). This folder is the COMPLETE repository content and supersedes every earlier package.

## Steps
1. `cd` into the local clone of `practice-exchange` and run `git pull`.
2. Copy everything from this folder into the repo, overwriting existing files (do NOT copy this task file):
   `build.py`, `README.md`, `.gitignore`, `.github/workflows/publish.yml`, all of `posts/`, all of `static/`.
3. Remove the old example files, which are no longer used:
   `git rm -f --ignore-unmatch posts/_example-with-pictures.md.txt static/images/example-small-steps.jpg`
4. Check the build:
   `pip install markdown && PX_TODAY=2026-11-30 python build.py` → expect "built 13 of 13 posts".
   `grep -rl '\.html"' dist --include=index.html` → should print nothing. Then delete `dist/`.
5. Commit and push:
   ```
   git add -A
   git commit -m "SEO refresh (clean URLs, Solutions menu, BlogPosting schema, search titles) and guest posts: The December wobble (Conor Govey), Securing Section F (Michelle Woodward); Disability History Month"
   git push
   ```
6. Confirm the "Publish The Practice Exchange" GitHub Action succeeds (two green ticks).

Publishing schedule (posts go live automatically at about 6am on their date):
- Thu 22 Oct — Persistent and severe absence (live)
- Wed 28 Oct — The graduated approach (live)
- Sat 31 Oct — Your Pupil Premium strategy statement (live)
- Mon 2 Nov — GUEST: Regulation starts with us, Victoria Willis (live)
- Thu 5 Nov — Sharing information safely (live)
- Mon 9 Nov — Reducing SENCO workload
- Tue 10 Nov — Beyond the assembly: marking Disability History Month (with the UKDHM 2026 graphic as its cover)
- Thu 12 Nov — GUEST: The December wobble, Conor Govey
- Mon 16 Nov — How ASEND360 helps you track EHCP outcomes
- Thu 19 Nov — Behaviour isn't a barrier: it's a signal
- Mon 23 Nov — GUEST: Securing Section F in the classroom, Michelle Woodward
- Thu 26 Nov — Preparing for Ofsted
- Mon 30 Nov — Small steps are still steps
