#!/usr/bin/env python3
"""
run_clearance_tests.py — NLT Red Team CI Harness
=================================================
Implements a 3-tier clearance rubric for CI submissions:
  Level 1 (Basic)    — syntax checks, unit tests, linting
  Level 2 (Standard) — integration tests, coverage thresholds
  Level 3 (Full)     — end-to-end tests, security baseline checks

Exit codes:
  0 — all required levels passed
  1 — one or more required levels failed
  2 — argument/configuration error
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Sequence

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

CLEARANCE_LEVELS = (1, 2, 3)
DEFAULT_LEVEL = 1
DEFAULT_REPORT_DIR = Path("clearance-reports")

log = logging.getLogger(__name__)


@dataclass
class StepResult:
    name: str
    command: List[str]
    returncode: int
    stdout: str
    stderr: str
    duration_s: float

    @property
    def passed(self) -> bool:
        return self.returncode == 0


@dataclass
class LevelReport:
    level: int
    steps: List[StepResult] = field(default_factory=list)
    started_at: str = ""
    finished_at: Optional[str] = None

    @property
    def passed(self) -> bool:
        return all(s.passed for s in self.steps)

    @property
    def failed_steps(self) -> List[StepResult]:
        return [s for s in self.steps if not s.passed]


# ---------------------------------------------------------------------------
# Step definitions per clearance level
# ---------------------------------------------------------------------------

# Each entry is (step_name, argv).  Paths are relative to the repo root and
# must not contain shell metacharacters — they are passed directly to
# subprocess without shell=True.
LEVEL_STEPS: dict[int, List[tuple[str, List[str]]]] = {
    1: [
        (
            "syntax-check",
            [sys.executable, "-m", "py_compile"],
        ),
        (
            "lint-errors",
            [
                sys.executable,
                "-m",
                "flake8",
                "src",
                "scripts",
                "--count",
                "--select=E9,F63,F7,F82",
                "--show-source",
                "--statistics",
            ],
        ),
        (
            "unit-tests",
            [sys.executable, "-m", "pytest", "tests/", "--tb=short", "-q"],
        ),
    ],
    2: [
        (
            "coverage",
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "--tb=short",
                "-q",
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-fail-under=60",
            ],
        ),
        (
            "type-check",
            [sys.executable, "-m", "mypy", "src", "--ignore-missing-imports"],
        ),
    ],
    3: [
        (
            "secret-scan",
            [sys.executable, "scripts/scan_secrets.py", "--fail-on-findings"],
        ),
        (
            "provenance-check",
            [sys.executable, "scripts/validate_provenance.py"],
        ),
    ],
}

# Level 1 steps are synthesised per-file; for the syntax check we scan all
# Python source files found under src/ and scripts/.
PYTHON_SOURCE_DIRS = ["src", "scripts"]


def _collect_python_files(repo_root: Path) -> List[Path]:
    """Return all .py files under PYTHON_SOURCE_DIRS relative to repo_root."""
    files: List[Path] = []
    for d in PYTHON_SOURCE_DIRS:
        target = repo_root / d
        if target.is_dir():
            files.extend(target.rglob("*.py"))
    return files


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def run_step(
    name: str,
    argv: List[str],
    repo_root: Path,
    timeout: int,
) -> StepResult:
    """Execute a single step and return its result."""
    log.info("  → running step: %s", name)
    log.debug("    command: %s", argv)

    start = time.monotonic()
    try:
        proc = subprocess.run(  # noqa: S603 — argv is a list, no shell expansion
            argv,
            capture_output=True,
            text=True,
            cwd=repo_root,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - start
        log.warning("  ✗ step '%s' timed out after %ds", name, timeout)
        return StepResult(
            name=name,
            command=argv,
            returncode=1,
            stdout="",
            stderr=f"Timed out after {timeout}s",
            duration_s=elapsed,
        )
    except FileNotFoundError as exc:
        elapsed = time.monotonic() - start
        log.error("  ✗ step '%s' — executable not found: %s", name, exc)
        return StepResult(
            name=name,
            command=argv,
            returncode=1,
            stdout="",
            stderr=str(exc),
            duration_s=elapsed,
        )

    elapsed = time.monotonic() - start
    status = "✓" if proc.returncode == 0 else "✗"
    log.info("  %s step '%s' exited %d (%.1fs)", status, name, proc.returncode, elapsed)
    return StepResult(
        name=name,
        command=argv,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        duration_s=elapsed,
    )


def run_level(level: int, repo_root: Path, timeout: int) -> LevelReport:
    """Execute all steps for a given clearance level."""
    report = LevelReport(
        level=level,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    log.info("▶ Clearance Level %d", level)

    # Level 1 syntax check: collect all .py files and pass them together
    if level == 1:
        py_files = _collect_python_files(repo_root)
        steps: List[tuple[str, List[str]]] = []
        for s_name, s_cmd in LEVEL_STEPS[1]:
            if s_name == "syntax-check":
                if py_files:
                    steps.append(
                        ("syntax-check", s_cmd + [str(f) for f in py_files])
                    )
                else:
                    log.warning("No Python source files found to syntax-check.")
            else:
                steps.append((s_name, s_cmd))
    else:
        steps = list(LEVEL_STEPS.get(level, []))

    for step_name, argv in steps:
        result = run_step(step_name, argv, repo_root, timeout)
        report.steps.append(result)

    report.finished_at = datetime.now(timezone.utc).isoformat()

    if report.passed:
        log.info("✅ Level %d PASSED", level)
    else:
        failed = ", ".join(s.name for s in report.failed_steps)
        log.error("❌ Level %d FAILED — failing steps: %s", level, failed)

    return report


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def _to_serialisable(obj: object) -> object:
    """Recursively convert dataclasses and lists for json.dumps."""
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _to_serialisable(v) for k, v in asdict(obj).items()}  # type: ignore[arg-type]
    if isinstance(obj, list):
        return [_to_serialisable(i) for i in obj]
    return obj


def write_report(
    reports: List[LevelReport],
    report_dir: Path,
    fmt: str,
) -> Path:
    """Persist the clearance report to *report_dir*."""
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if fmt == "json":
        payload = {
            "generated_at": timestamp,
            "overall_pass": all(r.passed for r in reports),
            "levels": [_to_serialisable(r) for r in reports],
        }
        path = report_dir / f"clearance-report-{timestamp}.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    else:
        lines: List[str] = [
            f"# Clearance Report — {timestamp}",
            "",
        ]
        overall = all(r.passed for r in reports)
        lines.append(f"**Overall:** {'PASS ✅' if overall else 'FAIL ❌'}")
        lines.append("")
        for r in reports:
            status = "PASS ✅" if r.passed else "FAIL ❌"
            lines += [
                f"## Level {r.level} — {status}",
                "",
                "| Step | Result | Duration |",
                "| ---- | ------ | -------- |",
            ]
            for s in r.steps:
                icon = "✅" if s.passed else "❌"
                lines.append(
                    f"| `{s.name}` | {icon} `{s.returncode}` | {s.duration_s:.1f}s |"
                )
            if r.failed_steps:
                lines += ["", "### Failures", ""]
                for s in r.failed_steps:
                    lines += [
                        f"#### `{s.name}`",
                        "```",
                        s.stderr.strip() or s.stdout.strip(),
                        "```",
                        "",
                    ]
            lines.append("")
        path = report_dir / f"clearance-report-{timestamp}.md"
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
        "--level",
        type=int,
        choices=CLEARANCE_LEVELS,
        default=DEFAULT_LEVEL,
        help="Maximum clearance level to run (default: %(default)s). "
        "All levels from 1 up to this value are executed.",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root (default: current directory).",
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
        "--timeout",
        type=int,
        default=300,
        help="Per-step timeout in seconds (default: %(default)s).",
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

    repo_root = args.repo_root.resolve()
    if not repo_root.is_dir():
        log.error("--repo-root '%s' is not a directory.", repo_root)
        return 2

    if args.timeout < 1:
        log.error("--timeout must be >= 1 second.")
        return 2

    reports: List[LevelReport] = []
    for lvl in range(1, args.level + 1):
        report = run_level(lvl, repo_root, args.timeout)
        reports.append(report)
        if not report.passed:
            log.error(
                "Stopping: level %d failed. Higher levels will not run.", lvl
            )
            break

    write_report(reports, args.report_dir, args.report_format)

    overall_pass = all(r.passed for r in reports)
    if overall_pass:
        log.info("All clearance levels PASSED.")
        return 0
    else:
        log.error("One or more clearance levels FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
