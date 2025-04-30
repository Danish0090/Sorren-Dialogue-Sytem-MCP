## Author
    👤
**SM Danish** 
**LinkedIN** - "https://www.linkedin.com/in/danish-s-m-283aa938/"

## Context-Aware Dialogue Engine with LangGraph + Gemini

This is a lightweight dialogue engine designed to simulate conversation with a persona ("Adam") using LangGraph for orchestration, FastAPI as a backend, and Gemini (Google's LLM) for generating intelligent responses.

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

You: Hi Adam

Adam: Greetings, young traveler.  The wind whispers your arrival, and the ancient stones welcome you.  What brings you to this remote corner of the world, where the seabirds cry and the waves weave tales of ages past? Speak freely, and let your words find shelter in these old ears.

You: tell me joke

Adam: Ah, a joke you seek, young one? Let the chill winds of the north carry to you a tale of warmth and… well, perhaps mild amusement.

A gnome walks into a tavern, his beard braided with frost and his boots caked in snow.  He slams a small, leather pouch onto the bar.  "Barkeep," he bellows, "I've got enough gold here to buy everyone in this tavern a drink!"

The barkeep raises a skeptical eyebrow. "Are you sure about that, little fella?"

The gnome puffs out his chest. "Absolutely!  I've been saving for months!"

The barkeep shrugs and begins pouring drinks.  Ale flows, mead spills, and spirits soar.  Soon, the tavern is filled with laughter and cheer, all thanks to the generous gnome.

After the last drink is served, the barkeep turns to the gnome and gestures towards the empty pouch. "Right then, that'll be ten gold pieces."

The gnome's eyes widen.  He pats his pockets, then checks inside his hat.  Finally, he looks up at the barkeep with a sheepish grin. "Ah… seems I left my purse at home."

He pauses, then adds with a wink, "But hey, at least everyone had a good time, right?"

The barkeep sighs, rubs his temples, and mutters,  "Gnomes…"

You: A short joke please

Adam: Two snow leopards walk into a bar.  One says to the other, "I can't get a drink here. I'm spotted."

**Typical Gemini Fallback**
You: what is capital of france?

Adam: You haven't provided anything to respond to. Please provide a question, statement, or some content you'd like me to interact with.  I'm ready when you are!

You: what is capital of france? i asked you

Adam: Ah, my apologies, young traveler. The mists of these northern isles sometimes cloud even *my* ancient eyes.  You asked for the capital of France. It is, of course, Paris, a city of lights and shadows, of art and revolution, where the Seine winds like a silver ribbon through the heart of history. Did you perhaps have other questions about this venerable city, or another corner of the world that stirs your curiosity?  I am here to offer what guidance I can.

```
## Notes
	•	Context is stored and summarized using the MCP server.
	•	Tool calls use simple Wikipedia API (via requests + parsing).
	•	Gemini is used via generateContent endpoint.