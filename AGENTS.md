# AGENTS.md

## Big Picture (Read This First)
- `src/main.py` boots FastAPI and mounts only one business router: `src/adapters/inbound/api/chat_router.py` (`POST /chat`).
- `/chat` delegates to `ChatService` (`src/application/services/chat_service.py`), which invokes a compiled LangGraph with:
  - `config.configurable.thread_id` (conversation checkpoint key)
  - `runtime.context.user_id` and `runtime.context.should_generate_report`
- Graph assembly lives in `src/application/graph/graph.py` and is wired through DI in `src/dependencies.py`.

## Graph/Data Flow You Must Preserve
- Current flow: `START -> (load_memory + safeguard_check) -> resolve_initial_checks -> identify_intent -> path_* -> report -> summarize -> END`.
- Unsafe prompts branch to `blocked` then `summarize`; API maps blocked responses to HTTP 400 (`src/adapters/inbound/api/chat_router.py`).
- Path decisions use `Path` enum in `src/application/graph/state.py`; returning raw strings instead of enum values will break conditional routing.
- `summarize` trims memory to last 6 messages using `RemoveMessage(REMOVE_ALL_MESSAGES)` (`src/application/graph/nodes/summarize_node.py`).

## Architecture Conventions (Project-Specific)
- Hexagonal split is strict in practice:
  - `src/application/ports/*`: interfaces
  - `src/adapters/*`: concrete integrations (OpenRouter, Postgres, HTTP)
  - `src/application/graph/nodes/*`: orchestration nodes
- Node factories commonly return closures with injected dependencies (example: `path_a(path_history_repo)`, `identify_intent(model_client)`).
- Prompt logic is schema-first: prompt module defines both Pydantic schema + prompt builder (see `identify_intent_prompt.py`, `summarize_prompt.py`, `guardrails_prompt.py`).
- Import style: start from `src` directory

## Persistence + State Details
- Two PostgreSQL concerns are used:
  - LangGraph checkpoints/store via `PostgresMemory` (`src/adapters/outbound/persistence/postgres_memory.py`)
  - Path history table via `PathHistoryRepository` (`src/adapters/outbound/persistence/path_history_repository.py`)
- `infra/db/init-db.sh` creates `path_history_db`; compose also sets default `POSTGRES_DB=some_db` for memory DB.
- Preferred path memory is stored under namespace `("preferences", "paths")` (`src/adapters/outbound/persistence/postgres_repository.py`).
- `thread_id` is cookie-based and generated when absent (`resolve_thread_id` in `chat_service.py`).

## MCP + External Integrations
- Model client is OpenRouter-backed `ChatOpenAI` with provider routing metadata (`src/adapters/outbound/model_clients/open_api_client.py`).
- Report generation is optional (`generate_report=true` query param) and happens in graph node `generate_report`.
- Tools are composed at request time in `src/application/services/tools_service.py`:
  - filesystem MCP server via `npx @modelcontextprotocol/server-filesystem` scoped to `reports_dir`
  - custom `get_path_history` LangChain tool (`src/application/tools/get_path_history_tool.py`)

## Developer Workflow (What Actually Matters)
- Environment layering in tests: `tests/conftest.py` loads root `.env` then overrides with `tests/.env.test`.
- Most chat tests are integration-like (real graph + DB), so bring up Postgres first:
  - `docker compose up -d`
  - `pytest -q` (or `pytest -vs` for graph logs)
- Health smoke test is cheap: `GET /health`.
- LangGraph CLI config exists in `langgraph.json` with graph id `agent` and entrypoint `langgraph_dev/graph_entry.py` (uses `MockMemory`).

## Change Guidance for Agents
- When adding graph behavior, update both routing logic and tests under `tests/test_chat_*.py` that assert path/safeguard/summary behavior.
- If you introduce new runtime context keys, thread them through `ChatService.chat(...)` and consume from node `runtime.context`.
- Keep report-writing constrained to `reports_dir` semantics used by `fs_tool.py` and `report_prompt.py`.

