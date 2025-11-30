# LLM Fight Club - 実装メモ

## 更新履歴

| No. | 日付 | 内容 | ステータス |
|-----|------|------|-----------|
| 001 | 2025-11-29 | プロジェクト構成・エージェント実装 | 完了 |
| 002 | 2025-11-29 | YAMLプロンプト管理に移行 | 完了 |
| 003 | 2025-11-29 | ユニットテスト追加（29件通過） | 完了 |
| 004 | 2025-11-29 | MAF調査（MagenticBuilder採用決定） | 完了 |
| 005 | 2025-11-29 | ドキュメント作成・日本語化 | 完了 |
| 006 | 2025-11-29 | 接続テストスクリプト作成 | 完了 |
| 007 | - | ローカル環境で接続テスト実行 | 待機中 |
| 008 | - | LiteLLMChatClient実装 | 未着手 |
| 009 | - | MagenticBuilder統合 | 未着手 |

---

## 概要

GPT、Claude、Gemini、Grokがトピックについて議論するマルチLLMグループチャットシステム。オーケストレーター（OpenAI gpt-4o-mini）がファシリテーターとして進行を管理する。

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
│  StandardMagenticManager (OpenAI gpt-4o-mini - オーケストレーター)  │
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

---

## 完了した作業

### 001: プロジェクト構成

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
│   ├── conftest.py
│   └── unit/test_agents/
├── scripts/
│   └── test_openai.py     # 接続テスト
└── docs/
    └── implementation-notes.md
```

### 002: エージェント実装 (LiteLLM)

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
| Orchestrator | `openai/gpt-4o-mini` | なし（調整のみ） |

### 003: 環境変数

`.env`に必要:

```
GOOGLE_API_KEY=
XAI_API_KEY=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
```

### 004: ユニットテスト

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

### 005: 接続テストスクリプト

```bash
# ローカル環境で実行
uv run python scripts/test_openai.py
```

期待される出力:
```
Testing OpenAI connection...
API Key: sk-proj-xxxxx...xxxx

Success! Response:
こんにちは！
```

---

## 未完了の作業

### 007: ローカル接続テスト（待機中）
- `.env`にAPIキーを設定
- `scripts/test_openai.py`を実行して接続確認
- 各プロバイダーのテストスクリプトを追加予定

### 008: LiteLLMChatClient
- LiteLLM用のMAF `ChatClientProtocol`ラッパーを実装
- メッセージフォーマット変換を処理（MAF <-> LiteLLM）

### 009: MagenticBuilder統合
- OpenAIで`StandardMagenticManager`を設定
- 4つのエージェントを参加者として追加
- `group_chat.py`ワークフローを実装

---

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

---

## 設計上の決定

1. **LangChainよりLiteLLM**: シンプル、LLMコールのみに特化、MAFとの相性が良い
2. **YAMLプロンプト**: 関心の分離、パーソナリティの変更が容易
3. **プロバイダー固有検索**: 各モデルが自身の検索機能を使用し最良の結果を得る
4. **srcレイアウト**: Pythonパッケージ構成のベストプラクティス
5. **MAF MagenticBuilder**: 公式フレームワーク、カスタムグループチャット実装なし
