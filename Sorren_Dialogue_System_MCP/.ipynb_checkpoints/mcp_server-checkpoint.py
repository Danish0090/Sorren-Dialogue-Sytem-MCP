'''
A custom MCP server exposing context-aware operations.

ADD_MESSAGE {role, content} – Append message.
GET_CONTEXT – Return summarized + recent messages within token limit.
SUMMARIZE_HISTORY – Condense old dialogue.
RESET – Clear conversation.
TOOL_CALL <query> – Search Wikipedia or any public data source and return top result (can use requests + parsing).
'''

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
import requests
import tiktoken
import yaml
import os

# Load from config.yml
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Set as environment variables
for key, value in config.get("env", {}).items():
    os.environ[key] = value

# Now you can use it like:
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = FastAPI()

# Define memory and token limit
CONVERSATION_HISTORY: List[dict] = []
MAX_TOKEN = 4000
ENC = tiktoken.get_encoding("cl100k_base") #Works with Gemini, but will be approx.
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"

# Pydantic data model for validation of annotations
class Message(BaseModel):
  role: str
  content: str

class ToolQuery(BaseModel):
  query: str

# ------ Utilities -------

def estimate_tokens(text: str) -> int:
  return len(ENC.encode(text))

# Not a good way to do , I will replace it with Gemini Summarizer later

#def summarize_history(history: List[dict], MAX_TOKEN=1000) -> str:
#  combined = " ".join([msg["content"] for msg in history])
#  if combined>200:
#    trunc_combined = combined[:200] + "..."
#  else:
#    trunc_combined = combined

#  return trunc_combined


# Copying Gemini Summarizer
def summarize_history(history: List[dict], MAX_TOKEN=500) -> str:
    if not history:
        return ""

    chat_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

    payload = {
        "contents": [
            {
                "parts": [{"text": f"Summarize this conversation briefly:\n\n{chat_text}"}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GOOGLE_API_KEY
    }

    try:
        response = requests.post(GEMINI_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        summary = response.json()['candidates'][0]['content']['parts'][0]['text']
        return summary.strip()
    except Exception as e:
        print(f"[Gemini summarization error] {e}")
        return "Summary unavailable."

def get_context():
    try:
        summary = summarize_history(CONVERSATION_HISTORY[:-5]) if CONVERSATION_HISTORY else ""
        recent = CONVERSATION_HISTORY[-5:]
        return {
            "summary": summary,
            "recent": recent,
            "total_tokens": estimate_tokens(summary + ''.join([m["content"] for m in recent]))
        }
    except Exception as e:
        return {
            "summary": "",
            "recent": [],
            "total_tokens": 0,
            "error": str(e)
        }
 
# Making a wikipedia call for factual information
def wiki_search(query: str) -> str:
    wiki_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'utf8': 1
    }
    response = requests.get(wiki_url, params=params)
    results = response.json().get("query", {}).get("search", [])
    return results[0]["snippet"] if results else "I am sorry, I don't have the information you need."

# ------ Endpoints -------
@app.get("/")
def read_root():
    return {"message": "API is running. Available endpoints: /add_message, /get_context, /summarize_history, /tool_call, /reset"}

@app.post("/add_message")
def add_message(message: Message):
    CONVERSATION_HISTORY.append(message.dict())
    return {"status": "Message added."}

@app.get("/get_context")
def get_context_endpoint():
    return get_context()

@app.post("/summarize_history")
def summarize_endpoint():
    summary = summarize_history(CONVERSATION_HISTORY)
    return {"summary": summary}

@app.post("/tool_call")
def tool_call(query: ToolQuery):
    result = wiki_search(query.query)
    return {"result": result}

@app.post("/reset")
def reset():
    CONVERSATION_HISTORY.clear()
    return {"status": "History cleared."}
