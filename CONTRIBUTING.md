# Contributing to Hirelist

Thanks for helping make Hirelist better. Ideas, bug reports and pull requests are all welcome. The maintainer reviews every change, and only approved changes are merged into the official Hirelist.

## Never share personal data

Never post resumes, cover letters, names, salaries or application details in issues, pull requests, screenshots or test files. Use made-up companies and people.

## Reporting a bug or suggesting an idea

Use the issue templates. A good bug report says:

- What you did or asked
- What Hirelist did
- What you expected
- Which part (setup, the daily shortlist, the tracker page or cover letters)
- Which Claude app you used

**New job sites are especially welcome.** If a board works well in your country, open an idea with its name and the search URL pattern that loads.

## Making a change

1. Fork the repository and create a branch.
2. Make your change.
   - The tracker is one self-contained file: `hirelist/assets/hirelist.html`, plain JavaScript with no build step.
   - Libraries load from cdnjs at exact versions.
3. Run the tests from the repository root:

   ```bash
   python -m unittest discover -s tests -v
   ```

   They need Python 3.9+. The JavaScript checks also need Node.js.
4. Add a test where you can, and a line under a new heading in `CHANGELOG.md`.
5. Open a pull request using the template.

## Keep the three descriptions in step

The tracker page, `reference/setup.md` (the database fields) and `reference/daily-run.md` (what the scheduled run reads and writes) describe the same data. If you add or rename a field or status, change all three. The tests check the parts that can be checked automatically, such as the statuses and the slug rule.

## Ground rules

- Hirelist never applies to jobs, signs in to job sites or messages employers on the user's behalf.
- It never gets around sites that block automated reading.
- It never invents postings, salaries or requirements.
- Cover letters use only facts from the user's resume.

## Releasing (maintainer)

1. Bump `VERSION` in `hirelist/assets/hirelist.html` and move the changelog notes under the new version.
2. Push.
3. On GitHub, go to **Releases → Draft a new release**. Tag it `vX.Y.Z`, paste the changelog notes, and publish.
4. The release workflow runs the tests and attaches `hirelist.zip` and `hirelist.skill` automatically.

Existing users keep their tracker. To get a new tracker version, they ask Claude to "update my Hirelist page" with the new skill installed, and Claude republishes the page to the same link. Their saved jobs and settings stay.
