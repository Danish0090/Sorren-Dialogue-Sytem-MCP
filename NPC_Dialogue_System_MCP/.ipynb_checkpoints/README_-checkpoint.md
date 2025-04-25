
# 🧠 Context-Aware Dialogue Engine with LangGraph + Gemini

This project is a lightweight, modular dialogue engine simulating a character ("Adam") who responds with wisdom and contextual awareness. It's built using **LangGraph** for flow orchestration, **FastAPI** for a backend context server, and **Gemini** (Google's LLM) to generate responses.

![Architecture](./Architecture_Dialogue_Engine.jpeg)

---

## 📁 Project Structure

```
.
├── mcp_client.py             # LangGraph-powered conversation agent
├── mcp_server.py             # FastAPI server to store and serve conversation context
├── config.yml                # YAML file storing Gemini API Key
├── Architecture_Dialogue_Engine.jpeg  # Architecture diagram
```

---

## 🧠 Key Features

- LangGraph-based flow logic
- Tool routing (factual vs conversational questions)
- MCP server for memory and summarization
- Wiki API integration for factual answers
- Gemini LLM integration for free-form responses

---

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install fastapi uvicorn langchain langgraph tiktoken requests pyyaml
```

### 2. Configure API Key

Create a file named `config.yml` in the root directory with this content:

```yaml
env:
  GOOGLE_API_KEY: "your-gemini-api-key-here"
```

---

## ▶️ How to Run

### Start the MCP Server (Backend)

```bash
uvicorn mcp_server:app --reload
```

### Launch the LangGraph Client

```bash
python mcp_client.py
```

Start chatting with Adam through the CLI interface.

---

## 🖼️ Architecture Overview

The LangGraph workflow includes:

- `check_context_node`: Gets recent history from the MCP server
- `tool_decision_node`: Determines if the query is factual
- `tool_call_node`: Calls MCP `/tool_call` (Wiki API) if factual
- `prompt_assembly_node`: Builds the GPT prompt
- `llm_node`: Sends the prompt to Gemini
- `output_node`: Logs and returns the reply

---

## 💬 5-Turn Transcript Example (with Tool Call)

```
You: Hi Adam
Adam: Greetings, traveler. What brings you to me today?

You: What is the capital of Norway?
[TOOL_CALL triggered: Wiki API called]
Adam: According to what I've found, the capital of Norway is Oslo.

You: Nice, thanks!
Adam: You're most welcome. Curiosity is the beginning of wisdom.

You: I feel stuck in my career.
Adam: When one path feels blocked, another often lies hidden in the mist. Tell me more.

You: How can I improve in Counter Strike?
Adam: Ah, a test of reflexes and strategy. Focus on map awareness, communication, and mastering recoil control.
```

---

## 🔌 API Endpoints (MCP Server)

- `POST /add_message`: Adds a message to memory `{ "role": "user" | "adam", "content": "..." }`
- `GET /get_context`: Returns a summary + recent turns
- `POST /tool_call`: Uses a basic Wiki API to fetch factual answers

---

## 🛠️ Helper Scripts

- `mcp_server.py`: FastAPI app that handles storing messages, summarizing history, and calling tools
- `mcp_client.py`: LangGraph script that controls conversation logic and interacts with Gemini

---

## 📸 Diagram

See `Architecture_Dialogue_Engine.jpeg` for the full architecture flow.

---

## 🙏 Credits

Built for an assessment to demonstrate RAG-like orchestration with LangGraph + Gemini.
