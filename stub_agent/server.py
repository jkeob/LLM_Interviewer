import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

APP_NAME = "stub-general-agent"
APP_VERSION = "0.1.0"

VLLM_URL = os.getenv("VLLM_URL", "http://localhost:8000/v1/chat/completions")
MODEL = os.getenv("MODEL", "Qwen/Qwen3-30B-A3B-Instruct-2507")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8090"))

SYSTEM_PROMPT = """You are a general purpose AI assistant capable of handling a wide range of tasks.
You can help with code generation, debugging, email writing, planning, reasoning, summarization, and more.
Always produce concrete, complete outputs. Do not describe what you would do, just do it.
"""


class InvokeRequest(BaseModel):
    message: str


class InvokeResponse(BaseModel):
    response: str


app = FastAPI(title=APP_NAME, version=APP_VERSION)


@app.get("/health")
def health():
    return {"ok": True, "name": APP_NAME, "version": APP_VERSION}


@app.post("/invoke", response_model=InvokeResponse)
def invoke(req: InvokeRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    payload = {
        "model": MODEL,
        "max_tokens": 4096,
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message},
        ],
    }

    try:
        r = requests.post(
            VLLM_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=120,
        )
        r.raise_for_status()
        body = r.json()
        text = body["choices"][0]["message"]["content"].strip()
        return InvokeResponse(response=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
