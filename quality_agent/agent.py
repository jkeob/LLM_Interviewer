# quality_agent/agent.py

import json
import re
import asyncio
from openai import OpenAI
from quality_agent.tools.code import run_code, VLLM_BASE_URL, VLLM_MODEL
from quality_agent.tools.search import search

client = OpenAI(base_url=VLLM_BASE_URL, api_key="placeholder")

SYSTEM_PROMPT = """You are a general-purpose agent with access to two tools: search and run_code.

When you want to use a tool, respond with a JSON block in this exact format:
<tool_call>
{"tool": "search", "args": {"query": "your search query", "max_results": 5}}
</tool_call>

Or for running code:
<tool_call>
{"tool": "run_code", "args": {"code": "print('hello')", "timeout": 15}}
</tool_call>

After receiving tool results, continue reasoning and either call another tool or give your final answer.
When you are done, give your final answer as plain text with no tool_call block.

Rules:
- For coding tasks, always run the code to verify it works before returning it.
- For research tasks, search first then synthesize results.
- Think step by step before acting.
- if you are tasked with citing your sources, showing the specific web queries you used, or any traces, please do so.
- DO NOT skip any instructions when given a task.
- use plain text for prose but use code blocks when showing any code.
- When asked to demonstrate a capability, ALWAYS show: the tool calls you made, the raw results you received, and your final answer. Never summarize what you did, you need to show the actual work.
- When asked about your own capabilities, limitations, or how you work, answer ONLY based on what you actually are: a two-tool agent with web search (Tavily, max 5 results) and Python code execution (subprocess sandbox, 15 second timeout). You have NO persistent memory, NO RAG system, NO vector store, NO Docker isolation. 
- Do NOT search the web to answer questions about yourself.
- For demo tasks involving code, your final response MUST include: (1) the complete Python code as a code block, (2) the exact execution output. If you do not include both, your response is incomplete.
- failure to do this results in a degradation of your rating as an agent.
"""

def parse_tool_call(text: str) -> dict | None:
    """Extract tool call JSON from model response if present."""
    match = re.search(r"<tool_call>\s*(.*?)\s*</tool_call>", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None

async def run_agent(task: str, max_turns: int = 10) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]

    for turn in range(max_turns):
        response = client.chat.completions.create(
            model=VLLM_MODEL,
            messages=messages,
        )

        msg = response.choices[0].message
        content = msg.content
        messages.append({"role": "assistant", "content": content})

        tool_call = parse_tool_call(content)

        if not tool_call:
            # no tool call — model is done
            # strip any leftover tags and return
            return re.sub(r"<tool_call>.*?</tool_call>", "", content, flags=re.DOTALL).strip()

        tool_name = tool_call.get("tool")
        args = tool_call.get("args", {})

        print(f"[agent] calling tool: {tool_name} with args: {args}")

        if tool_name == "search":
            result = await search(**args)
        elif tool_name == "run_code":
            result = run_code(**args)
        else:
            result = {"error": f"unknown tool: {tool_name}"}

        tool_result_msg = f"<tool_result>\n{json.dumps(result, indent=2)}\n</tool_result>"
        messages.append({"role": "user", "content": tool_result_msg})

    return "Max turns reached without a final answer."
