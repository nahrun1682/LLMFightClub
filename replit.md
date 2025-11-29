# LLM Fight Club

## Overview

LLM Fight Club is a multi-LLM group chat system where four different AI models (GPT, Claude, Gemini, and Grok) engage in real-time discussions about a given topic. An orchestrator agent (powered by GPT-4o-mini) acts as a facilitator, managing the conversation flow and ensuring productive debate among the participants.

The system enables users to ask a single question and watch as multiple AI models debate, agree, disagree, supplement, and challenge each other's perspectives—creating a dynamic "group chat" environment where diverse AI viewpoints converge to provide comprehensive answers.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework

**Microsoft Agent Framework (MAF)**: The application uses MAF's `MagenticBuilder` and `StandardMagenticManager` for orchestrating group chat workflows. The orchestrator creates plans, tracks progress, determines which agent speaks next, and synthesizes final answers from the multi-agent discussion.

**LiteLLMChatClient**: Custom wrapper class implementing MAF's `ChatClientProtocol`, bridging LiteLLM's multi-provider support with MAF's agent architecture. Located in `src/llm_fight_club/clients/litellm_client.py`.

**LiteLLM**: Provides a unified interface for communicating with multiple LLM providers (OpenAI, Anthropic, Google, xAI), abstracting away provider-specific API differences and enabling seamless multi-model interactions.

### Agent Architecture

**MAF ChatAgent Pattern**: All participant agents are created using MAF's `ChatAgent` class with:
- Custom `LiteLLMChatClient` for multi-provider support
- System prompts loaded from YAML configuration files
- Agent-specific descriptions for orchestrator planning

**Agent Factory** (`src/llm_fight_club/agents/maf_agents.py`):
- `create_gpt_agent()`: Balanced, neutral personality (GPT-4o)
- `create_claude_agent()`: Thoughtful, critical perspective (Claude 3.5 Haiku)
- `create_gemini_agent()`: Data-driven, evidence-based (Gemini 2.0 Flash)
- `create_grok_agent()`: Provocative, edgy (Grok 2)
- `create_orchestrator_client()`: LiteLLM client for GPT-4o-mini orchestrator
- `create_all_agents()`: Creates all participant agents

### Group Chat Workflow

**FightClubGroupChat** (`src/llm_fight_club/workflows/group_chat.py`):
- Uses `MagenticBuilder` to construct multi-agent workflow
- `StandardMagenticManager` orchestrates discussion with configurable max rounds
- Event callbacks for real-time message display
- Returns synthesized final answer from all perspectives

### Configuration Management

**Environment-Based Configuration**: API keys for all providers are loaded via `python-dotenv`. The `Config` dataclass validates that all required keys are present before the application runs.

**YAML-Based Prompts**: System prompts for each agent are stored in separate YAML files under the `prompts/` directory, allowing easy customization of agent personalities without code changes.

### Data Flow (MAF-based)

1. User submits a topic/question via CLI
2. `FightClubGroupChat` initializes with 4 participant agents
3. `MagenticBuilder` constructs workflow with `StandardMagenticManager`
4. Orchestrator (GPT-4o-mini) creates facts and plan
5. Orchestrator directs participants to speak based on plan
6. Each agent responds using its unique personality
7. Orchestrator tracks progress and determines next speaker
8. Discussion continues until max_round_count is reached
9. Orchestrator synthesizes final summary from all perspectives

## External Dependencies

### LLM Providers

- **OpenAI (GPT-4o, GPT-4o-mini)**: Primary orchestrator model and discussion participant
- **Anthropic (Claude 3.5 Haiku)**: Discussion participant
- **Google (Gemini 2.0 Flash)**: Discussion participant
- **xAI (Grok 2)**: Discussion participant

### Libraries & Frameworks

- **Microsoft Agent Framework (MAF) v1.0.0b**: Group chat orchestration via MagenticBuilder
- **LiteLLM**: Unified LLM API interface supporting all providers
- **python-dotenv**: Environment variable management
- **PyYAML**: Prompt configuration loading
- **pytest**: Testing framework with async support

### Search & Tool Integrations

> **Note**: Web search features are temporarily disabled due to LiteLLM compatibility issues. Basic chat functionality works without search.

### Development Tools

- **pytest-asyncio**: Async test support
- **uv**: Python package management

## Project Structure

```
src/llm_fight_club/
├── __init__.py
├── main.py                    # CLI entry point
├── config.py                  # Configuration management
├── prompts.py                 # YAML prompt loading
├── agents/
│   ├── __init__.py
│   ├── base.py                # Legacy BaseAgent class
│   ├── maf_agents.py          # MAF ChatAgent factories
│   └── [gpt|claude|gemini|grok|orchestrator].py
├── clients/
│   ├── __init__.py
│   └── litellm_client.py      # LiteLLMChatClient (ChatClientProtocol)
└── workflows/
    ├── __init__.py
    └── group_chat.py          # FightClubGroupChat (MagenticBuilder)

prompts/
├── gpt.yaml
├── claude.yaml
├── gemini.yaml
├── grok.yaml
└── orchestrator.yaml
```

## Recent Changes (November 2025)

- **Integrated Microsoft Agent Framework (MAF)** for group chat orchestration
  - Created `LiteLLMChatClient` implementing `ChatClientProtocol`
  - Built agent factory functions in `maf_agents.py`
  - Implemented `FightClubGroupChat` using `MagenticBuilder` and `StandardMagenticManager`
  - Updated `main.py` to use MAF-based workflow
- Migrated orchestrator from Azure OpenAI to regular OpenAI (GPT-4o-mini)
- Updated model names to LiteLLM-compatible versions:
  - Claude: `anthropic/claude-3-5-haiku-20241022`
  - Gemini: `gemini/gemini-2.0-flash`
  - Grok: `xai/grok-2-latest`
  - GPT: `openai/gpt-4o`
- Converted unit tests from mock-based to live API tests
- Temporarily disabled web search parameters (LiteLLM compatibility issue)

## Usage

```bash
# Run a discussion
uv run python -m llm_fight_club.main "Your topic here" --rounds 5
```
