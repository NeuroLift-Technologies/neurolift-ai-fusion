#!/usr/bin/env python3
"""
validate_provenance.py — NLT CI Harness: PGSA Provenance Validator
===================================================================
Discovers provenance manifests in the repository and validates them against:
  1. Required schema fields.
  2. PGSA whitelist — approved package/tool origins.
  3. PGSA blacklist — explicitly forbidden package/tool origins.

A provenance manifest is a JSON file matching the glob ``**/provenance.json``
or ``**/*.provenance.json``.  It must conform to the schema described in
``docs/CI_HARNESS_README.md``.

Exit codes:
  0 — all manifests valid and no blacklist violations
  1 — validation failures detected
  2 — argument/configuration error
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set

log = logging.getLogger(__name__)

DEFAULT_REPORT_DIR = Path("clearance-reports")
DEFAULT_CONFIG_PATH = Path("config/pgsa-allowlists.json")

# ---------------------------------------------------------------------------
# Default PGSA allow/deny lists (overridden by --config)
# ---------------------------------------------------------------------------

DEFAULT_WHITELIST: List[str] = [
    "github.com",
    "pypi.org",
    "npmjs.com",
    "registry.npmjs.org",
    "hub.docker.com",
]

DEFAULT_BLACKLIST: List[str] = [
    "untrusted-registry.example.com",
    "malware-source.example.com",
]

# ---------------------------------------------------------------------------
# Required top-level fields in a provenance manifest
# ---------------------------------------------------------------------------

REQUIRED_FIELDS: List[str] = [
    "schema_version",
    "component",
    "version",
    "source",
    "build_system",
]


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class ManifestViolation:
    manifest_path: str
    violation_type: str  # "missing_field" | "blacklisted_source" | "parse_error"
    detail: str


@dataclass
class ValidationReport:
    generated_at: str
    scan_root: str
    manifests_found: int = 0
    manifests_valid: int = 0
    violations: List[ManifestViolation] = field(default_factory=list)
    whitelist: List[str] = field(default_factory=list)
    blacklist: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.violations


# ---------------------------------------------------------------------------
# Manifest discovery
# ---------------------------------------------------------------------------

# Allowable glob patterns for provenance manifests.
# Restricted to known filename patterns to avoid traversing into unexpected
# directories (e.g. .git, node_modules).
MANIFEST_GLOBS = [
    "**/provenance.json",
    "**/*.provenance.json",
]

# Directories to skip during discovery
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".tox"}


def _discover_manifests(root: Path) -> List[Path]:
    """Return provenance manifests under *root*, skipping excluded dirs."""
    found: List[Path] = []
    for pattern in MANIFEST_GLOBS:
        for candidate in root.glob(pattern):
            # Reject paths that traverse into excluded directories
            if any(part in SKIP_DIRS for part in candidate.parts):
                log.debug("Skipping excluded path: %s", candidate)
                continue
            # Ensure the path is actually within the root (no traversal)
            try:
                candidate.resolve().relative_to(root.resolve())
            except ValueError:
                log.warning("Path traversal rejected: %s", candidate)
                continue
            found.append(candidate)
    # Deduplicate while preserving order
    seen: Set[Path] = set()
    unique: List[Path] = []
    for p in found:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def _load_pgsa_config(config_path: Path) -> tuple[List[str], List[str]]:
    """Load whitelist/blacklist from *config_path* (JSON)."""
    if not config_path.is_file():
        log.debug("PGSA config not found at '%s'; using defaults.", config_path)
        return list(DEFAULT_WHITELIST), list(DEFAULT_BLACKLIST)

    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Failed to load PGSA config '%s': %s — using defaults.", config_path, exc)
        return list(DEFAULT_WHITELIST), list(DEFAULT_BLACKLIST)

    whitelist = raw.get("whitelist", DEFAULT_WHITELIST)
    blacklist = raw.get("blacklist", DEFAULT_BLACKLIST)

    if not isinstance(whitelist, list) or not isinstance(blacklist, list):
        log.warning("PGSA config has unexpected structure — using defaults.")
        return list(DEFAULT_WHITELIST), list(DEFAULT_BLACKLIST)

    return [str(e) for e in whitelist], [str(e) for e in blacklist]


def _validate_manifest(
    path: Path,
    whitelist: List[str],
    blacklist: List[str],
) -> List[ManifestViolation]:
    """Validate a single provenance manifest and return any violations."""
    violations: List[ManifestViolation] = []
    rel_path = str(path)

    try:
        content: Any = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        violations.append(
            ManifestViolation(
                manifest_path=rel_path,
                violation_type="parse_error",
                detail=str(exc),
            )
        )
        return violations

    if not isinstance(content, dict):
        violations.append(
            ManifestViolation(
                manifest_path=rel_path,
                violation_type="parse_error",
                detail="Manifest root must be a JSON object.",
            )
        )
        return violations

    manifest: Dict[str, Any] = content

    # 1. Schema: required fields
    for req in REQUIRED_FIELDS:
        if req not in manifest:
            violations.append(
                ManifestViolation(
                    manifest_path=rel_path,
                    violation_type="missing_field",
                    detail=f"Required field '{req}' is absent.",
                )
            )

    # 2. Source origin checks
    source = str(manifest.get("source", ""))

    for blocked in blacklist:
        if blocked and blocked.lower() in source.lower():
            violations.append(
                ManifestViolation(
                    manifest_path=rel_path,
                    violation_type="blacklisted_source",
                    detail=f"Source '{source}' matches blacklisted origin '{blocked}'.",
                )
            )

    # 3. Whitelist advisory (warn, do not fail)
    if source and not any(w.lower() in source.lower() for w in whitelist):
        log.warning(
            "Manifest '%s': source '%s' is not on the PGSA whitelist (advisory only).",
            rel_path,
            source,
        )

    return violations


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def write_report(report: ValidationReport, report_dir: Path, fmt: str) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if fmt == "json":
        payload = asdict(report)
        path = report_dir / f"provenance-report-{timestamp}.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        status = "✅ PASSED" if report.passed else "❌ FAILED"
        lines: List[str] = [
            f"# Provenance Validation Report — {timestamp}",
            "",
            f"**Status:** {status}",
            f"**Scan root:** `{report.scan_root}`",
            f"**Manifests found:** {report.manifests_found}",
            f"**Valid manifests:** {report.manifests_valid}",
            "",
        ]
        if report.violations:
            lines += [
                f"## {len(report.violations)} Violation(s)",
                "",
                "| Manifest | Type | Detail |",
                "| -------- | ---- | ------ |",
            ]
            for v in report.violations:
                lines.append(
                    f"| `{v.manifest_path}` | `{v.violation_type}` | {v.detail} |"
                )
        else:
            lines.append("All manifests passed validation.")

        path = report_dir / f"provenance-report-{timestamp}.md"
        path.write_text("\n".join(lines), encoding="utf-8")

    log.info("Report written → %s", path)
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--scan-root",
        type=Path,
        default=Path("."),
        help="Root directory to scan for provenance manifests (default: CWD).",
    )
    p.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to PGSA allowlists JSON config (default: %(default)s).",
    )
    p.add_argument(
        "--report-dir",
        type=Path,
        default=DEFAULT_REPORT_DIR,
        help="Directory for output reports (default: %(default)s).",
    )
    p.add_argument(
        "--report-format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: %(default)s).",
    )
    p.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug logging.",
    )
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    scan_root = args.scan_root.resolve()
    if not scan_root.is_dir():
        log.error("--scan-root '%s' is not a directory.", scan_root)
        return 2

    config_path = args.config.resolve() if args.config else DEFAULT_CONFIG_PATH
    whitelist, blacklist = _load_pgsa_config(config_path)

    log.info("Discovering provenance manifests under: %s", scan_root)
    manifests = _discover_manifests(scan_root)
    log.info("Found %d manifest(s)", len(manifests))

    report = ValidationReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        scan_root=str(scan_root),
        manifests_found=len(manifests),
        whitelist=whitelist,
        blacklist=blacklist,
    )

    for manifest_path in manifests:
        log.info("Validating: %s", manifest_path)
        violations = _validate_manifest(manifest_path, whitelist, blacklist)
        if violations:
            report.violations.extend(violations)
        else:
            report.manifests_valid += 1

    write_report(report, args.report_dir, args.report_format)

    if report.passed:
        if manifests:
            log.info("✅ All %d provenance manifest(s) are valid.", len(manifests))
        else:
            log.info("✅ No provenance manifests found; nothing to validate.")
        return 0
    else:
        log.error(
            "❌ %d violation(s) found across %d manifest(s).",
            len(report.violations),
            len(manifests),
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
