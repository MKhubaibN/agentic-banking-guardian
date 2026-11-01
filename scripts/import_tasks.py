#!/usr/bin/env python3
"""Import the planning sheet into GitHub Issues and a GitHub Project.

Usage:
  python scripts/import_tasks.py tasks.csv OWNER/REPO PROJECT_NUMBER PROJECT_OWNER [--dry-run]

tasks.csv columns (header row required, names case-insensitive):
  ID, Title, Owner, Due, Description
Owner must be a GitHub username. The ID is the join key: issue title = "[ID] Title".
Re-running is safe; tasks whose "[ID]" issue already exists are skipped.
Needs: gh CLI logged in with scopes `repo` and `project`.
"""

import csv
import json
import subprocess
import sys


def gh(*args):
    return subprocess.run(
        ["gh", *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    path, repo, proj, proj_owner = sys.argv[1:5]
    dry = "--dry-run" in sys.argv
    existing = set()
    if not dry:
        issues = json.loads(
            gh(
                "issue",
                "list",
                "-R",
                repo,
                "--state",
                "all",
                "--limit",
                "500",
                "--json",
                "title",
            )
        )
        existing = {
            i["title"].split("]")[0].lstrip("[")
            for i in issues
            if i["title"].startswith("[")
        }
        gh("label", "create", "task", "-R", repo, "--force")
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [
            {k.strip().lower(): (v or "").strip() for k, v in r.items()}
            for r in csv.DictReader(f)
        ]
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate task IDs in sheet"
    for r in rows:
        if r["id"] in existing:
            print(f"skip   {r['id']} (exists)")
            continue
        title = f"[{r['id']}] {r['title']}"
        body = (
            f"**Task ID:** {r['id']}\n**Owner:** @{r['owner']}\n"
            f"**Due:** {r['due']}\n\n{r.get('description', '')}"
        )
        print(f"create {title}")
        if dry:
            continue
        cmd = ["issue", "create", "-R", repo, "-t", title, "-b", body, "-l", "task"]
        if r["owner"]:
            cmd += ["-a", r["owner"]]
        url = gh(*cmd)
        gh("project", "item-add", proj, "--owner", proj_owner, "--url", url)
    print(f"done: {len(rows)} rows processed")


if __name__ == "__main__":
    main()
