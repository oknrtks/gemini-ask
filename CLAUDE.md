# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Gemini APIを使用したCLIツールおよびMCPサーバー。Google Search機能を備えており、最新情報に基づいた回答が可能。

## 開発環境

- **パッケージマネージャ**: `uv` を使用
- **Pythonバージョン**: >= 3.10
- **依存ライブラリ**: google-genai, python-dotenv, fastmcp

## よく使うコマンド

```bash
# 依存関係のインストール
uv sync

# CLIツールの実行（開発中）
uv run gemini-ask "質問内容"

# モデル指定
uv run gemini-ask "質問内容" --model "gemini-2.5-pro"

# パッケージビルド
uv build

# MCPサーバーの実行
uv run gemini-ask-mcp

# MCP Inspectorでツール確認
npx @modelcontextprotocol/inspector uv run gemini-ask-mcp
```

## 環境変数の設定

以下のいずれかの環境変数が必要（`.env`ファイルで設定可能）:

- `GEMINI_API_KEY`（優先）
- `GOOGLE_API_KEY`

## アーキテクチャ

### CLIツール
- **エントリーポイント**: `src/gemini_ask/gemini_ask.py:main()`
- **CLI定義**: argparseを使用
  - `query`: 必須の位置引数（質問内容）
  - `--model`: オプション（デフォルト: `gemini-2.5-flash`）

### MCPサーバー
- **エントリーポイント**: `src/gemini_ask/mcp_server.py:main()`
- **サーバー名**: `gemini_ask_mcp`
- **ツール**: `gemini_ask_query`
  - Pydantic v2で入力バリデーション
  - JSON/Markdown両対応
  - Google Search機能有効化

### API呼び出し
- `google-genai`ライブラリを使用し、Google Searchツールを有効化
