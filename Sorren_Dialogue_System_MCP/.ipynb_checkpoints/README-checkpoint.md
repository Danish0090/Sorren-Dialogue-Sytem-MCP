## Author
    👤
**SM Danish** 
**LinkedIN** - "https://www.linkedin.com/in/danish-s-m-283aa938/"

## Context-Aware Dialogue Engine with LangGraph + Gemini

This is a lightweight dialogue engine designed to simulate conversation with a persona ("Sorren") using LangGraph for orchestration, FastAPI as a backend, and Gemini (Google's LLM) for generating intelligent responses.

## Project Structure
├── mcp_client.py                      # LangGraph client to drive the conversation
├── mcp_server.py                      # FastAPI server exposing context and tools
├── config.yml                         # Contains your Gemini API key
├── Architecture_Dialogue_Engine.jpeg  # System diagram

## How It Works

1. Player Input (from CLI) is passed into a LangGraph workflow.
2. MCP Server provides relevant context via `/GET_CONTEXT`.
3. Tool Decision Node** routes:
   - PromptAssembly → Gemini (for conversational questions)
   - ToolCall → MCP `/TOOL_CALL` → Wiki API (for factual questions)
4. Final response is printed and logged via the OutputNode.

## Setup

1. **Install dependencies** (use a virtual environment):

```bash
pip install -r requirements.txt
```
2. **Update config_.yml** to store your Gemini API Key:

## Running the System

1. **Start the Server (MCP)**

```bash
uvicorn mcp_server:app --reload
```
2. **Optional** Run of MCP Server

```bash
python mcp_server.py
```
To test Swagger UI **http://localhost:8000/docs** for endpoints

3. **Run the Client (LangGraph workflow)**

```bash
python mcp_client.py
```

## 5-Turn Transcript Example (with Tool Call)
```

You: Hi Sorren

Sorren: Hi, little sparrow. Come, sit by the fire.  The wind whispers stories tonight, and the flames dance to their rhythm.  What brings you to my humble abode, tucked away in the embrace of the mountain?  There's tea brewing, if you've the time for a cup and a quiet moment.  Speak your heart, little sparrow, and let its burdens take flight.

You: Tell me a deep poem of rumi

Sorren: Ah, Rumi. A heart overflowing with the divine, wasn't he?  His words are like stars, guiding us through the darkest nights.  Let me share one that resonates deeply within me, little sparrow. Close your eyes for a moment and let the words settle upon your soul:

*Out beyond ideas of wrongdoing and rightdoing,*
*there is a field. I'll meet you there.*

*When the soul lies down in that grass,*
*the world is too full to talk about.*
*Ideas, language, even the phrase *each other**
*doesn't make any sense.*

Open your eyes now, little sparrow.  What do you feel stirring within you?  Those simple words hold oceans of meaning. They speak of a place beyond the duality of our world, a place of pure connection, of unity.  Rumi reminds us that true meeting, true understanding, transcends the limitations of our minds and our judgments.  It is in the silence, in the stillness, that we truly find each other, and in finding each other, we find ourselves… and the Divine.  Sip your tea, little sparrow, and let these words take root within you.

You: A very short thought of Rumi?

Sorren: "You are the soul of the soul of the universe, and your name is Love."  There, little sparrow.  A tiny seed of Rumi's wisdom.  Hold it close, and let it blossom within you.  Sometimes the smallest words hold the greatest truths.  Like a single drop of rain reflecting the entire sky.

#################TOOL_CALL for Factual Questions################

**Typical Gemini Fallback**
You: What is the capital of Egypt?

Sorren: You haven't provided anything to respond to.  Please give me a question, some text, a code snippet, or something else to work with!

You: I have provided check please

Sorren: Ah, little sparrow, you seek direction, a path forward.  But tell me, what journey are you on?  The capital of Egypt, yes, it is Cairo. A bustling city, a hub of humanity, a place where history whispers from ancient stones. But is that the knowledge you truly seek?  Is Cairo a destination, or a stepping stone on a larger quest? Sip your tea, little sparrow, and tell me, where does your heart long to go? Perhaps there is a deeper question hidden within your request, a yearning for something beyond mere facts and figures.  Let us explore that together, shall we?

```
## Notes
	•	Context is stored and summarized using the MCP server.
	•	Tool calls use simple Wikipedia API (via requests + parsing).
	•	Gemini is used via generateContent endpoint.