"""
server.py
---------
Spins up a vllm server for Qwen3-30B and waits until it is ready.
Call start() before running the interview, stop() when done.
"""

import subprocess
import time
import os
import signal
import requests

MODEL = "Qwen/Qwen3-30B-A3B-Instruct-2507"
PORT = 8000
HOST = "http://localhost"
HEALTH_URL = f"{HOST}:{PORT}/v1/models"
STARTUP_TIMEOUT = 300  # seconds to wait for server to be ready


_proc: subprocess.Popen = None


def start():
    global _proc

    print(f"[server] starting vllm for {MODEL} on port {PORT}...")

    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "2,3"

    _proc = subprocess.Popen(
        [
            "vllm", "serve", MODEL,
            "--tensor-parallel-size", "2",
            "--max-model-len", "8192",
            "--port", str(PORT),
            "--dtype", "bfloat16",
            "--gpu-memory-utilization", "0.8",
        ],
        env=env,
        stdout=None,
        stderr=None,
    )

    _wait_until_ready()
    print(f"[server] vllm is ready on port {PORT}")


def stop():
    global _proc
    if _proc is not None:
        print("[server] shutting down vllm...")
        _proc.send_signal(signal.SIGTERM)
        try:
            _proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            _proc.kill()
        _proc = None
        print("[server] vllm stopped")


def _wait_until_ready():
    deadline = time.time() + STARTUP_TIMEOUT
    while time.time() < deadline:
        try:
            r = requests.get(HEALTH_URL, timeout=3)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(3)
    raise TimeoutError(f"[server] vllm did not become ready within {STARTUP_TIMEOUT}s")
