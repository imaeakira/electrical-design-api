from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import traceback

# 標準ライブラリのインポート
import math
import decimal
import fractions
import statistics
import random
import itertools
import collections
import functools
import operator
import datetime
import time
import re
import copy
import enum
import dataclasses
import abc
import warnings
import heapq
import bisect
import array
import uuid
import hashlib
import base64
import unicodedata
import string
import textwrap
import pprint

# typing関連
from typing import (
    List, Dict, Any, Tuple, Optional, Union, Set, FrozenSet,
    Callable, Iterator, Iterable, Sequence, Mapping, MutableMapping,
    Type, TypeVar, Generic, Protocol, Final, Literal, TypedDict,
    NamedTuple, ClassVar, cast, overload, runtime_checkable,
    get_type_hints, get_origin, get_args
)

# collections関連の追加インポート
from collections import (
    defaultdict, Counter, OrderedDict, deque,
    namedtuple, ChainMap, UserDict, UserList, UserString
)

# dataclasses関連
from dataclasses import dataclass, field, fields, asdict, astuple

# enum関連
from enum import Enum, IntEnum, Flag, IntFlag, auto

app = FastAPI()

# CORSを有効化（すべてのオリジンからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        # 電気設備設計で使用可能な標準ライブラリを含むグローバル環境
        global_env = {
            "__builtins__": __builtins__,
            
            # 数学・計算関連
            "math": math,
            "decimal": decimal,
            "fractions": fractions,
            "statistics": statistics,
            "random": random,
            "operator": operator,
            
            # データ構造・アルゴリズム
            "itertools": itertools,
            "collections": collections,
            "functools": functools,
            "heapq": heapq,
            "bisect": bisect,
            "array": array,
            
            # collections の個別クラス
            "defaultdict": defaultdict,
            "Counter": Counter,
            "OrderedDict": OrderedDict,
            "deque": deque,
            "namedtuple": namedtuple,
            "ChainMap": ChainMap,
            "UserDict": UserDict,
            "UserList": UserList,
            "UserString": UserString,
            
            # 日時処理
            "datetime": datetime,
            "time": time,
            
            # 文字列処理
            "re": re,
            "string": string,
            "textwrap": textwrap,
            "unicodedata": unicodedata,
            
            # データ処理
            "json": json,
            "copy": copy,
            "pprint": pprint,
            "base64": base64,
            "hashlib": hashlib,
            "uuid": uuid,
            
            # 型定義・クラス定義
            "enum": enum,
            "Enum": Enum,
            "IntEnum": IntEnum,
            "Flag": Flag,
            "IntFlag": IntFlag,
            "auto": auto,
            "dataclasses": dataclasses,
            "dataclass": dataclass,
            "field": field,
            "fields": fields,
            "asdict": asdict,
            "astuple": astuple,
            "abc": abc,
            "warnings": warnings,
            
            # typing関連のすべて
            "typing": __import__("typing"),
            "List": List,
            "Dict": Dict,
            "Any": Any,
            "Tuple": Tuple,
            "Optional": Optional,
            "Union": Union,
            "Set": Set,
            "FrozenSet": FrozenSet,
            "Callable": Callable,
            "Iterator": Iterator,
            "Iterable": Iterable,
            "Sequence": Sequence,
            "Mapping": Mapping,
            "MutableMapping": MutableMapping,
            "Type": Type,
            "TypeVar": TypeVar,
            "Generic": Generic,
            "Protocol": Protocol,
            "Final": Final,
            "Literal": Literal,
            "TypedDict": TypedDict,
            "NamedTuple": NamedTuple,
            "ClassVar": ClassVar,
            "cast": cast,
            "overload": overload,
            "runtime_checkable": runtime_checkable,
            "get_type_hints": get_type_hints,
            "get_origin": get_origin,
            "get_args": get_args,
        }
        
        local_vars = {}
        
        # コードを実行
        try:
            exec(request.code, global_env, local_vars)
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

# 利用可能なライブラリ一覧を返すエンドポイント
@app.get("/available-libraries")
async def available_libraries():
    return {
        "status": "success",
        "libraries": {
            "math": "数学関数（sin, cos, sqrt, pi等）",
            "decimal": "十進演算（高精度計算）",
            "fractions": "分数演算",
            "statistics": "統計関数",
            "random": "乱数生成",
            "itertools": "効率的なループ処理",
            "collections": "特殊なコンテナデータ型",
            "functools": "関数型プログラミングツール",
            "datetime": "日付と時刻の操作",
            "re": "正規表現",
            "json": "JSON処理",
            "enum": "列挙型",
            "dataclasses": "データクラス",
            "typing": "型ヒント（完全対応）",
            "その他": "copy, uuid, hashlib, base64等"
        }
    }

# ルートエンドポイント（ブラウザからのアクセス確認用）
@app.get("/")
async def root():
    return {"message": "電気設備設計自動化 Python API サーバー稼働中"}
