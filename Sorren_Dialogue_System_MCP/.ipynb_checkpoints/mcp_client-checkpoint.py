'''
An MCP client that generates dialogue with Adam & LangGraph for orchestration and routing.

InputNode: Receives user message.
CheckContextNode: Calls MCP to get summarized context.
ToolDecisionNode: If user asks a factual question, route to TOOL_CALL node.
PromptAssemblyNode: Builds the full GPT prompt (persona + summary + recent turns).
LLMNode: Sends prompt to GPT and receives response.
OutputNode: Logs final output and updates server with new messages.
'''

import os
import yaml
import requests
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# --- Load API Key from config.yml ---
if os.path.exists("config.yml"):
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
    for k, v in config.get("env", {}).items():
        os.environ[k] = v

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
MCP_URL = "http://localhost:8000"

# --- Shared state type ---
class LangGraph_State(TypedDict):
    user_input: str
    context: str
    tool_result: str
    full_prompt: str
    response: str

# --- Nodes ---
def input_node(state: LangGraph_State) -> LangGraph_State:
    print("📥 input_node")
    return state

def check_context_node(state: LangGraph_State) -> LangGraph_State:
    print("📚 check_context_node")
    try:
        r = requests.get(f"{MCP_URL}/get_context")
        data = r.json()
        summary = data.get("summary", "")
        recent = data.get("recent", [])
        recent_text = "\n".join([f"{m['role']}: {m['content']}" for m in recent])
        state["context"] = f"{summary}\n{recent_text}"
    except Exception as e:
        print("⚠️ MCP context fetch failed:", e)
        state["context"] = ""
    return state

def is_factual_question(text: str) -> bool:
    keywords = ["what", "who", "where", "when", "how", "define", "list", "explain"]
    return any(k in text.lower() for k in keywords)

def tool_decision_node(state: LangGraph_State) -> str:
    print("🧠 tool_decision_node:", state["user_input"])
    return "tool_call" if is_factual_question(state["user_input"]) else "prompt_assembly"

def tool_call_node(state: LangGraph_State) -> LangGraph_State:
    print("🔧 tool_call_node")
    try:
        r = requests.post(f"{MCP_URL}/tool_call", json={"query": state["user_input"]})
        state["tool_result"] = r.json().get("result", "")
    except Exception as e:
        print("⚠️ Tool call failed:", e)
        state["tool_result"] = ""
    return state

def prompt_assembly_node(state: LangGraph_State) -> LangGraph_State:
    print("✏️ prompt_assembly_node")
    persona = "You are Sorren, a wise hermit and sufi who enlightens with kinship and wisdom."
    prompt = f"{persona}\n\nConversation so far:\n{state['context']}\n\nPlayer: {state['user_input']}\nAdam:"
    if state.get("tool_result"):
        prompt += f"\n\n(Use this fact: {state['tool_result']})"
    state["full_prompt"] = prompt
    return state

def llm_node(state: LangGraph_State) -> LangGraph_State:
    print("🤖 llm_node")
    payload = {
        "contents": [{"parts": [{"text": state["full_prompt"]}]}]
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GOOGLE_API_KEY
    }

    try:
        r = requests.post(GEMINI_ENDPOINT, json=payload, headers=headers)
        response_json = r.json()

        if "candidates" in response_json:
            result = response_json["candidates"][0]["content"]["parts"][0]["text"]
            state["response"] = result.strip()
        else:
            print("⚠️ Gemini error response:", response_json)
            state["response"] = response_json.get("error", {}).get("message", "Unknown error from Gemini.")
    except Exception as e:
        print(f"⚠️ Gemini call failed: {e}")
        state["response"] = "I'm sorry, something went wrong while generating my response."

    return state

def output_node(state: LangGraph_State) -> LangGraph_State:
    print("📤 output_node")
    print(f"\nAdam: {state['response']}")
    try:
        requests.post(f"{MCP_URL}/add_message", json={"role": "user", "content": state["user_input"]})
        requests.post(f"{MCP_URL}/add_message", json={"role": "Sorren", "content": state["response"]})
    except Exception as e:
        print("⚠️ Failed to save messages to MCP:", e)
    return state

# --- Build LangGraph ---
def build_graph():
    builder = StateGraph(LangGraph_State)

    builder.add_node("input", input_node)
    builder.add_node("check_context", check_context_node)
    builder.add_node("tool_call", tool_call_node)
    builder.add_node("prompt_assembly", prompt_assembly_node)
    builder.add_node("llm", llm_node)
    builder.add_node("output", output_node)

    builder.set_entry_point("input")
    builder.add_edge("input", "check_context")
    

    builder.add_conditional_edges(
    "check_context",
    tool_decision_node,
    {
        "tool_call": "tool_call",
        "prompt_assembly": "prompt_assembly"
    }
)

    builder.add_edge("tool_call", "llm")
    builder.add_edge("prompt_assembly", "llm")
    builder.add_edge("llm", "output")
    builder.add_edge("output", END)
    
    print("🔁 Expected Graph Flow:")
    print("input → check_context → tool_decision → tool_call → llm → output → END")
    print("                                          ↘ prompt_assembly →")

    print("🧩 Added nodes:", builder.nodes.keys())
    workflow = builder.compile()
    return workflow

# --- Main Execution ---
if __name__ == "__main__":
    print("🚀 Starting MCP Client...")
    graph = build_graph()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        initial_state = {
            "user_input": user_input,
            "context": "",
            "tool_result": "",
            "full_prompt": "",
            "response": ""
        }

        try:
            final_state = graph.invoke(initial_state)
        except Exception as e:
            print(f"❌ LangGraph execution failed: {e}")