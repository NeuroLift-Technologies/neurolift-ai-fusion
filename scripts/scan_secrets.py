#!/usr/bin/env python3
"""
scan_secrets.py — NLT CI Harness: Unified Secrets Scanner
==========================================================
Wraps Gitleaks and/or TruffleHog CLIs to produce a unified secrets report.
Only one tool needs to be installed; the script degrades gracefully when a
tool is missing.

Exit codes:
  0 — no secrets detected (or all tools unavailable)
  1 — secrets detected and --fail-on-findings is set
  2 — argument/configuration error
"""

from __future__ import annotations

import argparse
import json
import logging
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Sequence

log = logging.getLogger(__name__)

DEFAULT_REPORT_DIR = Path("clearance-reports")
GITLEAKS_CONFIG_PATH = Path(".github/gitleaks.toml")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    tool: str
    rule_id: str
    description: str
    file: str
    line: int
    commit: str
    secret_preview: str  # truncated — never store the full secret


@dataclass
class ScanReport:
    generated_at: str
    scan_path: str
    tools_run: List[str] = field(default_factory=list)
    tools_unavailable: List[str] = field(default_factory=list)
    findings: List[Finding] = field(default_factory=list)

    @property
    def has_findings(self) -> bool:
        return bool(self.findings)


# ---------------------------------------------------------------------------
# Tool runners
# ---------------------------------------------------------------------------


def _tool_available(name: str) -> bool:
    return shutil.which(name) is not None


