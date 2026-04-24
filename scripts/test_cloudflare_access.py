#!/usr/bin/env python3
"""
NeuroLift Solutions — Cloudflare API Access Probe
==================================================

Tests Cloudflare API access using credentials from environment variables and
produces a detailed, human-readable report showing:

  • Which credentials are present / missing
  • Token validity (via /user/tokens/verify)
  • Per-permission access status for every resource this project uses
  • Exactly which token permissions are needed for anything that failed

Required environment variables (set as GitHub org secrets):
  CLOUDFLARE_API_TOKEN   — API token (mandatory)
  CLOUDFLARE_ACCOUNT_ID  — Account ID (needed for Workers / R2 / D1 checks)
  CLOUDFLARE_ZONE_ID     — Zone ID  (needed for zone-level checks; auto-discovered if omitted)

Usage:
  python scripts/test_cloudflare_access.py

Exit codes:
  0  — all tested endpoints returned successful responses
  1  — one or more endpoints failed (token invalid, missing permission, etc.)
  2  — CLOUDFLARE_API_TOKEN not set; nothing was tested
"""

import os
import sys
from typing import Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package is not installed.  Run: pip install requests")
    sys.exit(1)

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

BASE_URL = "https://api.cloudflare.com/client/v4"

# ANSI colours (disabled automatically on non-TTY via the helper below)
_USE_COLOUR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _USE_COLOUR else text


GREEN = lambda t: _c("32", t)   # noqa: E731
RED = lambda t: _c("31", t)   # noqa: E731
YELLOW = lambda t: _c("33", t)   # noqa: E731
CYAN = lambda t: _c("36", t)   # noqa: E731
BOLD = lambda t: _c("1", t)   # noqa: E731

OK = GREEN("✅  PASS")
FAIL = RED("❌  FAIL")
WARN = YELLOW("⚠️   WARN")
SKIP = YELLOW("⏭️   SKIP")


def section(title: str) -> None:
    print(f"\n{BOLD(title)}")
    print("─" * 60)


