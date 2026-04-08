"""Build the package and verify clean installation scenarios from the wheel."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=["all", "api", "base", "benchmarks"],
        default="all",
        help="Installation scenario to verify.",
    )
    return parser.parse_args()


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def preferred_python() -> str:
    return shutil.which("python3.11") or sys.executable


def bootstrap_tooling(work_dir: Path) -> tuple[Path, str]:
    base_python = preferred_python()
    tooling_dir = work_dir / "tooling-venv"
    run([base_python, "-m", "venv", str(tooling_dir)])
    python = python_bin(tooling_dir)
    run([str(python), "-m", "pip", "install", "--upgrade", "pip", "build"])
    return python, base_python


def build_wheel(build_python: Path, dist_dir: Path) -> Path:
    run([str(build_python), "-m", "build", "--sdist", "--wheel", "--outdir", str(dist_dir)], cwd=ROOT)
    wheels = sorted(dist_dir.glob("*.whl"))
    if not wheels:
        raise RuntimeError("No wheel produced by build")
    return wheels[-1]


def direct_ref(wheel_path: Path, extra: str | None = None) -> str:
    if not extra:
        return wheel_path.as_uri()
    return f"zpe-prosody[{extra}] @ {wheel_path.as_uri()}"


def python_bin(venv_dir: Path) -> Path:
    return venv_dir / "bin" / "python"


def verify_scenario(
    dist_dir: Path,
    wheel_path: Path,
    base_python: str,
    scenario: str,
    extra: str | None,
    imports: list[str],
) -> None:
    venv_dir = dist_dir / f"venv-{scenario}"
    run([base_python, "-m", "venv", str(venv_dir)])
    python = python_bin(venv_dir)
    run([str(python), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(python), "-m", "pip", "install", direct_ref(wheel_path, extra)])
    for statement in imports:
        run([str(python), "-c", statement])
    print(f"{scenario}: PASS")


def selected_scenarios(arg: str) -> list[tuple[str, str | None, list[str]]]:
    scenarios = {
        "base": ("base", None, ["import zpe_prosody"]),
        "api": ("api", "api", ["import zpe_prosody", "import fastapi", "import uvicorn"]),
        "benchmarks": (
            "benchmarks",
            "benchmarks",
            ["import zpe_prosody", "import numpy"],
        ),
    }
    if arg == "all":
        return [scenarios["base"], scenarios["api"], scenarios["benchmarks"]]
    return [scenarios[arg]]


def main() -> None:
    args = parse_args()
    with tempfile.TemporaryDirectory(prefix="zpe-prosody-release-") as tmp:
        work_dir = Path(tmp)
        build_python, base_python = bootstrap_tooling(work_dir)
        dist_dir = work_dir / "dist"
        dist_dir.mkdir(parents=True, exist_ok=True)
        wheel = build_wheel(build_python, dist_dir)
        if not wheel.exists():
            raise RuntimeError("Wheel path missing after build")
        for scenario, extra, imports in selected_scenarios(args.scenario):
            verify_scenario(dist_dir, wheel, base_python, scenario, extra, imports)


if __name__ == "__main__":
    main()
