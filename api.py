from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import traceback

app = FastAPI()

# CORSを有効化（すべてのオリジンからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# テスト用のエンドポイント
@app.get("/test")
async def test():
    return {"status": "success", "message": "API is working!"}