import cmd
import os
import subprocess

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import settings
from common.JsonFlask import JsonFlask
from logs_output_core.generation_log import red_logs

# 注意导包顺序 因为别的包已经要用到db了 这时候db必须在那些包前面初始化
app = JsonFlask(__name__)
app.config.from_object(settings.Configs)
db = SQLAlchemy(app)
from common.ApiResponse import ApiResponse
from controller.city_data_controller import cityDataModule
from controller.statistics_controller import statisticsModule
from controller.single_various_analysis_controller import singleVariousModule
from controller.double_various_analysis_controller import doubleVariousModule
from model import BigData
from utils.O2d import O2d

CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(cityDataModule, url_prefix='/cityData')
app.register_blueprint(statisticsModule, url_prefix='/statistics')
app.register_blueprint(singleVariousModule, url_prefix='/singleVarious')
app.register_blueprint(doubleVariousModule, url_prefix='/doubleVarious')

line_number = [0]
x = None


@app.route('/')
def hello_world():
    return ApiResponse.success(data=O2d.obj_to_list(BigData.query.all()))


@app.route("/getLogs")
def get_log():
    log_data = red_logs()  # 获取日志
    # 判断如果此次获取日志行数减去上一次获取日志行数大于0，代表获取到新的日志
    if len(log_data) - line_number[0] > 0:
        log_type = 2  # 当前获取到日志
        log_difference = len(log_data) - line_number[0]  # 计算获取到少行新日志
        log_list = []  # 存放获取到的新日志
        # 遍历获取到的新日志存放到log_list中
        for i in range(log_difference):
            log_i = log_data[-(i + 1)].decode('utf-8')  # 遍历每一条日志并解码
            log_list.insert(0, log_i)  # 将获取的日志存放log_list中
    else:
        log_type = 3
        log_list = ''
    # 已字典形式返回前端
    _log = {
        'log_type': log_type,
        'log_list': log_list
    }
    line_number.pop()  # 删除上一次获取行数
    line_number.append(len(log_data))  # 添加此次获取行数
    return _log


# @app.errorhandler(Exception)
# def error_handler(e):
#     return ApiResponse.error(msg=str(e))



if __name__ == '__main__':
    app.run()
