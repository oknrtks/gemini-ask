import os
import sys
import argparse
from google import genai
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

## os.environに、まずGEMINI_API_KEYがあるか確認し、なければGOOGLE_API_KEYを確認する。いずれもなければエラーを出す。
API_KEY = ""

def check_api_key():
    global API_KEY
    if "GEMINI_API_KEY" in os.environ:
        API_KEY = os.environ["GEMINI_API_KEY"]
    elif "GOOGLE_API_KEY" in os.environ:
        API_KEY = os.environ["GOOGLE_API_KEY"]
    return 

def ask_gemini(query: str, model: str) -> str:
    # client = genai.Client(API_KEY)
    client = genai.Client(api_key=API_KEY)
    config = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )

    response = client.models.generate_content(
        model=model,
        contents=query,
        config=config
    )

    print(response.text)

def main():
    # argparse にて以下の引数を受ける
    # query: 質問内容を指定する必須引数。オプションではない。
    # model: 使用するGeminiモデルを指定します。デフォルトは "gemini-2.5-flash" です。オプショナル。
    parser = argparse.ArgumentParser(description="Gemini APIを使用して質問に答えるサンプルコード")   
    parser.add_argument("query", help="質問内容を指定します。")
    parser.add_argument("--model", help="使用するGeminiモデルを指定します。デフォルトは \"gemini-3.5-flash\" です。", default="gemini-3.5-flash")
    args = parser.parse_args()  
    check_api_key()
    if API_KEY == "":
        print("Error: No API key found. Please set GEMINI_API_KEY or GOOGLE_API_KEY in your environment variables.")
        return
    ask_gemini(args.query, args.model)
    
if __name__ == "__main__":
    main()