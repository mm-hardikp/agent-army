import os
import sys
import json
import tempfile
import unittest
from pathlib import Path

# Add tools directory to path
tools_path = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_path))

from scan_ast import scan_directory, SymbolExtractor


class TestScanAst(unittest.TestCase):
    def test_scan_python_symbols(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_py = Path(tmpdir) / "sample.py"
            test_py.write_text('''
class Calculator:
    def add(self, a, b):
        return a + b

def standalone_func(x):
    return x * 2
''', encoding="utf-8")

            symbols = SymbolExtractor.extract_python_symbols(test_py)
            names = [s["name"] for s in symbols]
            self.assertIn("Calculator", names)
            self.assertIn("standalone_func", names)
            
            calc_sym = next(s for s in symbols if s["name"] == "Calculator")
            self.assertIn("add", calc_sym["methods"])

    def test_scan_js_ts_symbols(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_ts = Path(tmpdir) / "sample.ts"
            test_ts.write_text('''
export function fetchUser(id: string) {
    return { id };
}

export class UserService {
    getUser() {}
}
''', encoding="utf-8")

            symbols = SymbolExtractor.extract_js_ts_symbols(test_ts)
            names = [s["name"] for s in symbols]
            self.assertIn("fetchUser", names)
            self.assertIn("UserService", names)

    def test_scan_manifest_detection(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pkg_json = Path(tmpdir) / "package.json"
            pkg_json.write_text('{"name": "test-pkg"}', encoding="utf-8")
            
            req_txt = Path(tmpdir) / "requirements.txt"
            req_txt.write_text('pytest>=8.0.0', encoding="utf-8")

            res = scan_directory(Path(tmpdir))
            manifest_files = [m["file"] for m in res["manifests"]]
            self.assertIn("package.json", manifest_files)
            self.assertIn("requirements.txt", manifest_files)


if __name__ == "__main__":
    unittest.main()