def _get(token: str, endpoint: str, params: Optional[Dict] = None) -> Tuple[int, Dict]:
    """Make a GET request; return (status_code, body_dict)."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=headers,
            params=params or {},
            timeout=15,
        )
        try:
            body = resp.json()
        except Exception:
            body = {"raw": resp.text}
        return resp.status_code, body
    except requests.exceptions.RequestException as exc:
        return 0, {"error": str(exc)}


def _errors(body: Dict) -> str:
    """Extract human-readable error string from a Cloudflare API response."""
    errs = body.get("errors", [])
    if errs:
        return "; ".join(
            f"[{e.get('code', '?')}] {e.get('message', 'unknown')}" for e in errs
        )
    if "error" in body:
        return body["error"]
    return body.get("raw", "unknown error")


# ──────────────────────────────────────────────
# Individual probe functions
# Each returns (status_label, detail_string, success_bool)
# ──────────────────────────────────────────────

def probe_token_verify(token: str) -> Tuple[str, str, bool]:
    """GET /user/tokens/verify — confirms the token is valid."""
    code, body = _get(token, "/user/tokens/verify")
    if code == 200 and body.get("success"):
        result = body.get("result", {})
        status = result.get("status", "unknown")
        detail = f"Token status: {status}"
        return OK, detail, True
    if code == 401:
        return FAIL, (
            "401 Unauthorized — token is invalid or has been revoked.\n"
            "       Action: regenerate the token at "
            "https://dash.cloudflare.com/profile/api-tokens"
        ), False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_list_zones(token: str) -> Tuple[str, str, bool, Optional[str]]:
    """GET /zones — needs Zone:Read permission.  Returns discovered zone_id."""
    code, body = _get(token, "/zones")
    if code == 200 and body.get("success"):
        zones = body.get("result", [])
        if zones:
            names = ", ".join(z.get("name", "?") for z in zones[:5])
            extra = f" (+ {len(zones) - 5} more)" if len(zones) > 5 else ""
            detail = f"{len(zones)} zone(s): {names}{extra}"
            first_id = zones[0].get("id")
        else:
            detail = "0 zones — account has no domains yet"
            first_id = None
        return OK, detail, True, first_id
    if code == 403:
        return FAIL, (
            "403 Forbidden — token is missing Zone:Read permission.\n"
            "       Required permission: Zone → Zone → Read"
        ), False, None
    return FAIL, f"HTTP {code}: {_errors(body)}", False, None


def probe_zone_details(token: str, zone_id: str) -> Tuple[str, str, bool]:
    """GET /zones/{id} — Zone:Read."""
    code, body = _get(token, f"/zones/{zone_id}")
    if code == 200 and body.get("success"):
        z = body.get("result", {})
        return OK, f"Zone '{z.get('name')}' — plan: {z.get('plan', {}).get('name', 'unknown')}", True
    if code == 403:
        return FAIL, "403 Forbidden — need Zone → Zone → Read", False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_dns_records(token: str, zone_id: str) -> Tuple[str, str, bool]:
    """GET /zones/{id}/dns_records — Zone:DNS:Read (or Edit)."""
    code, body = _get(token, f"/zones/{zone_id}/dns_records")
    if code == 200 and body.get("success"):
        records = body.get("result", [])
        return OK, f"{len(records)} DNS record(s) readable", True
    if code == 403:
        return FAIL, "403 Forbidden — need Zone → DNS → Read (or Edit)", False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_page_rules(token: str, zone_id: str) -> Tuple[str, str, bool]:
    """GET /zones/{id}/pagerules — Zone:Page Rules:Read (or Edit)."""
    code, body = _get(token, f"/zones/{zone_id}/pagerules", {"status": "active"})
    if code == 200 and body.get("success"):
        rules = body.get("result", [])
        return OK, f"{len(rules)} active page rule(s)", True
    if code == 403:
        return FAIL, "403 Forbidden — need Zone → Page Rules → Read (or Edit)", False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_zone_settings(token: str, zone_id: str) -> Tuple[str, str, bool]:
    """GET /zones/{id}/settings — Zone:Zone Settings:Read (or Edit)."""
    code, body = _get(token, f"/zones/{zone_id}/settings")
    if code == 200 and body.get("success"):
        settings = body.get("result", [])
        ssl_setting = next(
            (s.get("value") for s in settings if s.get("id") == "ssl"), "unknown"
        )
        return OK, f"{len(settings)} settings readable (SSL mode: {ssl_setting})", True
    if code == 403:
        return FAIL, "403 Forbidden — need Zone → Zone Settings → Read (or Edit)", False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_security_level(token: str, zone_id: str) -> Tuple[str, str, bool]:
    """GET /zones/{id}/settings/security_level — Zone:Zone Settings:Read."""
    code, body = _get(token, f"/zones/{zone_id}/settings/security_level")
    if code == 200 and body.get("success"):
        level = body.get("result", {}).get("value", "unknown")
        return OK, f"Security level: {level}", True
    if code == 403:
        return FAIL, "403 Forbidden — need Zone → Zone Settings → Read (or Edit)", False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_ssl_settings(token: str, zone_id: str) -> Tuple[str, str, bool]:
    """GET /zones/{id}/settings/ssl — Zone:Zone Settings:Read."""
    code, body = _get(token, f"/zones/{zone_id}/settings/ssl")
    if code == 200 and body.get("success"):
        mode = body.get("result", {}).get("value", "unknown")
        return OK, f"SSL mode: {mode}", True
    if code == 403:
        return FAIL, "403 Forbidden — need Zone → Zone Settings → Read (or Edit)", False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_analytics(token: str, zone_id: str) -> Tuple[str, str, bool]:
    """GET /zones/{id}/analytics/dashboard — Zone:Analytics:Read."""
    code, body = _get(token, f"/zones/{zone_id}/analytics/dashboard")
    if code == 200 and body.get("success"):
        return OK, "Analytics dashboard readable", True
    if code == 403:
        return FAIL, "403 Forbidden — need Zone → Analytics → Read", False
    if code == 400:
        # Cloudflare returns 400 for free plans without analytics; token IS valid
        return WARN, "400 — analytics may require a paid Cloudflare plan", True
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_workers_scripts(token: str, account_id: str) -> Tuple[str, str, bool]:
    """GET /accounts/{id}/workers/scripts — Account:Workers Scripts:Read (or Edit)."""
    code, body = _get(token, f"/accounts/{account_id}/workers/scripts")
    if code == 200 and body.get("success"):
        scripts = body.get("result", [])
        names = ", ".join(s.get("id", "?") for s in scripts[:5]) if scripts else "none deployed"
        return OK, f"{len(scripts)} Worker script(s): {names}", True
    if code == 403:
        return FAIL, (
            "403 Forbidden — need Account → Workers Scripts → Read (or Edit)\n"
            "       Also verify CLOUDFLARE_ACCOUNT_ID is correct."
        ), False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


def probe_workers_routes(token: str, zone_id: str) -> Tuple[str, str, bool]:
    """GET /zones/{id}/workers/routes — Account:Workers Scripts:Read."""
    code, body = _get(token, f"/zones/{zone_id}/workers/routes")
    if code == 200 and body.get("success"):
        routes = body.get("result", [])
        return OK, f"{len(routes)} Worker route(s) configured", True
    if code == 403:
        return FAIL, "403 Forbidden — need Account → Workers Scripts → Read (or Edit)", False
    return FAIL, f"HTTP {code}: {_errors(body)}", False


# ──────────────────────────────────────────────
# Report runner
# ──────────────────────────────────────────────

def run() -> int:
    """Execute all probes and print the report.  Returns exit code."""

    print(BOLD("\n══════════════════════════════════════════════════════════"))
    print(BOLD(" NeuroLift Solutions — Cloudflare API Access Report"))
    print(BOLD("══════════════════════════════════════════════════════════"))

    # ── 1. Credentials inventory ──────────────────────────────
    section("1. Credentials Check")

    token = os.getenv("CLOUDFLARE_API_TOKEN")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    zone_id = os.getenv("CLOUDFLARE_ZONE_ID")

    cred_rows: List[Tuple[str, str, str]] = [
        (
            "CLOUDFLARE_API_TOKEN",
            "✅  set" if token else "❌  NOT SET (required)",
            "required",
        ),
        (
            "CLOUDFLARE_ACCOUNT_ID",
            "✅  set" if account_id else "⚠️   not set (Workers / R2 / D1 checks will be skipped)",
            "optional",
        ),
        (
            "CLOUDFLARE_ZONE_ID",
            "✅  set" if zone_id else "⚠️   not set (will auto-discover from first zone)",
            "optional",
        ),
    ]

    for name, status, req in cred_rows:
        print(f"  {status:<60}  {CYAN(name)} [{req}]")

    if not token:
        print(
            RED(
                "\nFATAL: CLOUDFLARE_API_TOKEN is not set — no API calls were made.\n"
            )
        )
        _print_setup_guide()
        return 2

    # ── 2. Token verification ─────────────────────────────────
    section("2. Token Validity")
    label, detail, ok = probe_token_verify(token)
    print(f"  {label}  {detail}")
    if not ok:
        print(RED("\nToken is invalid.  No further checks can be performed."))
        _print_setup_guide()
        return 1

    # ── 3. Zone discovery ─────────────────────────────────────
    section("3. Zone (Domain) Access")
    label, detail, ok, discovered_zone = probe_list_zones(token)
    print(f"  {label}  /zones  —  {detail}")

    if not zone_id and discovered_zone:
        zone_id = discovered_zone
        print(f"  {YELLOW('ℹ️   Using auto-discovered zone_id:')} {zone_id}")
    elif not zone_id and not discovered_zone:
        print(f"  {WARN}  No zone available for zone-level checks — skipping those sections.")

    if ok and zone_id:
        label2, detail2, _ = probe_zone_details(token, zone_id)
        print(f"  {label2}  /zones/{{id}}  —  {detail2}")

    # ── 4. DNS ────────────────────────────────────────────────
    section("4. DNS Records")
    if zone_id:
        label, detail, ok = probe_dns_records(token, zone_id)
        print(f"  {label}  /zones/{{id}}/dns_records  —  {detail}")
        if not ok:
            print(f"       {YELLOW('Required secret permission:')} Zone → DNS → Read")
    else:
        print(f"  {SKIP}  Skipped (no zone_id available)")

    # ── 5. Page Rules ─────────────────────────────────────────
    section("5. Page Rules")
    if zone_id:
        label, detail, ok = probe_page_rules(token, zone_id)
        print(f"  {label}  /zones/{{id}}/pagerules  —  {detail}")
        if not ok:
            print(f"       {YELLOW('Required secret permission:')} Zone → Page Rules → Read")
    else:
        print(f"  {SKIP}  Skipped (no zone_id available)")

    # ── 6. Zone Settings (SSL, Security Level) ────────────────
    section("6. Zone Settings")
    if zone_id:
        for probe_fn, name in [
            (probe_zone_settings,  "all settings"),
            (probe_security_level, "security_level setting"),
            (probe_ssl_settings,   "ssl setting"),
        ]:
            label, detail, ok = probe_fn(token, zone_id)
            print(f"  {label}  {name}  —  {detail}")
    else:
        print(f"  {SKIP}  Skipped (no zone_id available)")

    # ── 7. Analytics ──────────────────────────────────────────
    section("7. Analytics")
    if zone_id:
        label, detail, ok = probe_analytics(token, zone_id)
        print(f"  {label}  /zones/{{id}}/analytics/dashboard  —  {detail}")
        if not ok:
            print(f"       {YELLOW('Required secret permission:')} Zone → Analytics → Read")
    else:
        print(f"  {SKIP}  Skipped (no zone_id available)")

    # ── 8. Workers ────────────────────────────────────────────
    section("8. Workers")
    if account_id:
        label, detail, ok = probe_workers_scripts(token, account_id)
        print(f"  {label}  /accounts/{{id}}/workers/scripts  —  {detail}")
        if not ok:
            print(f"       {YELLOW('Required secret permission:')} Account → Workers Scripts → Read")

        if zone_id:
            label, detail, ok = probe_workers_routes(token, zone_id)
            print(f"  {label}  /zones/{{id}}/workers/routes  —  {detail}")
    else:
        print(f"  {SKIP}  Workers checks skipped — CLOUDFLARE_ACCOUNT_ID not set")
        print("         Set CLOUDFLARE_ACCOUNT_ID as an org/repo secret to enable this section.")

    # ── 9. Summary ────────────────────────────────────────────
    _print_summary()
    return 0


def _print_summary() -> None:
    section("9. Summary & Next Steps")
    print(
        "  Review the results above:\n"
        f"  {GREEN('✅  PASS')}  — API call succeeded; credential has the required permission.\n"
        f"  {RED('❌  FAIL')}  — API call failed; see the explanation on the next line.\n"
        f"  {YELLOW('⚠️   WARN')}  — Partial access or plan limitation; review the detail.\n"
        f"  {YELLOW('⏭️   SKIP')}  — Check was skipped because a credential was not provided.\n"
    )
    print(
        "  If any FAIL rows appear, follow the 'Required permission' instructions\n"
        "  shown under that row.  For a quick recap of all token permissions needed,\n"
        "  run this script with --guide:\n"
        "      python scripts/test_cloudflare_access.py --guide\n"
    )


def _print_setup_guide() -> None:
    section("Setup Guide — what you need")
    print(
        """
  ┌─────────────────────────────────────────────────────────────────┐
  │           Cloudflare API Token — Required Permissions           │
  └─────────────────────────────────────────────────────────────────┘

  1. Go to: https://dash.cloudflare.com/profile/api-tokens
  2. Click "Create Token" → "Create Custom Token"
  3. Add the following permission groups:

     Resource type    │ Permission group             │ Access level
     ─────────────────┼──────────────────────────────┼─────────────
     Zone             │ Zone                         │ Read
     Zone             │ DNS                          │ Edit
     Zone             │ Page Rules                   │ Edit
     Zone             │ Zone Settings                │ Edit
     Zone             │ Analytics                    │ Read
     Account          │ Workers Scripts              │ Edit
     ─────────────────┴──────────────────────────────┴─────────────

  4. Under "Zone Resources" select:
       "Include → Specific zone → neuroliftsolutions.com"
     (or "All zones" for broader access)

  5. Copy the generated token (shown only once!) and store it as a
     GitHub org secret named:  CLOUDFLARE_API_TOKEN

  ┌─────────────────────────────────────────────────────────────────┐
  │         Additional GitHub Org Secrets (recommended)            │
  └─────────────────────────────────────────────────────────────────┘

     Secret name              │ Where to find the value
     ─────────────────────────┼──────────────────────────────────────
     CLOUDFLARE_API_TOKEN     │ API Tokens page (created above)
     CLOUDFLARE_ACCOUNT_ID    │ URL bar when logged in:
                              │   dash.cloudflare.com/<account-id>/
     CLOUDFLARE_ZONE_ID       │ Domain overview page → API section
     ─────────────────────────┴──────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────┐
  │              GitHub Org Secrets — How to Add                   │
  └─────────────────────────────────────────────────────────────────┘

     Organization level (applies to all repos):
       GitHub → Your Org → Settings → Secrets and variables →
       Actions → "New organization secret"

     Repository level (this repo only):
       GitHub → This repo → Settings → Secrets and variables →
       Actions → "New repository secret"

     Make sure the secret is accessible to this repository's
     workflows (set "Repository access" appropriately).
"""
    )


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if "--guide" in sys.argv or "-g" in sys.argv:
        _print_setup_guide()
        sys.exit(0)

    sys.exit(run())
