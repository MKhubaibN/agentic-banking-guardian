#!/usr/bin/env bash
# Usage: ./scripts/setup_branch_protection.sh OWNER/REPO
# Needs: gh CLI logged in as repo admin. Run AFTER the first push and one CI run,
# so the check names exist.
set -euo pipefail
REPO="${1:?usage: $0 OWNER/REPO}"
gh api -X PUT "repos/$REPO/branches/main/protection" --input - <<JSON
{
  "required_status_checks": { "strict": true, "contexts": ["pre-commit", "test"] },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "require_code_owner_reviews": true,
    "dismiss_stale_reviews": true
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
echo "Protection set on $REPO:main"
