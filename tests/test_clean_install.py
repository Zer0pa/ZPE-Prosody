from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CleanInstallTests(unittest.TestCase):
    def test_release_surface_base_scenario(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_release_surface.py", "--scenario", "base"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("base: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
