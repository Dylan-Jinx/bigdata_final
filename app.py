from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import settings
from common.JsonFlask import JsonFlask
# 注意导包顺序 因为别的包已经要用到db了 这时候db必须在那些包前面初始化
app = JsonFlask(__name__)
app.config.from_object(settings.Configs)
db = SQLAlchemy(app)
from common.ApiResponse import ApiResponse
from controller.city_data_controller import cityDataModule
from controller.statistics_controller import statisticsModule
from controller.single_various_analysis_controller import singleVariousModule
from model import BigData
from utils.O2d import O2d
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(cityDataModule, url_prefix='/cityData')
app.register_blueprint(statisticsModule, url_prefix='/statistics')
app.register_blueprint(singleVariousModule, url_prefix='/singleVarious')


@app.route('/')
def hello_world():
    return ApiResponse.success(data=O2d.obj_to_list(BigData.query.all()))


@app.errorhandler(Exception)
def error_handler(e):
    return ApiResponse.error(msg=str(e))


if __name__ == '__main__':
    app.run()
