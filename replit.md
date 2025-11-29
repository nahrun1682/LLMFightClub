# LLM Fight Club

## Overview

LLM Fight Club is a multi-LLM group chat system where four different AI models (GPT, Claude, Gemini, and Grok) engage in real-time discussions about a given topic. An orchestrator agent (powered by GPT-4o-mini) acts as a facilitator, managing the conversation flow and ensuring productive debate among the participants.

The system enables users to ask a single question and watch as multiple AI models debate, agree, disagree, supplement, and challenge each other's perspectives—creating a dynamic "group chat" environment where diverse AI viewpoints converge to provide comprehensive answers.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework

**Microsoft Agent Framework (MAF)**: The application is designed to use MAF's `MagenticBuilder` and `StandardMagenticManager` for orchestrating group chat workflows. The orchestrator creates plans, tracks progress, determines which agent speaks next, and synthesizes final answers from the multi-agent discussion.

**LiteLLM**: Provides a unified interface for communicating with multiple LLM providers (OpenAI, Anthropic, Google, xAI), abstracting away provider-specific API differences and enabling seamless multi-model interactions.

### Agent Architecture

**Base Agent Pattern**: All agents inherit from `BaseAgent`, which provides:
- System prompt loading from YAML configuration files
- Asynchronous message handling via LiteLLM's `acompletion`
- Standardized response format through `AgentResponse` dataclass
- Provider-specific parameter injection via `get_extra_params()`

**Specialized Agents**:
- **GeminiAgent**: Data-driven personality with Google Search grounding enabled
- **GrokAgent**: Provocative personality with X/Twitter, web, and news search capabilities
- **ClaudeAgent**: Critical, thoughtful personality with web search tools
- **GPTAgent**: Balanced, neutral personality with web search preview
- **OrchestratorAgent**: Facilitator using GPT-4o-mini to manage discussion flow

Each agent has a distinct personality and search capability, creating diverse perspectives in group discussions.

### Configuration Management

**Environment-Based Configuration**: API keys for all providers are loaded via `python-dotenv` from a `.env` file. The `Config` dataclass validates that all required keys are present before the application runs.

**YAML-Based Prompts**: System prompts for each agent are stored in separate YAML files under the `prompts/` directory, allowing easy customization of agent personalities without code changes.

### Data Flow

1. User submits a topic/question
2. Orchestrator initializes the discussion and creates a conversation plan
3. Participants (Gemini, Grok, Claude, GPT) take turns responding based on orchestrator's direction
4. Each agent leverages its unique search capabilities to ground responses
5. Orchestrator tracks conversation state and determines next speaker
6. Discussion continues until orchestrator determines sufficient coverage
7. Orchestrator synthesizes final summary from all perspectives

### Message Structure

**Message Format**: Conversations use a standardized `Message` dataclass with `role`, `content`, and optional `name` fields, compatible with OpenAI's chat format and extensible to other providers.

**Response Format**: Agent responses are wrapped in `AgentResponse` dataclass containing the content, agent identifier, and raw API response for debugging.

## External Dependencies

### LLM Providers

- **OpenAI (GPT-4o, GPT-4o-mini)**: Primary orchestrator model and discussion participant
- **Anthropic (Claude 3.5 Haiku)**: Discussion participant
- **Google (Gemini 2.0 Flash)**: Discussion participant
- **xAI (Grok 2)**: Discussion participant

### Libraries & Frameworks

- **Microsoft Agent Framework (MAF)**: Group chat orchestration (planned integration)
- **LiteLLM**: Unified LLM API interface supporting all providers
- **python-dotenv**: Environment variable management
- **PyYAML**: Prompt configuration loading
- **pytest**: Testing framework with async support

### Search & Tool Integrations

> **Note**: Web search features are temporarily disabled due to LiteLLM compatibility issues. Basic chat functionality works without search.

### Development Tools

- **pytest-asyncio**: Async test support
- **Black/Ruff**: Code formatting and linting (implicit from Python project structure)

## Recent Changes (November 2025)

- Migrated orchestrator from Azure OpenAI to regular OpenAI (GPT-4o-mini)
- Updated model names to LiteLLM-compatible versions:
  - Claude: `anthropic/claude-3-5-haiku-20241022`
  - Gemini: `gemini/gemini-2.0-flash`
  - Grok: `xai/grok-2-latest`
  - GPT: `openai/gpt-4o`
- Converted unit tests from mock-based to live API tests
- Temporarily disabled web search parameters (LiteLLM compatibility issue)