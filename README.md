# prod-agentic-flow

Agentic-workflow production in tooling.

## Stack

- Model: **Qwen-3:4B** via **Ollama**
- Lang: Python

## Packages

See `requirements.txt` for full list. Key deps:

- fastapi, uvicorn — API server
- langchain, langgraph — agent orchestration
- ollama, langchain-ollama — LLM integration
- httpx, aiohttp — HTTP client
- pydantic — data validation
- SQLAlchemy — database
- python-dotenv — env config
