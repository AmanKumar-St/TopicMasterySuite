"""
JSEvaluator: Node.js subprocess execution engine for JavaScript testing.
Runs user code alongside deterministic test suites and returns structured execution results.
"""

import json
import os
import subprocess
import tempfile
from typing import Any, Dict, Optional


class JSEvaluator:
    def __init__(self, node_path: str = "node", timeout_seconds: int = 10):
        self.node_path = node_path
        self.timeout_seconds = timeout_seconds

    def evaluate(self, student_code: str, test_suite_code: str) -> Dict[str, Any]:
        """
        Executes student code together with a test harness in Node.js.
        Returns a dictionary with status, passed tests, failed tests, logs, and errors.
        """
        # Wrap everything in a sandbox harness that catches unhandled errors and emits JSON results
        harness = f"""
// === STUDENT CODE START ===
{student_code}
// === STUDENT CODE END ===

// === TEST HARNESS START ===
(async () => {{
    const __results = {{
        total: 0,
        passed: 0,
        failed: 0,
        tests: [],
        logs: [],
        error: null
    }};

    const originalLog = console.log;
    const originalError = console.error;
    console.log = (...args) => {{
        __results.logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '));
    }};
    console.error = (...args) => {{
        __results.logs.push('[STDERR] ' + args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' '));
    }};

    async function test(name, fn) {{
        __results.total++;
        try {{
            await fn();
            __results.passed++;
            __results.tests.push({{ name, passed: true, error: null }});
        }} catch (err) {{
            __results.failed++;
            __results.tests.push({{ name, passed: false, error: err.message || String(err) }});
        }}
    }}

    function assert(condition, message) {{
        if (!condition) throw new Error(message || 'Assertion failed');
    }}

    function assertEqual(actual, expected, message) {{
        const actStr = JSON.stringify(actual);
        const expStr = JSON.stringify(expected);
        if (actStr !== expStr) {{
            throw new Error((message ? message + ': ' : '') + `Expected ${{expStr}}, but got ${{actStr}}`);
        }}
    }}

    try {{
        {test_suite_code}
    }} catch (harnessErr) {{
        __results.error = harnessErr.stack || harnessErr.message || String(harnessErr);
    }}

    process.stdout.write('__JSON_START__' + JSON.stringify(__results) + '__JSON_END__');
}})().catch(err => {{
    process.stdout.write('__JSON_START__' + JSON.stringify({{
        total: 0,
        passed: 0,
        failed: 1,
        tests: [{{ name: 'Global Execution', passed: false, error: err.message || String(err) }}],
        logs: [],
        error: err.stack || err.message || String(err)
    }}) + '__JSON_END__');
}});
"""
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cjs', delete=False, encoding='utf-8') as f:
                f.write(harness)
                temp_file = f.name

            proc = subprocess.run(
                [self.node_path, temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                encoding='utf-8',
                errors='replace'
            )

            stdout = proc.stdout or ""
            stderr = proc.stderr or ""

            if "__JSON_START__" in stdout and "__JSON_END__" in stdout:
                json_str = stdout.split("__JSON_START__")[1].split("__JSON_END__")[0]
                res = json.loads(json_str)
                res["returncode"] = proc.returncode
                res["raw_stderr"] = stderr
                return res
            else:
                return {
                    "total": 0,
                    "passed": 0,
                    "failed": 1,
                    "tests": [{"name": "Execution Check", "passed": False, "error": stderr or stdout or "No output"}],
                    "logs": [stdout] if stdout else [],
                    "error": stderr or "Failed to parse structured test output.",
                    "returncode": proc.returncode,
                    "raw_stderr": stderr
                }

        except subprocess.TimeoutExpired:
            return {
                "total": 0,
                "passed": 0,
                "failed": 1,
                "tests": [{"name": "Timeout", "passed": False, "error": f"Execution timed out after {self.timeout_seconds}s (possible infinite loop)"}],
                "logs": [],
                "error": f"Execution timed out after {self.timeout_seconds} seconds.",
                "returncode": -1,
                "raw_stderr": ""
            }
        except Exception as e:
            return {
                "total": 0,
                "passed": 0,
                "failed": 1,
                "tests": [{"name": "System Execution Error", "passed": False, "error": str(e)}],
                "logs": [],
                "error": str(e),
                "returncode": -1,
                "raw_stderr": ""
            }
        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass


if __name__ == "__main__":
    evaluator = JSEvaluator()
    student = "function add(a, b) { return a + b; }"
    tests = "await test('adds 1+2', () => assertEqual(add(1, 2), 3));"
    result = evaluator.evaluate(student, tests)
    print("Test Result:", json.dumps(result, indent=2))
