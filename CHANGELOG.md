# Changelog

All notable changes to Hirelist. Versions follow [semantic versioning](https://semver.org): a change to the tracker's stored data that older pages can't read is a major version.

## [1.0.0] — 2026-11-20

First public release.

### Added
- **Tracker page**:
  - Today view with the three best jobs to apply to and follow-ups that need a nudge
  - All jobs with search and filters
  - A board for applications, from Applied to Offer
  - Notes on every job
- **Sorting**: swipe right for applied and left for not for me, with buttons and keyboard shortcuts on a computer. Every action can be undone.
- **Onboarding** in five steps: welcome, resume (PDF upload or paste), search preferences, optional extras, done.
- **Cover letters**: one tap per job, written by Claude from the saved resume and, optionally, the pasted job description. Copy, save as PDF, or save as Word.
- **Daily shortlist**, a scheduled task that:
  - reads the resume and settings from the tracker
  - searches several job sites
  - skips anything already in the tracker
  - adds new matches with a fit score and a breakdown of that score
  - sends a ranked list
- **Optional features**, each with a switch: learn from "Not for me" reasons, flag closed postings, follow-up reminders after a set number of days.
- **Job sources**: tested for the Philippines, with starting points for other countries and company hiring boards everywhere.
- **Fallback** for platforms without the tracker page: a `jobs.csv` file in the user's folder.
