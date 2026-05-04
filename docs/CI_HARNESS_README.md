# NLT Red Team CI Harness

> **Governance:** ORG-DEV-OTOI-1.0.0 | Red Team SOP-NLT-003  
> **Maintained by:** NeuroLift Technologies Security Team

---

## Overview

The NLT Red Team CI harness enforces two complementary quality and compliance gates on every pull request targeting `main`:

| Gate | Workflow | Purpose |
| ---- | -------- | ------- |
| **Clearance Rubric** | `redteam-ci.yml` | 3-tier progressive quality check |
| **PGSA Portability Gate** | `pgsa-portability-gate.yml` | Secrets scan + provenance validation |

Both workflows are designed to be **non-blocking by default** during development but become **required status checks** when enabled via branch protection rules.

---

## Clearance Rubric (`redteam-ci.yml`)

Implements a 3-tier progressive clearance system.  Each level must pass before the next one runs.

### Level 1 — Basic

| Step | Tool | What it checks |
| ---- | ---- | -------------- |
| `syntax-check` | `python -m py_compile` | All `.py` files parse without syntax errors |
| `lint-errors` | `flake8` | Fatal linting errors (`E9`, `F63`, `F7`, `F82`) |
| `unit-tests` | `pytest` | Unit test suite passes |

### Level 2 — Standard

| Step | Tool | What it checks |
| ---- | ---- | -------------- |
| `coverage` | `pytest-cov` | Test coverage ≥ 60 % |
| `type-check` | `mypy` | Static type analysis of `src/` |

### Level 3 — Full

| Step | Script | What it checks |
| ---- | ------ | -------------- |
| `secret-scan` | `scan_secrets.py` | Secrets in source tree (Gitleaks) |
| `provenance-check` | `validate_provenance.py` | PGSA provenance manifest compliance |

### Reports

Each level uploads a Markdown report as a GitHub Actions artifact (`clearance-level-<N>-report`).  A summary comment is posted on pull requests when all levels complete.

---

## PGSA Portability Gate (`pgsa-portability-gate.yml`)

Enforces the **Portability and Governance Security Assessment** requirements.

### Jobs

#### `secrets-scan`

- Installs Gitleaks and runs `scripts/scan_secrets.py --fail-on-findings`.
- Fails the gate if any secrets are detected.
- Uses `.github/gitleaks.toml` for NLT-specific rules and allowlisting.

#### `provenance-check`

- Runs `scripts/validate_provenance.py` against all `**/provenance.json` manifests.
- Validates required schema fields and PGSA whitelist/blacklist rules.
- Config loaded from `config/pgsa-allowlists.json`.

#### `pgsa-gate`

Aggregates the results of both jobs.  This is the **required status check** to add to branch protection rules.

---

## Scripts

### `scripts/run_clearance_tests.py`

```
usage: run_clearance_tests.py [-h] [--level {1,2,3}] [--repo-root PATH]
                               [--report-dir PATH] [--report-format {json,markdown}]
                               [--timeout SECONDS] [--verbose]

Options:
  --level          Maximum clearance level to run (1–3, default: 1)
  --repo-root      Repository root path (default: CWD)
  --report-dir     Output directory for reports (default: clearance-reports/)
  --report-format  json | markdown (default: markdown)
  --timeout        Per-step timeout in seconds (default: 300)
  --verbose        Enable debug logging
```

### `scripts/scan_secrets.py`

```
usage: scan_secrets.py [-h] [--scan-path PATH] [--gitleaks-config PATH]
                        [--report-dir PATH] [--report-format {json,markdown}]
                        [--fail-on-findings] [--skip-gitleaks] [--skip-trufflehog]
                        [--verbose]

Options:
  --scan-path        Path to scan (default: CWD)
  --gitleaks-config  Gitleaks config file (default: .github/gitleaks.toml)
  --report-dir       Output directory for reports (default: clearance-reports/)
  --report-format    json | markdown (default: markdown)
  --fail-on-findings Exit 1 when secrets are found
  --skip-gitleaks    Skip Gitleaks even if installed
  --skip-trufflehog  Skip TruffleHog even if installed
  --verbose          Enable debug logging
```

### `scripts/validate_provenance.py`

```
usage: validate_provenance.py [-h] [--scan-root PATH] [--config PATH]
                               [--report-dir PATH] [--report-format {json,markdown}]
                               [--verbose]

Options:
  --scan-root     Root directory to scan for provenance manifests (default: CWD)
  --config        Path to PGSA allowlists JSON (default: config/pgsa-allowlists.json)
  --report-dir    Output directory for reports (default: clearance-reports/)
  --report-format json | markdown (default: markdown)
  --verbose       Enable debug logging
```

---

## Provenance Manifest Schema

Each `provenance.json` (or `*.provenance.json`) must include:

```json
{
  "schema_version": "1.0",
  "component": "my-package",
  "version": "1.2.3",
  "source": "https://pypi.org/project/my-package/",
  "build_system": "pip"
}
```

| Field | Required | Description |
| ----- | -------- | ----------- |
| `schema_version` | ✅ | Manifest format version |
| `component` | ✅ | Package/component name |
| `version` | ✅ | Semantic version |
| `source` | ✅ | Origin URL or registry |
| `build_system` | ✅ | Build tool (`pip`, `npm`, `docker`, etc.) |

---

## PGSA Allowlists (`config/pgsa-allowlists.json`)

```json
{
  "whitelist": ["github.com", "pypi.org", "npmjs.com", ...],
  "blacklist": ["untrusted-registry.example.com", ...]
}
```

- **Whitelist** — advisory; sources not on the list generate a warning but do not fail validation.
- **Blacklist** — enforced; any manifest whose `source` matches a blacklisted origin causes a validation failure.

---

## Gitleaks Configuration (`.github/gitleaks.toml`)

Extends the built-in Gitleaks ruleset with NLT-specific rules:

| Rule ID | Description |
| ------- | ----------- |
| `nlt-api-key` | NLT internal API keys |
| `nlt-jwt-secret` | NLT JWT signing secrets |
| `nlt-supabase-key` | Supabase service-role/anon keys |
| `nlt-cloudflare-token` | Cloudflare API tokens |

The global allowlist suppresses false positives for:
- Placeholder/example values in documentation and tests.
- GitHub Actions expression syntax (`${{ secrets.FOO }}`).
- Environment variable references (`$ENV_VAR`, `os.environ.get(...)`).

---

## Enabling as Required Status Checks

To enforce both gates on `main`:

1. Go to **Settings → Branches → Branch protection rules → `main`**
2. Enable **"Require status checks to pass before merging"**
3. Add the following required checks:
   - `Clearance Level 1 — Basic`
   - `PGSA Gate — Required Status Check`
4. Enable **"Require branches to be up to date before merging"**

---

## Local Development

Run any script locally from the repository root:

```bash
# Run Level 1 clearance (syntax, lint, tests)
python scripts/run_clearance_tests.py --level 1 --verbose

# Run secrets scan (Gitleaks must be installed)
python scripts/scan_secrets.py --fail-on-findings --verbose

# Validate provenance manifests
python scripts/validate_provenance.py --verbose
```

Install Gitleaks for local use:

```bash
# macOS
brew install gitleaks

# Linux
GITLEAKS_VERSION="8.21.2"
curl -sSfL \
  "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
  | tar -xz -C ~/.local/bin gitleaks
```
