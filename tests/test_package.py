"""Baseline smoke test: proves the package imports and the test toolchain works
before any feature code exists. See docs/NEXT-STEPS.md #4 for the green baseline
this test defines."""

import unittest


class TestPackageImports(unittest.TestCase):
    def test_package_has_a_version(self):
        import csvkit

        self.assertTrue(hasattr(csvkit, "__version__"))
        self.assertEqual(csvkit.__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
