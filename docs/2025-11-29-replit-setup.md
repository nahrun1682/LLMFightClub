# Replit環境セットアップ記録

**日付**: 2025年11月29日

## 概要

LLM Fight ClubプロジェクトをReplit環境にセットアップし、4つのLLMエージェント（GPT、Claude、Gemini、Grok）が正常に動作することを確認した。

## 実施内容

### 1. Azure OpenAIからOpenAIへの移行

**変更ファイル:**
- `src/llm_fight_club/agents/orchestrator.py`
- `src/llm_fight_club/config.py`

**変更内容:**
- OrchestratorAgentのモデルを `azure/gpt-4o-mini` から `openai/gpt-4o-mini` に変更
- Azure関連の設定（AZURE_OPENAI_API_KEY、AZURE_OPENAI_ENDPOINT）を削除
- 4つのAPIキーのみに簡素化:
  - OPENAI_API_KEY
  - ANTHROPIC_API_KEY
  - GOOGLE_API_KEY
  - XAI_API_KEY

### 2. モデル名の修正（LiteLLM互換）

各エージェントのモデル名をLiteLLM互換バージョンに更新:

| エージェント | 変更前 | 変更後 |
|-------------|--------|--------|
| GPT | openai/gpt-4o | openai/gpt-4o |
| Claude | anthropic/claude-sonnet-4-20250514 | anthropic/claude-3-5-haiku-20241022 |
| Gemini | gemini/gemini-1.5-pro | gemini/gemini-2.0-flash |
| Grok | xai/grok-beta | xai/grok-2-latest |

### 3. ウェブ検索機能の一時無効化

LiteLLM互換性の問題により、各エージェントのウェブ検索パラメータを一時的に無効化:

**変更ファイル:**
- `src/llm_fight_club/agents/gpt.py`
- `src/llm_fight_club/agents/claude.py`
- `src/llm_fight_club/agents/gemini.py`
- `src/llm_fight_club/agents/grok.py`

**変更内容:**
```python
# 変更前（例: GPT）
def get_extra_params(self) -> dict[str, Any]:
    return {"tools": [{"type": "web_search_preview"}]}

# 変更後
def get_extra_params(self) -> dict[str, Any]:
    return {}
```

### 4. テストのmock削除と実APIテストへの変更

**変更ファイル:**
- `tests/conftest.py`
- `tests/unit/test_agents/test_gpt.py`
- `tests/unit/test_agents/test_claude.py`
- `tests/unit/test_agents/test_gemini.py`
- `tests/unit/test_agents/test_grok.py`

**変更内容:**
- conftest.pyからmock fixtureを削除
- APIキー存在確認用のskip fixtureを追加
- 各テストファイルで実際のAPIを呼び出すテストに変更
- テスト結果をprint出力するように追加

### 5. main.pyの実装

グループチャット機能の基本実装を追加:

**機能:**
- 4つのエージェント（GPT、Claude、Gemini、Grok）が参加
- OrchestratorAgentが議論を管理
- 指定されたラウンド数で各エージェントが順番に発言
- 最後にファシリテーターがまとめを生成

## テスト結果

### 実行コマンド
```bash
uv run pytest tests/unit/test_agents/ -v -s
```

### 結果: 全12テスト成功

各エージェントの応答例（質問: 「どう？今日の調子は？」）:

```
[GPT] 今日は調子がいいですよ！皆さんの話題を楽しみにしています。
      どんな話題でもサポートしますので、お気軽にどうぞ。

[Claude] はい、なかなか興味深い質問ですね。今日の調子は悪くありませんが、
         これは本当に重要な話題でしょうか？少し掘り下げて、
         具体的にどんな意図があるのか教えていただけますか？

[Gemini] 今日の調子ですか？私は大規模言語モデルなので、
         感情や体調といった概念はありません。
         常に一定のパフォーマンスを維持できるように設計されています。

[Grok] 今日の調子？Xでみんなが言ってるけど、
       調子なんて気にしないで、トレンドに乗っかって楽しむのが一番だよ！
       どうせみんなが同じこと考えてるんだから、ちょっと挑戦してみる？
```

**各エージェントの個性が反映されていることを確認:**
- GPT: バランス良く協調的
- Claude: 批判的・掘り下げ系
- Gemini: データドリブン・事実重視
- Grok: 挑発的・Xネタ

## 次のステップ

1. グループチャット（main.py）の動作確認
2. ウェブ検索機能の再有効化（LiteLLM互換性解決後）
3. 追加テストの実装

## 設定済みAPIキー

- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GOOGLE_API_KEY
- XAI_API_KEY
