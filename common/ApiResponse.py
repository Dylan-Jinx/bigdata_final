import datetime


class ApiResponse(object):

    def __init__(self, data, code, msg, currentTime):
        self.data = data
        self.code = code
        self.msg = msg
        self.currentTime = currentTime

    @classmethod
    def success(cls, data=None, code=20000, msg='获取成功'):
        return cls(data, code, msg, datetime.datetime.now())

    @classmethod
    def error(cls, data=None, code=20000, msg='获取成功'):
        return cls(data, code, msg, datetime.datetime.now())

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "currentTime": self.currentTime,
            "data": self.data
        }
