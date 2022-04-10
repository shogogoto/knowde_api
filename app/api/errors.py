from typing import List, Type
from fastapi import FastAPI


class ApiError(Exception):
    pass

# https://tech.jxpress.net/entry/fastapi_error_definitions
# def error_response(error_types: List[Type[ApiError]]) -> dict:
def error_response(error_types) -> dict:
    # error_types に列挙した ApiError を OpenAPI の書式で定義する
    d = {}
    for et in error_types:
        if not d.get(et.status_code):
            d[et.status_code] = {
                'description': f'"{et.detail}"',
                'content': {
                    'application/json': {
                        'example': {
                            'detail': et.detail
                        }
                    }
                }}
        else:
            # 同じステータスコードなら description へ追記
            d[et.status_code]['description'] += f'<br>"{et.detail}"'
    return d


