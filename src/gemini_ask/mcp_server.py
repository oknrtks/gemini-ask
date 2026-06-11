import asyncio
import json
import logging
import os
from enum import Enum
from typing import Optional

from google import genai
from google.genai import types
from pydantic import BaseModel, Field, field_validator, ConfigDict
from fastmcp import FastMCP

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

mcp = FastMCP("gemini_ask_mcp")

# APIキー取得
API_KEY: Optional[str] = None


def _get_api_key() -> Optional[str]:
    global API_KEY
    if API_KEY is None:
        API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    return API_KEY


class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


class GeminiAskInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    query: str = Field(
        ...,
        description="質問内容（例: '今日の天気は？', '量子力学について教えて'）",
        min_length=1,
        max_length=200,
    )
    model: str = Field(
        default="gemini-3.5-flash",
        description="使用するGeminiモデル名（例: 'gemini-3.5-flash', 'gemini-3.1-pro-preview'）",
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="出力形式: 'markdown' または 'json'",
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("質問内容は必須です")
        return v.strip()


def _handle_error(e: Exception) -> str:
    if isinstance(e, ValueError):
        return f"Error: {e}"
    if "API key" in str(e):
        return "Error: APIキーが設定されていません。GEMINI_API_KEYまたはGOOGLE_API_KEY環境変数を設定してください。"
    return f"Error: 予期しないエラーが発生しました: {type(e).__name__}: {e}"


async def _format_markdown(response_text: str, query: str) -> str:
    return f"# Gemini AI 回答: {query}\n\n{response_text}"


async def _format_json(response_text: str, query: str) -> str:
    return json.dumps(
        {"query": query, "response": response_text},
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool(
    name="gemini_ask_query",
    annotations={
        "title": "Ask Gemini AI with Google Search",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def gemini_ask_query(params: GeminiAskInput) -> str:
    """Google検索を利用したAIアシスタント。質問に対して最新情報に基づいた回答を生成します。

    このツールはGoogle Gemini APIとGoogle検索を組み合わせて、最新の情報に基づいた回答を提供します。
    最新ニュース、現在の天気、株価など、最新の情報が必要な質問に対応しています。
    検索結果のリストではなく、分析された回答を提供します。

    Args:
        params (GeminiAskInput): 入力パラメータ
            - query (str): 質問内容（必須、1-200文字）
            - model (str): Geminiモデル名（デフォルト: 'gemini-3.5-flash'）
            - response_format (ResponseFormat): 出力形式（'markdown' または 'json'、デフォルト: 'markdown'）

    Returns:
        str: Gemini AIの回答（MarkdownまたはJSON形式）

        JSON形式:
        {
            "query": "質問内容",
            "response": "AIの回答"
        }

        Markdown形式: 質問と回答がフォーマットされたテキスト

    Examples:
        - gemini_ask_query(query="今日の天気は？")
        - gemini_ask_query(query="量子力学について教えて", model="gemini-3.1-pro-preview")
        - gemini_ask_query(query="最新のAI動向は？", response_format="json")

    Error Handling:
        - 入力検証エラー: Pydanticモデルで処理
        - APIキー未設定: 明確なエラーメッセージ
        - APIエラー: エラーの種類を示すメッセージ
    """
    api_key = _get_api_key()
    if not api_key:
        return _handle_error(ValueError("APIキーが設定されていません"))

    try:
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )

        response = await asyncio.to_thread(
            client.models.generate_content,
            model=params.model,
            contents=params.query,
            config=config,
        )

        if params.response_format == ResponseFormat.MARKDOWN:
            return await _format_markdown(response.text, params.query)
        return await _format_json(response.text, params.query)

    except Exception as e:
        logger.error(f"Gemini APIエラー: {e}")
        return _handle_error(e)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
