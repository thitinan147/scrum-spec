"""Contract tests for the repo layout, the skill's frontmatter, links, versions, and
the markers shared by the prompts and scripts/check.py.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / "skills"
SKILL = SKILLS_DIR / "scrum-spec"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
THAI = re.compile(f"[{chr(0x0E00)}-{chr(0x0E7F)}]")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip().strip('"').strip("'")
    return data


def skill_text() -> str:
    return (SKILL / "SKILL.md").read_text(encoding="utf-8")


class SkillContractTests(unittest.TestCase):
    def test_one_skill_directory(self) -> None:
        dirs = sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir())
        self.assertEqual(dirs, ["scrum-spec"])

    def test_skill_ships_only_runtime_files(self) -> None:
        bad = [
            str(p.relative_to(REPO))
            for p in SKILL.rglob("*")
            if p.name in {"__pycache__", ".DS_Store"} or p.suffix in {".pyc", ".pyo"}
            or p.name.startswith("test_") or p.name == "evals"
        ]
        self.assertEqual(bad, [], f"not runtime files in the skill: {bad}")

    def test_agentskills_frontmatter_constraints(self) -> None:
        fm = parse_frontmatter(skill_text())
        self.assertEqual(fm.get("name"), SKILL.name)
        self.assertRegex(fm.get("name", ""), r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertTrue(1 <= len(fm.get("description", "")) <= 1024, len(fm.get("description", "")))
        self.assertTrue(1 <= len(fm.get("compatibility", "")) <= 500)

    def test_one_run_loads_at_most_1500_words(self) -> None:
        skill_words = len(skill_text().split())
        steps = {p.name: len(p.read_text(encoding="utf-8").split()) for p in (SKILL / "steps").glob("*.md")}
        self.assertEqual(sorted(steps), ["ac.md", "handoff.md", "split.md"])
        for name, words in steps.items():
            self.assertLessEqual(skill_words + words, 1500, f"SKILL.md + {name}: {skill_words + words} words")
        for ref in (SKILL / "references").glob("*.md"):
            self.assertLessEqual(len(ref.read_text(encoding="utf-8").split()), 450, ref.name)

    def test_section_names_cited_in_quotes_exist(self) -> None:
        headings = {}
        for md_file in SKILL.rglob("*.md"):
            headings[md_file.name] = set(re.findall(r"^#+ (.+)$", md_file.read_text(encoding="utf-8"), re.MULTILINE))
        for md_file in SKILL.rglob("*.md"):
            for name, target in re.findall(r'"([^"]+)" (?:in|of) `([A-Za-z-]+\.md)`', md_file.read_text(encoding="utf-8")):
                self.assertIn(name, headings.get(target, set()), f"{md_file.name} cites missing section {name!r} in {target}")

    def test_markdown_links_resolve_inside_the_skill(self) -> None:
        root = SKILL.resolve()
        for md_file in SKILL.rglob("*.md"):
            for target in LINK_RE.findall(md_file.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "#")):
                    continue
                resolved = (md_file.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.exists(), f"{md_file} -> {target}")
                self.assertTrue(resolved.is_relative_to(root), f"link leaves the skill: {md_file} -> {target}")

    def test_backticked_skill_files_exist(self) -> None:
        for md_file in SKILL.rglob("*.md"):
            for ref in re.findall(r"`((?:steps|references|scripts)/[A-Za-z0-9._-]+)`", md_file.read_text(encoding="utf-8")):
                self.assertTrue((SKILL / ref).exists(), f"{md_file.name} cites missing {ref}")

    def test_human_only_skill_has_three_layer_protection(self) -> None:
        fm = parse_frontmatter(skill_text())
        self.assertEqual(fm.get("disable-model-invocation"), "true")  # Claude Code
        yaml_text = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertRegex(yaml_text, r"allow_implicit_invocation:\s*false")  # Codex
        self.assertTrue(fm.get("description", "").startswith("HUMAN-ONLY COMMAND."))  # Cursor and others

    def test_no_claude_only_variables_in_the_body(self) -> None:
        body = skill_text().split("---", 2)[2]
        for md_file in [SKILL / "SKILL.md", *SKILL.glob("steps/*.md"), *SKILL.glob("references/*.md")]:
            text = body if md_file.name == "SKILL.md" else md_file.read_text(encoding="utf-8")
            self.assertNotIn("${CLAUDE_SKILL_DIR}", text, md_file.name)

    def test_versions_match_across_plugin_marketplace_and_skill(self) -> None:
        plugin = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        versions = {"plugin.json": plugin["version"]}
        versions.update({"marketplace.json": e["version"] for e in market["plugins"] if e["name"] == plugin["name"]})
        match = re.search(r'^\s+version:\s*"([^"]+)"', skill_text(), re.MULTILINE)
        self.assertIsNotNone(match, "metadata.version missing")
        versions["SKILL.md"] = match.group(1)
        self.assertEqual(len(versions), 3, versions)
        self.assertEqual(len(set(versions.values())), 1, f"versions differ: {versions}")
        changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(f"## {plugin['version']}", changelog)

    def test_checker_markers_appear_in_the_prompts(self) -> None:
        prompts = "\n".join(p.read_text(encoding="utf-8") for p in SKILL.rglob("*.md"))
        for marker in ("<!-- scrum-spec -->", "**approve:** ❌ waiting for PO", "**approve:** ✅ <name> · <YYYY-MM-DD>",
                       "- **D<n>** <what was decided> · <name> · <YYYY-MM-DD>", "⚠️ D<n>", "per <work> D<n>:", "**Source:**",
                       "## Acceptance Criteria", "## Questions", "## Decisions", "## Test steps",
                       "| # | Given | When | Then |", "| # | Question | Ask | Blocks | Answer |"):
            self.assertIn(marker, prompts, f"check.py relies on {marker!r} but no prompt writes it")

    def test_fixtures_follow_the_templates(self) -> None:
        spec = (REPO / "evals" / "files" / "room-booking" / "scrum-spec" / "rb-12-book-room" / "spec.md").read_text(encoding="utf-8")
        order = [line for line in spec.splitlines() if line.startswith("## ")]
        self.assertEqual(order, ["## Story", "## Rules", "## Acceptance Criteria", "## Questions", "## Decisions",
                                 "## Test steps"])
        for section in order:
            self.assertIn(section, skill_text())

    def test_no_thai_outside_allowed_places(self) -> None:
        allowed = {SKILL / "references" / "input.md", REPO / "evals" / "evals.json"}
        for path in REPO.rglob("*"):
            if ".git" in path.parts or not path.is_file() or path in allowed:
                continue
            if path.suffix in {".md", ".py", ".json", ".yaml", ".yml", ".txt"}:
                self.assertIsNone(THAI.search(path.read_text(encoding="utf-8")), str(path.relative_to(REPO)))

    def test_readme_links_and_paths_exist(self) -> None:
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        for target in LINK_RE.findall(readme):
            if target.startswith(("http://", "https://", "#")):
                continue
            self.assertTrue((REPO / target.split("#", 1)[0]).exists(), f"README link missing: {target}")
        for match in re.findall(r"\bskills/([a-z0-9-]+(?:/[a-zA-Z0-9._-]+)*)", readme):
            self.assertTrue((SKILLS_DIR / match).exists(), f"README path missing: skills/{match}")


if __name__ == "__main__":
    unittest.main()
