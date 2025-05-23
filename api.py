from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import traceback
import os

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
import typing
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

# CORSを有効化（APPからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://electrical-design-app.web.app", "https://electrical-design-app.firebaseapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        # 安全な組み込み関数のみを選択
        safe_builtins = {
            # 基本的な型と関数
            'abs': abs, 'all': all, 'any': any, 'bool': bool,
            'bytes': bytes, 'chr': chr, 'complex': complex,
            'dict': dict, 'divmod': divmod, 'enumerate': enumerate,
            'filter': filter, 'float': float, 'format': format,
            'frozenset': frozenset, 'hash': hash, 'hex': hex,
            'int': int, 'isinstance': isinstance, 'issubclass': issubclass,
            'iter': iter, 'len': len, 'list': list, 'map': map,
            'max': max, 'min': min, 'next': next, 'oct': oct,
            'ord': ord, 'pow': pow, 'print': print, 'range': range,
            'repr': repr, 'reversed': reversed, 'round': round,
            'set': set, 'slice': slice, 'sorted': sorted, 'str': str,
            'sum': sum, 'tuple': tuple, 'type': type, 'zip': zip,
            # 安全な例外クラス
            'Exception': Exception, 'ValueError': ValueError,
            'TypeError': TypeError, 'KeyError': KeyError,
            'IndexError': IndexError, 'AttributeError': AttributeError,
            'ZeroDivisionError': ZeroDivisionError,
            # その他の安全な組み込み
            'None': None, 'True': True, 'False': False,
            'NotImplemented': NotImplemented,
        }
        
        # 電気設備設計で使用可能な標準ライブラリを含むグローバル環境
        global_env = {
            "__builtins__": safe_builtins,
            
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
            # __import__は削除（セキュリティのため）
            "typing": typing,
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

# テスト用のエンドポイント - OPTIONS対応
@app.options("/test")
@app.get("/test")
async def test():
    return {"status": "success", "message": "API is working!"}

# 実行エンドポイントにもOPTIONSを追加
@app.options("/execute")
async def options_execute():
    return {}

# 利用可能なライブラリ一覧を返すエンドポイント
@app.get("/available-libraries")
async def available_libraries():
    return {
        "status": "success",
        "libraries": {
            "math": "数学関数（sin, cos, sqrt, pi等）",
            "decimal": "十進演算（高精度計算）",
            "fractions": "分数演算",
            "statistics": "統計関数（平均、標準偏差等）",
            "random": "乱数生成",
            "itertools": "効率的なループ処理（組み合わせ、順列等）",
            "collections": "特殊なコンテナデータ型",
            "functools": "関数型プログラミングツール",
            "datetime": "日付と時刻の操作",
            "re": "正規表現",
            "json": "JSON処理",
            "enum": "列挙型",
            "dataclasses": "データクラス",
            "typing": "型ヒント（完全対応）",
            "copy": "オブジェクトのコピー",
            "uuid": "UUID生成",
            "hashlib": "ハッシュ関数",
            "base64": "Base64エンコード/デコード",
            "その他": "heapq, bisect, array, pprint等"
        },
        "使用例": {
            "面積計算": "math.pi * radius ** 2",
            "座標計算": "math.sqrt((x2-x1)**2 + (y2-y1)**2)",
            "組み合わせ": "list(itertools.combinations(items, 2))",
            "型ヒント": "def calculate(points: List[Tuple[float, float]]) -> float:"
        },
        "セキュリティ": {
            "利用不可": "os, sys, subprocess, socket, urllib等のシステム操作・ネットワーク関連",
            "制限事項": "ファイル操作、外部通信、システムコマンド実行は不可"
        }
    }

# ルートエンドポイント（ブラウザからのアクセス確認用）
@app.get("/")
async def root():
    return {"message": "電気設備設計自動化 Python API サーバー稼働中"}
