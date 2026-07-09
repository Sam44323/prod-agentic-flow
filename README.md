# prod-agentic-flow

Agentic workflow production tooling. Qwen-3:4B agent orchestrated via LangGraph, served via FastAPI.

## Stack

- Model: **Qwen-3:4B** via **Ollama**
- Lang: Python

## Architecture

```
app/
├── api/                # FastAPI routes & request/response models
│   ├── models.py
│   └── routes.py
├── graph/
│   ├── node/           # One file per node handler
│   │   ├── approval.py
│   │   ├── calculator.py
│   │   ├── calculator_request.py
│   │   ├── guardrail.py
│   │   ├── guardrail_response.py
│   │   ├── llm.py
│   │   ├── output_error.py
│   │   ├── output_guardrail.py
│   │   ├── planner.py
│   │   ├── post_approval_route.py
│   │   ├── query_rewritter.py
│   │   ├── retriever.py
│   │   ├── tool_authorization.py
│   │   └── weather.py
│   ├── graph.py        # LangGraph flow definition & edges
│   ├── nodes.py        # Re-exports from node/ (backwards compat)
│   ├── router.py       # Conditional-routing functions
│   └── state.py        # AgentState TypedDict
├── guardrails/
│   └── policy_engine.py  # Input/output/tool-authorization policies
├── llm/
│   └── qwen.py         # Qwen-3:4B via Ollama wrapper
├── memory/
│   ├── fact_extractor.py
│   ├── semantic_memory.py
│   ├── session_memory.py
│   └── sqlite_memory.py
├── tools/
│   ├── calculator.py
│   ├── database.py
│   ├── executor.py
│   ├── registry.py
│   └── weather.py
├── config.py
└── main.py

tests/
├── test_calculator.py
├── test_graph.py
├── test_guardrails.py
├── test_node.py
└── test_router.py
pyproject.toml
pyrightconfig.json
requirements.txt
```

## Build

```bash
python -m build
```

Generates a distributable `.tar.gz` and `.whl` in `dist/`. Requires `build` package (`pip install build`).

## Run

```bash
pip install -e .     # install the project in editable mode
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
- pytest - testing
- SQLAlchemy — database
- python-dotenv — env config
