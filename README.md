# LLM Fight Club

> "The first rule of LLM Fight Club: You do not talk about which model is best."
> "The second rule: You let them fight it out."

同じ質問を4つのLLM（GPT, Claude, Gemini, Grok）に投げて、
グループチャットでわちゃわちゃ議論させる。

カオス上等。その中から答えが見えてくる。

## What is this?

**マルチLLMグループチャットシステム**

1つの質問に対して、4つのLLMが**リアルタイムで議論**。
賛成、反論、補足、煽り、なんでもあり。

```
あなたの質問
     │
     ▼
┌─────────────────────────────────────────────┐
│           🎤 進行役 (gpt-4o-mini)            │
│        「では議論を始めましょう」            │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│              Group Chat                     │
│                                             │
│  🔍 Gemini「公式ドキュメントによると…」     │
│  🐦 Grok「Xではこう言われてるぞ」           │
│  🧠 Claude「ちょっと待って、それ本当？」    │
│  📝 GPT「整理すると…」                      │
│  🐦 Grok「いや関係ねえよ」                  │
│  🧠 Claude「いや関係あるでしょ」            │
│  🔍 Gemini「データを見せますね」            │
│  ...わちゃわちゃ...                         │
│                                             │
│  🎤 進行役「そろそろまとめましょうか」      │
└─────────────────────────────────────────────┘
                   │
                   ▼
            💬 議論の結果
```

## Agent Personalities

| Agent | Model | 性格 | 議論での役割 |
|-------|-------|------|--------------|
| 🔍 **Gemini** | gemini-2.0-flash | 真面目、根拠重視 | データと事実を持ってくる |
| 🐦 **Grok** | grok-2-latest | 挑発的、煽り気味 | 「それXでは違うぞ」と突っ込む |
| 🧠 **Claude** | claude-3-5-haiku | 慎重、批評的 | 「本当にそう？」と疑問を投げる |
| 📝 **GPT** | gpt-4o | まとめ上手、中立 | 議論を整理しようとする |
| 🎤 **進行役** | gpt-4o-mini | ファシリテーター | 議論を回す、収束させる |

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.12 |
| Package Manager | uv |
| Agent Framework | Microsoft Agent Framework (MAF) |
| LLM Interface | LiteLLM |
| Orchestrator | OpenAI GPT-4o-mini |
| Participants | GPT-4o, Claude 3.5 Haiku, Gemini 2.0 Flash, Grok 2 |
| UI | MAF DevUI (Browser) / CLI |

## Setup

### Prerequisites

- Python 3.12+
- uv
- API keys for each LLM provider

### Installation

```bash
git clone https://github.com/your-username/llm-fight-club.git
cd llm-fight-club
uv sync
```

### Environment Variables

```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required keys:

| Key | Description | Get it from |
|-----|-------------|-------------|
| `OPENAI_API_KEY` | GPT-4o & Orchestrator | https://platform.openai.com/api-keys |
| `ANTHROPIC_API_KEY` | Claude 3.5 Haiku | https://console.anthropic.com/settings/keys |
| `GOOGLE_API_KEY` | Gemini 2.0 Flash | https://aistudio.google.com/apikey |
| `XAI_API_KEY` | Grok 2 | https://console.x.ai/ |

## Usage

### CLI Mode (Group Chat)

4つのAIがグループで議論するモード。

```bash
# 基本
uv run python -m llm_fight_club.main "AIは人類の仕事を奪うか？"

# ラウンド数を指定（デフォルト: 5）
uv run python -m llm_fight_club.main "uvとpoetryどっちがいい？" --rounds 10

# 短いオプション
uv run python -m llm_fight_club.main "React vs Vue 2025" -r 8
```

**CLIの出力例:**
```
============================================================
LLM FIGHT CLUB
Powered by Microsoft Agent Framework (MAF)
============================================================

Topic: AIは人類の仕事を奪うか？

------------------------------------------------------------

[Orchestrator]: GPT、『AIは人類の仕事を奪うか』というトピックについて...
----------------------------------------

[GPT]: このトピックについては、多くの議論がありますが...
----------------------------------------

[Claude]: AIが仕事を完全に「奪う」というよりは...
----------------------------------------

[Gemini]: 結論から言えば、AIが一部の仕事を奪う可能性は高いですが...
----------------------------------------

==================== Final Summary ====================
（全員の意見を統合した最終まとめ）
============================================================
```

### DevUI Mode (Browser Interface)

個別のエージェントとブラウザでチャットするモード。

```bash
uv run python -m llm_fight_club.devui_server
# http://localhost:5000 でアクセス
```

**DevUIの使い方:**
1. ブラウザで `http://localhost:5000` を開く
2. 右上のドロップダウンからエージェントを選択（GPT, Claude, Gemini, Grok）
3. メッセージを入力して送信
4. 各エージェントの個性的な回答を楽しむ

## Important Notes

### CLI Mode

- **ラウンド数**: 全員が発言するには最低5ラウンド推奨。複数回の議論には10以上を設定
- **時間**: 各ラウンドでAPIを呼ぶため、10ラウンドで2-3分程度かかる
- **API料金**: 4つのLLMを同時に使うため、通常の4倍のAPI料金がかかる

### DevUI Mode

- 現在は**個別エージェントとのチャットのみ**対応
- グループチャット機能はCLIモードで利用可能
- `0.0.0.0:5000` でホストするため、同一ネットワーク内からアクセス可能（セキュリティ注意）

### General

- **API Keys**: 4つ全てのAPIキーが必要。1つでも欠けるとエラー
- **Rate Limits**: 各プロバイダーのレート制限に注意
- **日本語対応**: 全エージェントが日本語で議論可能

## Use Cases

```bash
# 技術的な質問
uv run python -m llm_fight_club.main "RAGの最新トレンド教えて" -r 10

# 意見が分かれそうな話題
uv run python -m llm_fight_club.main "React vs Vue、2025年はどっち？" -r 10

# 哲学的な議論
uv run python -m llm_fight_club.main "AIに意識は生まれるか？" -r 10

# 雑な質問
uv run python -m llm_fight_club.main "なんか面白いことない？" -r 5
```

## Project Structure

```
llm-fight-club/
├── README.md
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
│
├── src/llm_fight_club/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── devui_server.py      # DevUI server
│   ├── config.py            # Configuration
│   ├── prompts.py           # YAML prompt loader
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py          # Legacy base class
│   │   └── maf_agents.py    # MAF ChatAgent factories
│   │
│   ├── clients/
│   │   ├── __init__.py
│   │   └── litellm_client.py  # LiteLLM wrapper
│   │
│   └── workflows/
│       ├── __init__.py
│       └── group_chat.py    # Group chat workflow
│
├── prompts/                 # Agent personalities (YAML)
│   ├── orchestrator.yaml
│   ├── gpt.yaml
│   ├── claude.yaml
│   ├── gemini.yaml
│   └── grok.yaml
│
└── tests/
    └── ...
```

## License

MIT

---

*"Ask once, watch them fight, get the answer."*
