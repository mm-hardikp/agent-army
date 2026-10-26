import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add tools directory to path
tools_path = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_path))

from lint_ast import lint_file, check_python_native


class TestLintAst(unittest.TestCase):
    def test_python_syntax_valid(self):
        code = '''
def greet(name: str) -> str:
    return f"Hello {name}"
'''
        passed, errors = check_python_native(code, "valid.py")
        self.assertTrue(passed)
        self.assertEqual(len(errors), 0)

    def test_python_syntax_invalid(self):
        code = '''
def broken_syntax(
    return "unclosed paren"
'''
        passed, errors = check_python_native(code, "broken.py")
        self.assertFalse(passed)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("SyntaxError" in e for e in errors))

    def test_lint_file_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            f = Path(tmpdir) / "module.py"
            f.write_text("print('clean python')\n", encoding="utf-8")
            res = lint_file(f)
            self.assertTrue(res["passed"])
            self.assertEqual(res["engine"], "python_ast_native")

    def test_lint_file_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            f = Path(tmpdir) / "broken.py"
            f.write_text("def missing_colon()\n    pass\n", encoding="utf-8")
            res = lint_file(f)
            self.assertFalse(res["passed"])
            self.assertGreater(len(res["errors"]), 0)

    def test_compiler_fallback_for_unknown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            f = Path(tmpdir) / "script.custom"
            f.write_text("some custom text", encoding="utf-8")
            res = lint_file(f)
            self.assertTrue(res["passed"])
            self.assertIn("native_compiler_fallback", res["engine"])


if __name__ == "__main__":
    unittest.main()
