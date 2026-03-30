# quality_agent/main.py

import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from quality_agent import server
from quality_agent.agent import run_agent

app = FastAPI()

class TaskRequest(BaseModel):
    task: str
    max_turns: int = 10

class TaskResponse(BaseModel):
    result: str

class InvokeRequest(BaseModel):
    message: str

class InvokeResponse(BaseModel):
    response: str

@app.on_event("startup")
def startup():
    server.start()

@app.on_event("shutdown")
def shutdown():
    server.stop()

@app.post("/run", response_model=TaskResponse)
async def run(request: TaskRequest):
    try:
        result = await run_agent(request.task, request.max_turns)
        return TaskResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/invoke", response_model=InvokeResponse)
async def invoke(request: InvokeRequest):
    try:
        result = await run_agent(request.message)
        return InvokeResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
