# 🥊 LLM Fight Club

> "The first rule of LLM Fight Club: You do not talk about which model is best."
> "The second rule: You let them fight it out."

同じ質問を4つのLLM（GPT, Claude, Gemini, Grok）に投げて、
グループチャットでわちゃわちゃ議論させる。

カオス上等。その中から答えが見えてくる。

## 🎯 What is this?

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

## 💡 Use Cases

```bash
# 技術的な質問
"RAGの最新トレンド教えて"
"uvとpoetryどっちがいい？"

# 意見が分かれそうな話題
"React vs Vue、2025年はどっち？"
"AIエージェントは本当に使えるのか？"

# ローカル情報
"浅草でおすすめのサウナは？"

# 最新情報
"今日の生成AI関連のニュース"

# 雑な質問
"なんか面白いことない？"
```

## 🎭 Agent Personalities

| Agent | 情報源 | 性格 | 議論での役割 |
|-------|--------|------|--------------|
| 🔍 **Gemini** | Google検索、公式発表 | 真面目、根拠重視 | データと事実を持ってくる |
| 🐦 **Grok** | X (Twitter) リアルタイム | 挑発的、煽り気味 | 「それXでは違うぞ」と突っ込む |
| 🧠 **Claude** | 深い分析、文脈理解 | 慎重、批評的 | 「本当にそう？」と疑問を投げる |
| 📝 **GPT** | バランス型 | まとめ上手、中立 | 議論を整理しようとする |
| 🎤 **進行役** | - | ファシリテーター | 議論を回す、煽る、収束させる |

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.12 |
| Package Manager | uv |
| Agent Framework | Microsoft Agent Framework (MAF) |
| Orchestrator | Azure OpenAI (gpt-4o-mini) |
| Participants | Gemini API, Grok API, Claude API, OpenAI API |
| UI | MAF DevUI |

## 📁 Repository Structure

```
LLMFightClub/
├── README.md
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
│
├── src/
│   └── llm_fight_club/
│       ├── __init__.py
│       ├── main.py                 # エントリーポイント
│       ├── config.py               # 設定・環境変数読み込み
│       │
│       ├── agents/                 # エージェント定義
│       │   ├── __init__.py
│       │   ├── base.py             # 共通ベースクラス
│       │   ├── orchestrator.py     # 進行役
│       │   ├── gemini.py
│       │   ├── grok.py
│       │   ├── claude.py
│       │   └── gpt.py
│       │
│       └── workflows/
│           ├── __init__.py
│           └── group_chat.py       # グループチャット
│
├── prompts/                        # プロンプトテンプレート (YAML)
│   ├── orchestrator.yaml
│   ├── gemini.yaml
│   ├── grok.yaml
│   ├── claude.yaml
│   └── gpt.yaml
│
└── examples/
    └── sample_output.md
```

## ⚙️ Setup

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
```

```env
# Azure OpenAI (Orchestrator)
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini

# Google Gemini
GOOGLE_API_KEY=your-google-api-key

# xAI Grok
XAI_API_KEY=your-xai-api-key

# Anthropic Claude
ANTHROPIC_API_KEY=your-anthropic-api-key

# OpenAI GPT
OPENAI_API_KEY=your-openai-api-key
```

## 🚀 Usage

### 基本: グループチャットで議論

```bash
uv run llm-fight-club "uvとpoetryどっちがいい？"
```

### ラウンド数を指定

```bash
uv run llm-fight-club "RAGの最新トレンド" --rounds 15
```

### DevUI で可視化

```bash
uv run devui ./src/llm_fight_club/agents
# http://localhost:8080 で議論をリアルタイム観戦
```

## 📤 Output Example

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥊 LLM Fight Club
   Question: uvとpoetryどっちがいい？
   Rounds: 12
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎤 進行役
   では、uvとpoetryの比較について議論を始めましょう。

🔍 Gemini
   公式ベンチマークによると、uvはpoetryの10-100倍高速です。
   Astral社が開発しており、Rustで書かれています。

🐦 Grok
   Xでは最近uv派がめっちゃ増えてる。特にAstralがRuff出してから
   信頼度上がってる感じ。「もうpoetry戻れない」って声多い。

🧠 Claude
   速度だけで選ぶのは早計では？poetryはpyproject.tomlの
   標準化に貢献してきた実績がありますし、エコシステムの
   成熟度も考慮すべきかと。

📝 GPT
   整理すると、uvは速度、poetryは安定性と実績ですね。
   プロジェクトの規模や要件で選ぶのが良さそうです。

🐦 Grok
   いや、2025年にもなってpoetry選ぶ理由ある？
   uvがpyproject.toml対応してる時点で移行しない理由ないだろ。

🧠 Claude
   既存プロジェクトの移行コストは？大規模なCI/CDパイプラインを
   組んでいる場合、「速いから」だけでは動けませんよ。

🔍 Gemini
   移行ガイドを確認しましたが、uv migrationコマンドで
   ほぼ自動移行できるようです。

...

🎤 進行役
   議論が収束してきましたね。まとめると、新規プロジェクトなら
   uv、既存で安定運用中ならpoetryを急いで変える必要はない、
   という結論でしょうか。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Stats: 12 rounds, 45 messages
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🗺️ Roadmap

### Phase 1: MVP

- [ ] プロジェクトセットアップ
- [ ] 各エージェント実装（検索機能付き）
- [ ] 進行役の実装
- [ ] Group Chatワークフロー
- [ ] CLI出力

### Phase 2: 改善

- [ ] DevUI統合
- [ ] 議論ログ保存
- [ ] 出力フォーマット改善

### Phase 3: 拡張

- [ ] WebUI
- [ ] 特定モデルのみで議論
- [ ] カスタムエージェント追加

## 📜 License

MIT

---

*"Ask once, watch them fight, get the answer."* 🥊
