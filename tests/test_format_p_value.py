"""Offline acceptance checks for the journal-independent P-value formatter."""

import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = (Path(__file__).resolve().parents[1] / "skills" / "evidence-first-medical-writing"
          / "scripts" / "format_p_value.py")


class PValueFormatting(unittest.TestCase):
    def cli(self, value, *flags):
        return subprocess.run([sys.executable, "-IB", str(SCRIPT), "--unrounded", value, *flags],
                              capture_output=True, text=True, timeout=5)

    def test_classify_before_rounding_keep_three_places(self):
        for value, expected in {
            "1e-300": "< 0.001",
            "0.00099999999999999999999999": "< 0.001",
            "0.001": "= 0.001",
            ".0400": "= 0.040",
            ".0496": "= 0.050",
            ".1205": "= 0.121",
            ".99899": "= 0.999",
            ".999": "= 0.999",
            ".99900000000000000000000001": "> 0.999",
            ".99999999999999999999999999": "> 0.999",
        }.items():
            with self.subTest(value=value):
                result = self.cli(value)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), f"P {expected}")

    def test_confirmed_one(self):
        result = self.cli("1.000", "--exact-one")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "P = 1.000")

    def test_insufficient_or_contradictory_evidence(self):
        for value, flags in [
            ("1.000", []), ("< 0.05", []), ("NaN", []), ("Infinity", []), ("-0.4", []),
            ("1.1", []), (".9999", ["--exact-one"]),
        ]:
            with self.subTest(value=value, flags=flags):
                result = self.cli(value, *flags)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(result.stdout.strip())
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
