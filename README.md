# prod-agentic-flow

Agentic workflow production tooling. Qwen-3:4B agent orchestrated via LangGraph, served via FastAPI.

## Stack

- Model: **Qwen-3:4B** via **Ollama**
- Lang: Python

## Architecture

```
app/
├── api/            # FastAPI-routes
├── graph/          # LangGraph (state, nodes, edges)
├── llm/            # Qwen/Ollama wrapper
├── tools/          # REST, SQL, GitHub, Python, etc.
├── rag/            # Loaders, chunking, embeddings, retrieval
├── memory/         # The Short & long-term memory
├── guardrails/     # Input/output validation
├── checkpoints/    # Durable execution
├── prompts/        # System & task prompts
├── models/         # Pydantic schemas
├── services/       # Biz-logic
├── utils/          # Shared utilities
├── config.py
└── main.py

knowledge-base/    # Docs for RAG
data/              # SQLite/ChromaDB storage
tests/             # Unit & integration tests
docker/            # Container config
.env               # Environment vars
requirements.txt   # Python deps
pyrightconfig.json # Pyright-config
```

## Run

```bash
uvicorn app.main:app --reload
```

The api server starts at `http://localhost:8000`. Open Swagger UI at `http://localhost:8000/docs` to test `/chat` endpoint from browser.

## Packages

See `requirements.txt` for full list. Key deps:

- fastapi, uvicorn — API server
- langchain, langgraph — agent orchestration
- ollama, langchain-ollama — LLM integration
- httpx, aiohttp — HTTP client
- pydantic — data validation
- SQLAlchemy — database
- python-dotenv — env config