def _run_gitleaks(scan_path: Path, config_path: Optional[Path]) -> List[Finding]:
    """Run Gitleaks against *scan_path* and return parsed findings."""
    if not _tool_available("gitleaks"):
        log.warning("gitleaks not found in PATH — skipping")
        return []

    with tempfile.NamedTemporaryFile(
        suffix=".json", delete=False, mode="w"
    ) as report_file:
        report_path = Path(report_file.name)

    argv: List[str] = [
        "gitleaks",
        "detect",
        "--source",
        str(scan_path),
        "--report-format",
        "json",
        "--report-path",
        str(report_path),
        "--no-banner",
        "--exit-code",
        "0",  # we control exit behaviour ourselves
    ]

    if config_path and config_path.is_file():
        argv += ["--config", str(config_path)]

    log.info("Running gitleaks: %s", shlex.join(argv))
    try:
        proc = subprocess.run(  # noqa: S603 — list argv, no shell expansion
            argv,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        log.error("gitleaks timed out")
        return []
    except FileNotFoundError as exc:
        log.error("gitleaks executable error: %s", exc)
        return []

    if proc.returncode not in (0, 1):
        log.warning(
            "gitleaks exited %d; stderr: %s", proc.returncode, proc.stderr[:500]
        )

    findings: List[Finding] = []
    if report_path.exists():
        try:
            raw = json.loads(report_path.read_text(encoding="utf-8"))
            if isinstance(raw, list):
                for item in raw:
                    secret = item.get("Secret", "") or ""
                    findings.append(
                        Finding(
                            tool="gitleaks",
                            rule_id=item.get("RuleID", "unknown"),
                            description=item.get("Description", ""),
                            file=item.get("File", ""),
                            line=item.get("StartLine", 0),
                            commit=item.get("Commit", ""),
                            secret_preview=secret[:8] + "***" if secret else "",
                        )
                    )
        except (json.JSONDecodeError, KeyError) as exc:
            log.warning("Failed to parse gitleaks output: %s", exc)
        finally:
            report_path.unlink(missing_ok=True)

    log.info("gitleaks: %d finding(s)", len(findings))
    return findings


def _run_trufflehog(scan_path: Path) -> List[Finding]:
    """Run TruffleHog against *scan_path* and return parsed findings."""
    if not _tool_available("trufflehog"):
        log.warning("trufflehog not found in PATH — skipping")
        return []

    # Use filesystem mode with JSON output
    argv: List[str] = [
        "trufflehog",
        "filesystem",
        str(scan_path),
        "--json",
        "--no-update",
    ]

    log.info("Running trufflehog: %s", shlex.join(argv))
    try:
        proc = subprocess.run(  # noqa: S603 — list argv, no shell expansion
            argv,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        log.error("trufflehog timed out")
        return []
    except FileNotFoundError as exc:
        log.error("trufflehog executable error: %s", exc)
        return []

    findings: List[Finding] = []
    # TruffleHog emits one JSON object per line
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue

        raw_secret = (
            item.get("Raw", "") or item.get("RawV2", "") or ""
        )
        findings.append(
            Finding(
                tool="trufflehog",
                rule_id=item.get("DetectorName", "unknown"),
                description=item.get("DetectorName", ""),
                file=item.get("SourceMetadata", {})
                .get("Data", {})
                .get("Filesystem", {})
                .get("file", ""),
                line=0,
                commit="",
                secret_preview=raw_secret[:8] + "***" if raw_secret else "",
            )
        )

    log.info("trufflehog: %d finding(s)", len(findings))
    return findings


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def write_report(report: ScanReport, report_dir: Path, fmt: str) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if fmt == "json":
        payload = asdict(report)
        path = report_dir / f"secrets-report-{timestamp}.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        status = "🚨 FINDINGS DETECTED" if report.has_findings else "✅ CLEAN"
        lines: List[str] = [
            f"# Secrets Scan Report — {timestamp}",
            "",
            f"**Status:** {status}",
            f"**Scanned path:** `{report.scan_path}`",
            f"**Tools run:** {', '.join(report.tools_run) or '(none)'}",
        ]
        if report.tools_unavailable:
            lines.append(
                f"**Tools unavailable:** {', '.join(report.tools_unavailable)}"
            )
        lines.append("")
        if report.findings:
            lines += [
                f"## {len(report.findings)} Finding(s)",
                "",
                "| Tool | Rule | File | Line | Preview |",
                "| ---- | ---- | ---- | ---- | ------- |",
            ]
            for f in report.findings:
                lines.append(
                    f"| {f.tool} | `{f.rule_id}` | `{f.file}` "
                    f"| {f.line} | `{f.secret_preview}` |"
                )
        else:
            lines.append("No secrets detected.")

        path = report_dir / f"secrets-report-{timestamp}.md"
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
        "--scan-path",
        type=Path,
        default=Path("."),
        help="Root path to scan (default: current directory).",
    )
    p.add_argument(
        "--gitleaks-config",
        type=Path,
        default=GITLEAKS_CONFIG_PATH,
        help="Path to Gitleaks config file (default: %(default)s).",
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
        "--fail-on-findings",
        action="store_true",
        help="Exit 1 when secrets are found.",
    )
    p.add_argument(
        "--skip-gitleaks",
        action="store_true",
        help="Skip Gitleaks even if installed.",
    )
    p.add_argument(
        "--skip-trufflehog",
        action="store_true",
        help="Skip TruffleHog even if installed.",
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

    scan_path = args.scan_path.resolve()
    if not scan_path.exists():
        log.error("--scan-path '%s' does not exist.", scan_path)
        return 2

    report = ScanReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        scan_path=str(scan_path),
    )

    all_findings: List[Finding] = []

    # --- Gitleaks ---
    if not args.skip_gitleaks:
        if _tool_available("gitleaks"):
            report.tools_run.append("gitleaks")
            all_findings.extend(
                _run_gitleaks(scan_path, args.gitleaks_config)
            )
        else:
            report.tools_unavailable.append("gitleaks")
            log.warning("gitleaks is not installed.")

    # --- TruffleHog ---
    if not args.skip_trufflehog:
        if _tool_available("trufflehog"):
            report.tools_run.append("trufflehog")
            all_findings.extend(_run_trufflehog(scan_path))
        else:
            report.tools_unavailable.append("trufflehog")
            log.warning("trufflehog is not installed.")

    if not report.tools_run:
        log.warning(
            "No scanning tools were available. Install gitleaks or trufflehog."
        )

    report.findings = all_findings
    write_report(report, args.report_dir, args.report_format)

    if report.has_findings:
        log.error("🚨 %d secret(s) detected.", len(report.findings))
        if args.fail_on_findings:
            return 1
    else:
        log.info("✅ No secrets detected.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
