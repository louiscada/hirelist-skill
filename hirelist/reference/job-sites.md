# Job sites by country

During setup, paste the section for the user's country, plus **Everywhere**, into the `{{JOB_SITES}}` slot of `daily-run.md`.

These are starting points. Boards change their page layouts and blocking rules. If a direct fetch fails, fall back to WebSearch with `site:` for that board, and mention the failure in the run's last line.

## Philippines

This setup has been run daily and works.

1. **Indeed PH**: WebFetch search pages directly, one per keyword.
   - `https://ph.indeed.com/q-<keyword-with-dashes>-jobs.html`
   - e.g. `https://ph.indeed.com/q-business-analyst-jobs.html`
2. **Glassdoor**: WebFetch Philippines search pages directly.
   - `https://www.glassdoor.com/Job/philippines-<keyword>-jobs-SRCH_IL.0,11_IN204_KO12,<12 + keyword length>.htm`
   - e.g. "grc-analyst" (11 characters) → `…SRCH_IL.0,11_IN204_KO12,23.htm`
3. **JobStreet PH**: WebFetch `https://ph.jobstreet.com/<keyword-with-dashes>-jobs`.
4. **Kalibrr and company career pages**: WebSearch. Covers banks, insurers, fintechs, Big 4 firms and shared-services centers hiring in Metro Manila.

## Singapore

- **MyCareersFuture** (the government job portal) and **JobStreet SG**: WebFetch their search pages if they load, else WebSearch with `site:`.
- **Indeed SG**: `https://sg.indeed.com/q-<keyword>-jobs.html`.
- Company career pages via WebSearch.

## Malaysia

- **JobStreet MY** (`https://my.jobstreet.com/<keyword>-jobs`) and **Indeed MY** (`https://malaysia.indeed.com/q-<keyword>-jobs.html`).
- Company career pages via WebSearch.

## India

- **Naukri** and **Indeed India** (`https://in.indeed.com/q-<keyword>-jobs.html`).
- Company career pages via WebSearch.

## Australia

- **Seek** and **Indeed AU** (`https://au.indeed.com/q-<keyword>-jobs.html`).
- Company career pages via WebSearch.

## United Kingdom

- **Indeed UK** (`https://uk.indeed.com/q-<keyword>-jobs.html`), **Reed** and **Totaljobs**.
- Company career pages via WebSearch.

## United States and Canada

- **Indeed** (`https://www.indeed.com/q-<keyword>-jobs.html`, `https://ca.indeed.com/…`).
- Company applicant-tracking boards, which most US companies post on first (see Everywhere).

## Anywhere else

1. Find the country's Indeed subdomain and its one or two biggest local boards with a quick WebSearch on the first run.
2. Record what worked in the run's notes line.

## Everywhere

- **Company hiring boards**, via WebSearch with `site:`. Most LinkedIn postings come from these, and they can be read.
  - `job-boards.greenhouse.io`
  - `jobs.lever.co`
  - `*.myworkdayjobs.com`
  - `*.recruitee.com`
  - `jobs.ashbyhq.com`
- **Remote boards**, for roles open to the user's country: Remotive, Remote Rocketship, We Work Remotely.
- **LinkedIn cannot be read by an automated run.** It blocks automated fetching. Do not try to work around that: no mirrors, caches or scraping tricks. Find the same posting on the company's careers page instead. Users can turn on LinkedIn's own job alerts for anything this misses.
