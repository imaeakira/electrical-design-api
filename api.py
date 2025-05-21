from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import traceback
import os

app = FastAPI()

# CORSを有効化（すべてのオリジンからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # すべてのヘッダーを公開
)

# 静的ファイルの配信設定
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    print("静的ファイルディレクトリが見つかりません")

# リクエスト用モデル
class ExecuteRequest(BaseModel):
    code: str
    input_data: dict

@app.post("/execute")
async def execute_python(request: ExecuteRequest):
    try:
        # コードの安全な実行環境を作成
        local_vars = {}
        
        # コードを実行
        try:
            exec(request.code, {"__builtins__": __builtins__}, local_vars)
        except Exception as e:
            return {
                "status": "error",
                "message": f"コード実行エラー: {str(e)}",
                "traceback": traceback.format_exc()
            }
        
        # 関数の存在チェック
        if "arrange_equipment" not in local_vars:
            return {
                "status": "error", 
                "message": "arrange_equipment関数が見つかりません"
            }
        
        # 関数を実行
        try:
            result = local_vars["arrange_equipment"](request.input_data)
            return {"status": "success", "result": result}
        except Exception as e:
            return {
                "status": "error",
                "message": f"関数実行エラー: {str(e)}",
                "traceback": traceback.format_exc()
            }
            
    except Exception as e:
        return {
            "status": "error", 
            "message": f"予期せぬエラー: {str(e)}",
            "traceback": traceback.format_exc()
        }

# テスト用のエンドポイント - OPTIONS対応
@app.options("/test")
@app.get("/test")
async def test():
    return {"status": "success", "message": "API is working!"}

# 実行エンドポイントにもOPTIONSを追加
@app.options("/execute")
async def options_execute():
    return {}

# ルートエンドポイント（ブラウザからのアクセス確認用）
@app.get("/")
async def root():
    return {"message": "電気設備設計自動化 Python API サーバー稼働中"}
