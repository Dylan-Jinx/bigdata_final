class ApiResponse(object):

    def __init__(self, data, code, msg):
        self.data = data
        self.code = code
        self.msg = msg

    @classmethod
    def success(cls, data=None, code=20000, msg='获取成功'):
        return cls(data, code, msg)

    @classmethod
    def error(cls, data=None, code=20000, msg='获取成功'):
        return cls(data, code, msg)

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }
