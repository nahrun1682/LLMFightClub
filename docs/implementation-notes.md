# LLM Fight Club - Implementation Notes

## Overview

Multi-LLM group chat system where GPT, Claude, Gemini, Grok discuss topics with an orchestrator (Azure OpenAI) as facilitator.

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Orchestration | Microsoft Agent Framework (MAF) | Group chat workflow |
| LLM Interface | LiteLLM | Unified API for all providers |
| Search | Provider-native | Each model's built-in search |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MagenticBuilder                       │
├─────────────────────────────────────────────────────────┤
│  StandardMagenticManager (Azure OpenAI - Orchestrator)  │
│    - Creates plans                                       │
│    - Tracks progress                                     │
│    - Decides which agent speaks next                     │
│    - Synthesizes final answer                            │
├─────────────────────────────────────────────────────────┤
│  Participants:                                           │
│    ├── ChatAgent(Gemini) ─── LiteLLMChatClient          │
│    ├── ChatAgent(Grok) ──── LiteLLMChatClient           │
│    ├── ChatAgent(Claude) ── LiteLLMChatClient           │
│    └── ChatAgent(GPT) ───── LiteLLMChatClient           │
└─────────────────────────────────────────────────────────┘
```

## Completed Work

### 1. Project Structure

```
LLMFightClub/
├── src/llm_fight_club/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py          # Environment variable loading
│   ├── prompts.py         # YAML prompt loader
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py        # BaseAgent with LiteLLM
│   │   ├── gemini.py      # Google Search enabled
│   │   ├── grok.py        # X/web/news search enabled
│   │   ├── claude.py      # Web search enabled
│   │   ├── gpt.py         # Web search enabled
│   │   └── orchestrator.py
│   └── workflows/
│       ├── __init__.py
│       └── group_chat.py  # TODO: MAF implementation
├── prompts/
│   ├── gemini.yaml
│   ├── grok.yaml
│   ├── claude.yaml
│   ├── gpt.yaml
│   └── orchestrator.yaml
├── tests/
│   ├── conftest.py        # pytest fixtures with mocks
│   └── unit/
│       └── test_agents/
│           ├── test_base.py
│           ├── test_gemini.py
│           ├── test_grok.py
│           ├── test_claude.py
│           ├── test_gpt.py
│           └── test_orchestrator.py
└── docs/
    └── implementation-notes.md
```

### 2. Agent Implementation (LiteLLM)

Each agent extends `BaseAgent` and uses LiteLLM for unified API calls.

**BaseAgent Features:**
- Async `respond()` method using `litellm.acompletion()`
- YAML-based system prompts via `prompts.py`
- Message history support
- Provider-specific extra parameters

**Search Parameters by Provider:**

| Agent | Model | Search Config |
|-------|-------|---------------|
| Gemini | `gemini/gemini-1.5-pro` | `{"tools": [{"googleSearch": {}}]}` |
| Grok | `xai/grok-beta` | `{"search_parameters": {"mode": "on", "sources": ["x", "web", "news"]}}` |
| Claude | `anthropic/claude-sonnet-4-20250514` | `{"tools": [{"type": "web_search_20250305"}]}` |
| GPT | `openai/gpt-4o` | `{"tools": [{"type": "web_search_preview"}]}` |
| Orchestrator | `azure/gpt-4o` | None (coordination only) |

### 3. Environment Variables

Required in `.env`:

```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
GOOGLE_API_KEY=
XAI_API_KEY=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
```

### 4. Unit Tests

29 tests passing with mocked LiteLLM responses.

```bash
uv run python -m pytest tests/ -v
```

Tests cover:
- Message/AgentResponse dataclasses
- Agent initialization
- System prompt loading from YAML
- Extra parameters (search configs)
- API key handling
- Message building with history
- Async respond method

## Pending Work

### Phase 1: Connection Testing
- Create `scripts/test_connections.py`
- Verify each agent connects with real API keys
- Test search functionality

### Phase 2: LiteLLMChatClient
- Implement MAF `ChatClientProtocol` wrapper for LiteLLM
- Handle message format conversion (MAF <-> LiteLLM)

### Phase 3: MagenticBuilder Integration
- Wire up `StandardMagenticManager` with Azure OpenAI
- Add all 4 agents as participants
- Implement `group_chat.py` workflow

### Phase 4: Integration Testing
- Run actual multi-LLM discussions
- Verify orchestration logic

## MAF Research Notes

### Available Patterns

| Pattern | Description |
|---------|-------------|
| `MagenticBuilder` | Manager-worker orchestration |
| `SequentialBuilder` | Fixed order execution |
| `ConcurrentBuilder` | Parallel execution |

### Key MAF Components

- `ChatAgent` - Wraps ChatClient with instructions
- `ChatClientProtocol` - Interface for LLM providers
- `StandardMagenticManager` - Orchestrator logic
- `MagenticBuilder` - Workflow builder

### Why MagenticBuilder?

GroupChatBuilder is not yet available in the installed package. MagenticBuilder implements Magentic-One pattern which provides:
- Automatic planning
- Progress tracking
- Dynamic agent selection
- Final answer synthesis

This is essentially a sophisticated group chat with an intelligent orchestrator.

## Design Decisions

1. **LiteLLM over LangChain**: Simpler, focused on LLM calls only, works well with MAF
2. **YAML prompts**: Separation of concerns, easy to modify personalities
3. **Provider-native search**: Each model uses its own search capability for best results
4. **src layout**: Python best practice for package structure
5. **MAF MagenticBuilder**: Official framework, no custom group chat implementation
