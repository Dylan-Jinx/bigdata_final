from flask import Flask, jsonify

from common.ApiResponse import ApiResponse


class JsonFlask(Flask):
    def make_response(self, rv):
        """视图函数可以直接返回: list、dict、None"""
        if rv is None or isinstance(rv, (list, dict)):
            rv = ApiResponse.success(rv)

        if isinstance(rv, ApiResponse):
            rv = jsonify(rv.to_dict())

        return super().make_response(rv)
