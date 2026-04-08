from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExampleScriptTests(unittest.TestCase):
    def test_basic_roundtrip_example_runs(self) -> None:
        result = subprocess.run(
            [sys.executable, "examples/basic_roundtrip.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertIn("compression_ratio", payload)
        self.assertGreater(payload["compression_ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()
