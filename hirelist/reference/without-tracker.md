# Running Hirelist without the tracker page

Use this when the platform can't publish an artifact with a database. It works on other AI apps that read skills, and in Claude Code. Everything still works except swiping, the board and the one-tap cover letters.

## The file

Keep the list in `hirelist-data/jobs.csv` in the user's working folder. Start from `templates/jobs.csv` in this skill's folder.

- One row per job. The columns match the tracker's fields: `id, title, company, location, posted, source, salary, fit, why, gap, link, found, status, applied_on, skip_reason, notes`.
- `status` uses the same words as the tracker: new, applied, interviewing, offer, rejected, no_response, skipped, expired.
- The user edits `status` in any spreadsheet app, or tells you ("I applied to the Northwind job") and you update the row.

Keep the resume and preferences in `hirelist-data/profile.md`:

- The resume text
- Roles, most important first
- Roles to avoid
- Most years a job may ask for
- Location
- Minimum salary
- Whether "learn from not for me", "flag closed postings" and "follow-up reminders" are on, and the follow-up days

## A run

Follow `daily-run.md` with these swaps:

- Step 1 reads `profile.md` and `jobs.csv` instead of the tracker's database.
- Step 1c and Step 3 edit and append rows in `jobs.csv` instead of writing to the database.
- Step 4's tracker line becomes: "Update the status column in hirelist-data/jobs.csv as you apply."

If the platform doesn't keep files between conversations, give the user the updated `jobs.csv` at the end and ask them to attach it next time. Without it, nothing stops repeats.

## Scheduling

If the platform has its own scheduled tasks, use them. The prompt must stand on its own and point at the user's folder.

For command-line agents, a system scheduler works too. Examples: cron on macOS or Linux, Task Scheduler on Windows, or a scheduled GitHub Action that runs the agent with the daily prompt. Otherwise the user says "run my shortlist" each morning.
