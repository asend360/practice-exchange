# Task for Claude Code: update The Practice Exchange (new article, 18 illustrations, branded RSS page)

This folder is the COMPLETE blog repository. It does NOT include the email sign-up (on hold).
If a review finds sign-up code (notify.py, a "sub-form", an "Email subscribers" workflow step), stop and ask Sean.

## Steps
1. `cd` into the local clone of `practice-exchange`, `git pull`.
2. Copy everything from this folder into the repo, overwriting (not this task file).
3. `git rm -f --ignore-unmatch posts/_example-with-pictures.md.txt static/images/example-small-steps.jpg notify.py`
4. Check: `pip install markdown && PX_TODAY=2026-11-30 python build.py` → "built 14 of 14 posts". Delete `dist/`.
5. Commit and push:
   ```
   git add -A
   git commit -m "Add article: talking to families about progress (DfE research); new illustrations; branded RSS page"
   git push
   ```
6. Confirm the "Publish The Practice Exchange" Action succeeds. PUSH TONIGHT (Sunday 15 November), before 06:00 on Monday 16 November, so the new article goes live in the morning. If the push is later than 06:00, run the workflow by hand (Actions → Publish The Practice Exchange → Run workflow) and it will publish straight away.

## Schedule (posts go live at about 6am on their date)
- Mon 16 Nov — NEW: Talking to families about progress: what the DfE's new research means for SEND
- Wed 18 Nov — How ASEND360 helps you track EHCP outcomes (moved from 16 Nov)
- Thu 19 Nov — Behaviour isn't a barrier: it's a signal
- Mon 23 Nov — GUEST: Securing Section F in the classroom (Michelle Woodward)
- Thu 26 Nov — Preparing for Ofsted
- Mon 30 Nov — Small steps are still steps
