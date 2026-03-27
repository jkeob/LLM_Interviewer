import requests
import json

prompt = """You are a helpful and precise assistant for checking the quality of the answer.

[Question]
Summarize the main point of the article.

[Reference Answer]
A strong answer should clearly state the article's main argument in a concise way.

[The Start of Assistant 1's Answer]
The article argues that renewable energy adoption is necessary for long-term environmental and economic stability.
[The End of Assistant 1's Answer]

[System]
Please rate the answer on helpfulness, relevance, accuracy, and level of detail.
"""

payload = {
    "model": "BAAI/JudgeLM-33B-v1.0",
    "prompt": prompt,
    "temperature": 0.0,
    "max_tokens": 300
}

r = requests.post(
    "http://127.0.0.1:8001/v1/completions",
    headers={"Content-Type": "application/json"},
    json=payload,
    timeout=300,
)

print(r.status_code)
print(json.dumps(r.json(), indent=2))
