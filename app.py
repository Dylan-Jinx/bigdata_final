import pandas as pd
from flask import render_template

import pretreatment.data_precondition as dp
from common.JsonFlask import JsonFlask
from tableinfo.table_baseinfo import get_table_header

from common.ApiResponse import ApiResponse

pd.set_option('display.max_rows', None)

app = JsonFlask(__name__)


def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream


@app.route('/')
def hello_world():  # put application's code here
    datas = pd.read_excel('static/data.xlsx')
    print(datas)
    return 'Hello World!'


@app.route('/test')
def test():
    dp.graph()
    img_stream = return_img_stream('test.png')
    return render_template('index.html', img_stream=img_stream)


@app.route('/getTableHeader')
def getTableHeader():
    return ApiResponse.success(data=get_table_header())


@app.errorhandler(Exception)
def error_handler(e):
    return ApiResponse.error(msg=str(e))


if __name__ == '__main__':
    app.run()
