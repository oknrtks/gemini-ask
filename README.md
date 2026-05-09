# gemini-ask

Gemini APIを使用したCLIツールおよびMCPサーバー。Google Search機能を備えており、最新情報に基づいた回答が可能。

## インストール

**GitHubから直接実行（推奨）:**

```bash
uvx git+https://github.com/oknrtks/gemini-ask "質問内容"
```

**ローカルインストール:**

```bash
uvx --from /path/to/gemini-ask gemini-ask "質問内容"
# または
uv run gemini-ask "質問内容"
```

## 使用方法

### CLIツール

```bash
# 基本的な使用方法
gemini-ask "今日の天気は？"

# モデルを指定
gemini-ask "量子力学について教えて" --model "gemini-2.5-pro"
```

### MCPサーバー

```bash
# MCPサーバーとして実行
gemini-ask-mcp

# MCP Inspectorで確認
npx @modelcontextprotocol/inspector gemini-ask-mcp
```

**MCPサーバーのツール**:
- `gemini_ask_query`: Gemini AIに質問して回答を取得（Google Search有効）

## 環境変数

以下のいずれかの環境変数を設定してください：

- `GEMINI_API_KEY` (優先)
- `GOOGLE_API_KEY`

`.env`ファイルを使用することもできます。

## 依存関係

- Python >= 3.10
- fastmcp >= 3.2.4
- google-genai >= 1.63.0
- python-dotenv >= 1.2.1
