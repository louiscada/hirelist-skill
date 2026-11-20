# First-time setup

Goal: the user ends with their own Hirelist tracker (with their resume and preferences in it) and a weekday scheduled shortlist. It takes about five minutes of their time.

Say in one sentence what's about to happen, then go.

## 1. Publish their tracker

1. Copy `assets/hirelist.html` from this skill's folder into your working or scratch folder, unchanged.
2. Publish it as a new artifact with:
   - `capabilities`: `{"db": {}, "sample": {}, "downloads": true}`
     - `db` stores the resume, settings and jobs
     - `sample` lets the page ask Claude to write cover letters
     - `downloads` lets it save letters as PDF or Word
   - `icon`: `checklist`
   - `description`: "My Hirelist: daily job matches, applications and cover letters."
3. Tell the user to open it. A five-step intro starts on its own:
   1. Welcome
   2. **Your resume**: upload a PDF or paste the text
   3. **Your search**: roles in priority order, the most years a job may ask for, location, optional minimum salary
   4. **Extras**: three optional features, each with a switch
   5. Done
4. Mention once: the resume is saved with the tracker, so anyone they share the tracker link with can see it.

Wait for them to finish. If they attached a resume in chat instead and want you to fill it in, write it yourself (see "Database fields" below) after they confirm.

## 2. Check what they saved

Read `settings/prefs` and `settings/resume` from the tracker's database.

- `prefs.onboarded` is true and the resume has text → continue.
- No resume → setup can continue, but say matches will be rough until they add one under Settings.
- Nothing saved → they haven't finished the intro. Ask them to, or offer to fill it in from what they tell you.

## 3. Ask the remaining questions

Use a question card if you have one, otherwise a short numbered list:

1. **Which country are they job hunting in?** This picks the job sites (see `job-sites.md`). Use their settings' location if it's clear.
2. **What time should the shortlist run?** Default: weekdays at 9:57 in their timezone. Avoid exactly :00 or :30, when scheduled tasks are busiest.
3. **Their timezone**, if you can't tell.

## 4. Create the scheduled task

1. Take the prompt block from `daily-run.md` and fill in its placeholders:
   - `{{TRACKER_URL}}`: the artifact link from step 1
   - `{{FIRST_NAME}}`: from `settings/prefs.name`, or "the user"
   - `{{HOME}}`: city and country, e.g. "Cebu City, Philippines"
   - `{{TIMEZONE}}`: IANA name, e.g. `Asia/Manila`
   - `{{JOB_SITES}}`: the section for their country from `job-sites.md`, plus the "Everywhere" section
2. Create the task:
   - **Name:** "Hirelist daily shortlist"
   - **Schedule:** weekdays at the chosen time, written with `CRON_TZ=<timezone>`
   - **Prompt:** the filled-in text
   - **Notifications:** on, if the tool supports it
3. Each run starts a fresh session that may not have this skill installed. The prompt must stand on its own, so paste the whole block, not a reference to it.

If no scheduling tool turns up after searching, say so plainly. Suggest they say "run my shortlist" each morning, or set a phone reminder that says so.

## 5. Offer a first run now

Ask if they'd like their first shortlist now. If yes, either fire the scheduled task once or follow `daily-run.md` in this chat. Tell them where results will show up: a separate run with a notification, or right here.

## 6. Wrap up

In three or four lines:

- Their tracker link is in the artifact card.
- When the shortlist runs.
- How to sort jobs: swipe right for applied, left for not for me.
- How to get a cover letter: open a job and tap Write a cover letter.
- Where to change settings.

## Database fields

The tracker reads and writes these. Use exactly these names if you write any yourself.

**`settings/prefs`**: `onboarded` (bool), `name`, `roles` (text, most important first), `avoid`, `maxYears` (number), `location`, `salaryFloor` (text), `learnFromDismissals` (bool), `autoCheckClosed` (bool), `followUps` (bool), `followUpDays` (number), `updatedOn` ("YYYY-MM-DD").

**`settings/resume`**: `text` (up to 60,000 characters), `fileName`, `source` ("pdf", "file" or "paste"), `updatedOn`.

**`jobs/<id>`**, one per job:

| Field | Meaning |
| --- | --- |
| `title`, `company`, `location` | The basics |
| `posted` | "YYYY-MM-DD" or null |
| `source` | Job site name |
| `salary` | Text, or null when not listed |
| `fit` | Number 1–10 |
| `fitBreakdown` | `{skills, experience, role, location}`, each 1–10 |
| `isAI` | Bool |
| `why`, `gap` | One line each |
| `link` | Posting URL |
| `found` | Date added |
| `addedBy` | "shortlist" or "manual" |
| `status` | "new", "applied", "interviewing", "offer", "rejected", "no_response", "skipped" or "expired" |
| `appliedOn`, `stageOn`, `expiredOn` | Dates |
| `skipReason` | "wrong_role", "too_senior", "salary", "location", "company" or "other" |
| `notes` | The user's notes |
| `followUpDoneOn` | Date |
| `coverLetter`, `coverLetterOn`, `jobDescription` | The saved letter and what it was written from |

The doc id is a slug: company + "-" + title, lowercase, every run of characters other than a–z and 0–9 replaced with "-", trimmed of "-", cut to 120 characters, trimmed again.
