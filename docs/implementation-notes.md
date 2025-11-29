# LLM Fight Club - 実装メモ

## 概要

GPT、Claude、Gemini、Grokがトピックについて議論するマルチLLMグループチャットシステム。オーケストレーター（Azure OpenAI）がファシリテーターとして進行を管理する。

## 技術スタック

| コンポーネント | 技術 | 用途 |
|---------------|------|------|
| オーケストレーション | Microsoft Agent Framework (MAF) | グループチャットワークフロー |
| LLMインターフェース | LiteLLM | 全プロバイダー統一API |
| 検索 | 各プロバイダー固有 | 各モデルの組み込み検索機能 |

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│                    MagenticBuilder                       │
├─────────────────────────────────────────────────────────┤
│  StandardMagenticManager (Azure OpenAI - オーケストレーター)  │
│    - 計画を作成                                          │
│    - 進捗を追跡                                          │
│    - 次に話すエージェントを決定                            │
│    - 最終回答をまとめる                                   │
├─────────────────────────────────────────────────────────┤
│  参加者:                                                 │
│    ├── ChatAgent(Gemini) ─── LiteLLMChatClient          │
│    ├── ChatAgent(Grok) ──── LiteLLMChatClient           │
│    ├── ChatAgent(Claude) ── LiteLLMChatClient           │
│    └── ChatAgent(GPT) ───── LiteLLMChatClient           │
└─────────────────────────────────────────────────────────┘
```

## 完了した作業

### 1. プロジェクト構成

```
LLMFightClub/
├── src/llm_fight_club/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py          # 環境変数の読み込み
│   ├── prompts.py         # YAMLプロンプトローダー
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py        # LiteLLM使用のBaseAgent
│   │   ├── gemini.py      # Google検索有効
│   │   ├── grok.py        # X/web/news検索有効
│   │   ├── claude.py      # Web検索有効
│   │   ├── gpt.py         # Web検索有効
│   │   └── orchestrator.py
│   └── workflows/
│       ├── __init__.py
│       └── group_chat.py  # TODO: MAF実装
├── prompts/
│   ├── gemini.yaml
│   ├── grok.yaml
│   ├── claude.yaml
│   ├── gpt.yaml
│   └── orchestrator.yaml
├── tests/
│   ├── conftest.py        # モック付きpytestフィクスチャ
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

### 2. エージェント実装 (LiteLLM)

各エージェントは`BaseAgent`を継承し、統一APIコールにLiteLLMを使用。

**BaseAgentの機能:**
- `litellm.acompletion()`を使用した非同期`respond()`メソッド
- `prompts.py`経由のYAMLベースシステムプロンプト
- メッセージ履歴サポート
- プロバイダー固有の追加パラメータ

**プロバイダー別検索パラメータ:**

| エージェント | モデル | 検索設定 |
|-------------|--------|----------|
| Gemini | `gemini/gemini-1.5-pro` | `{"tools": [{"googleSearch": {}}]}` |
| Grok | `xai/grok-beta` | `{"search_parameters": {"mode": "on", "sources": ["x", "web", "news"]}}` |
| Claude | `anthropic/claude-sonnet-4-20250514` | `{"tools": [{"type": "web_search_20250305"}]}` |
| GPT | `openai/gpt-4o` | `{"tools": [{"type": "web_search_preview"}]}` |
| Orchestrator | `azure/gpt-4o` | なし（調整のみ） |

### 3. 環境変数

`.env`に必要:

```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
GOOGLE_API_KEY=
XAI_API_KEY=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
```

### 4. ユニットテスト

モック化されたLiteLLMレスポンスで29テスト通過。

```bash
uv run python -m pytest tests/ -v
```

テスト対象:
- Message/AgentResponseデータクラス
- エージェント初期化
- YAMLからのシステムプロンプト読み込み
- 追加パラメータ（検索設定）
- APIキー処理
- 履歴付きメッセージ構築
- 非同期respondメソッド

## 未完了の作業

### Phase 1: 接続テスト
- `scripts/test_connections.py`を作成
- 実際のAPIキーで各エージェントの接続を確認
- 検索機能をテスト

### Phase 2: LiteLLMChatClient
- LiteLLM用のMAF `ChatClientProtocol`ラッパーを実装
- メッセージフォーマット変換を処理（MAF <-> LiteLLM）

### Phase 3: MagenticBuilder統合
- Azure OpenAIで`StandardMagenticManager`を設定
- 4つのエージェントを参加者として追加
- `group_chat.py`ワークフローを実装

### Phase 4: 統合テスト
- 実際のマルチLLM議論を実行
- オーケストレーションロジックを検証

## MAF調査メモ

### 利用可能なパターン

| パターン | 説明 |
|---------|------|
| `MagenticBuilder` | マネージャー・ワーカー型オーケストレーション |
| `SequentialBuilder` | 固定順序実行 |
| `ConcurrentBuilder` | 並列実行 |

### MAFの主要コンポーネント

- `ChatAgent` - ChatClientをインストラクション付きでラップ
- `ChatClientProtocol` - LLMプロバイダー用インターフェース
- `StandardMagenticManager` - オーケストレーターロジック
- `MagenticBuilder` - ワークフロービルダー

### なぜMagenticBuilder？

GroupChatBuilderはインストール済みパッケージではまだ利用不可。MagenticBuilderはMagentic-Oneパターンを実装しており、以下を提供:
- 自動計画
- 進捗追跡
- 動的エージェント選択
- 最終回答の統合

これは本質的に、インテリジェントなオーケストレーターを持つ高度なグループチャット。

## 設計上の決定

1. **LangChainよりLiteLLM**: シンプル、LLMコールのみに特化、MAFとの相性が良い
2. **YAMLプロンプト**: 関心の分離、パーソナリティの変更が容易
3. **プロバイダー固有検索**: 各モデルが自身の検索機能を使用し最良の結果を得る
4. **srcレイアウト**: Pythonパッケージ構成のベストプラクティス
5. **MAF MagenticBuilder**: 公式フレームワーク、カスタムグループチャット実装なし
