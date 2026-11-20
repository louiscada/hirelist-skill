"""Checks that keep the Hirelist skill installable and consistent.

Run from the repository root:  python -m unittest discover -s tests -v
Uses the standard library only. The JavaScript checks run when Node.js is
installed and are skipped otherwise (GitHub's runners have it).
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "hirelist")
HTML = os.path.join(SKILL, "assets", "hirelist.html")


def read(*parts):
    with open(os.path.join(SKILL, *parts), encoding="utf-8") as f:
        return f.read()


def py_slug(company, title):
    s = re.sub(r"[^a-z0-9]+", "-", (company + "-" + title).lower()).strip("-")
    return s[:120].rstrip("-")


def page_script():
    m = re.search(r"<script>(.*)</script>", read("assets", "hirelist.html"), re.S)
    return m.group(1)


class SkillFile(unittest.TestCase):
    def setUp(self):
        self.text = read("SKILL.md")
        m = re.match(r"---\n(.*?)\n---\n", self.text, re.S)
        self.assertIsNotNone(m, "SKILL.md needs YAML frontmatter")
        self.front = dict(line.split(": ", 1) for line in m.group(1).splitlines())

    def test_frontmatter(self):
        self.assertEqual(self.front["name"], "hirelist")
        self.assertTrue(20 < len(self.front["description"]) <= 1024)
        self.assertNotIn("<", self.front["description"])

    def test_referenced_files_exist(self):
        for ref in set(re.findall(r"`((?:reference|assets|templates)/[\w./-]+)`", self.text)):
            self.assertTrue(os.path.isfile(os.path.join(SKILL, ref)), ref)


class DailyRun(unittest.TestCase):
    def setUp(self):
        text = read("reference", "daily-run.md")
        m = re.search(r"```text\n(.*?)\n```", text, re.S)
        self.assertIsNotNone(m, "daily-run.md needs one ```text prompt block")
        self.prompt = m.group(1)

    def test_placeholders(self):
        found = set(re.findall(r"\{\{([A-Z_]+)\}\}", self.prompt))
        self.assertEqual(found, {"FIRST_NAME", "HOME", "TIMEZONE", "TRACKER_URL", "JOB_SITES"})

    def test_placeholders_documented_in_setup(self):
        setup = read("reference", "setup.md")
        for name in ("FIRST_NAME", "HOME", "TIMEZONE", "TRACKER_URL", "JOB_SITES"):
            self.assertIn("{{%s}}" % name, setup)

    def test_safety_lines(self):
        self.assertIn("Do NOT apply to anything", self.prompt)
        self.assertIn("Never invent a posting", self.prompt)
        self.assertIn("never write to the \"settings\" collection", self.prompt)

    def test_statuses_match_page(self):
        page = read("assets", "hirelist.html")
        for status in ("applied", "interviewing", "offer", "rejected", "no_response", "skipped", "expired"):
            self.assertIn('"%s"' % status, self.prompt)
            self.assertIn(status, page)


class TrackerPage(unittest.TestCase):
    def setUp(self):
        self.html = read("assets", "hirelist.html")

    def test_is_a_fragment_with_title(self):
        self.assertTrue(self.html.startswith("<title>Hirelist</title>"))
        for tag in ("<!doctype", "<html", "<head>", "<body"):
            self.assertNotIn(tag, self.html.lower())

    def test_no_personal_or_regional_hardcoding(self):
        for s in ("Asia/Manila", "Metro Manila", "UgfQo", "louiscada@"):
            self.assertNotIn(s, self.html)

    def test_database_paths(self):
        for path in ('"jobs"', '"settings/prefs"', '"settings/resume"'):
            self.assertIn(path, self.html)

    def test_libraries_pinned(self):
        urls = re.findall(r"https://cdnjs\.cloudflare\.com/ajax/libs/[^\"']+", self.html)
        self.assertEqual(len(urls), 4)
        for u in urls:
            self.assertRegex(u, r"/\d+\.\d+\.\d+/")

    def test_version_matches_changelog(self):
        v = re.search(r'var VERSION = "([\d.]+)"', self.html).group(1)
        with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
            self.assertIn("## [%s]" % v, f.read())


@unittest.skipUnless(shutil.which("node"), "Node.js not installed")
class TrackerScript(unittest.TestCase):
    def test_syntax(self):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(page_script())
        try:
            r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
        finally:
            os.unlink(f.name)

    def test_slug_matches_daily_run_rule(self):
        m = re.search(r"  function slug\(company, title\) \{.*?\n  \}", page_script(), re.S)
        self.assertIsNotNone(m)
        cases = [["RELX", "Security Analyst: Third Party & Trust Center"],
                 ["Acme, Inc.", "Cybersecurity Analyst (GRC-Focused)"],
                 ["Ünïcode Co", "  Data -- Analyst  "],
                 ["A" * 80, "B" * 80]]
        js = m.group(0) + "\nconsole.log(JSON.stringify(%s.map(function (c) { return slug(c[0], c[1]); })));" % json.dumps(cases)
        r = subprocess.run(["node", "-e", js], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), [py_slug(*c) for c in cases])
        self.assertEqual(py_slug(*cases[0]), "relx-security-analyst-third-party-trust-center")


class FallbackTemplate(unittest.TestCase):
    def test_csv_columns_documented(self):
        header = read("templates", "jobs.csv").strip()
        doc = read("reference", "without-tracker.md")
        self.assertIn(header.replace(",", ", "), doc)


if __name__ == "__main__":
    unittest.main()
