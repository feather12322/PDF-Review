from flask import jsonify
import time

def success_response(data=None, message="操作成功"):
    """成功响应"""
    return jsonify({
        "code": 200,
        "message": message,
        "data": data,
        "timestamp": int(time.time())
    }), 200

def error_response(message="操作失败", code=400):
    """错误响应"""
    return jsonify({
        "code": code,
        "message": message,
        "data": None,
        "timestamp": int(time.time())
    }), code
