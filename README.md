# Agentic AI Banking Guardian

Risk-adaptive security framework for controlled autonomy in agentic banking systems.
UET Taxila, CS-400 FYP 2026-27. Supervisor: Dr. Qamas Gul Khan Safi.

> Research prototype. Synthetic data only. No real money, customer data or banking rails.

## Layout

| Folder      | Contents                                                                | Owner   |
|-------------|-------------------------------------------------------------------------|---------|
| `gateway/`  | Tool gateway, schema validation, provenance tagging, process isolation  | Raja    |
| `policy/`   | OPA/Rego policy, risk score, cumulative-exposure engine                 | Raja    |
| `bank/`     | Simulated bank: PostgreSQL schema, services, synthetic data             | Raja    |
| `tokens/`   | Attenuation-only delegation tokens, keys, signed approvals, audit chain | Khubaib |
| `eval/`     | Agent runner, baselines B0-B4, benchmark, attackers, statistics         | Talha   |
| `docs/`     | Threat model, specs, evaluation plan, reports                           | shared  |
| `infra/`    | Docker Compose, CI helpers, key/secret handling                         | Khubaib |
| `scripts/`  | Repo setup and task-import scripts                                      | Khubaib |

Ownership is enforced by `.github/CODEOWNERS`.

## Workflow

1. Pick a task from the board. The task ID is the join key with the planning sheet (e.g. `SET-03`).
2. Branch: `git checkout -b SET-03-short-description`
3. Commit often; start commit messages with the task ID.
4. Open a PR. Title starts with the task ID; body says `Closes #<issue>`.
5. CI must pass and one other person must approve. Squash-merge.

Never push to `main` directly.

## Secrets rule

No keys, tokens, passwords or `.env` files in git, ever. `.env.example` holds variable names
only. Pre-commit and CI both run gitleaks. If a secret is ever committed, treat it as leaked:
rotate it first, then clean history.

## Local setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install pre-commit pytest ruff
pre-commit install
cp .env.example .env   # fill in locally, never commit
```
