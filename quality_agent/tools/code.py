# quality_agent/tools/code.py

import subprocess
import tempfile
import os

VLLM_BASE_URL = "http://localhost:8050/v1"
VLLM_MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def run_code(code: str, timeout: int = 15) -> dict:
    """Write code to a temp file and execute it in a subprocess."""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["python", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Code execution timed out after {timeout}s",
            "returncode": -1,
        }
    finally:
        os.unlink(tmp_path)
