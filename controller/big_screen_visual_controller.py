import threading
import time

from flask import Blueprint, request
from sqlalchemy import between, create_engine
from sqlalchemy.orm import sessionmaker

from app import db
from common.ApiResponse import ApiResponse
from model import BigData, City, Province
from utils.O2d import O2d
from utils.list_object_deal import get_list_selected_attr_by_attrname

bigScreenVisualModule = Blueprint('bigScreenVisualModule', __name__)


@bigScreenVisualModule.route("/getProvinceDataByColNameAndYear")
def get_province_data_by_colNameAndYear():
    time.sleep(3)
    engine_str = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format('root', '12345678', 'localhost', '3306', 'big_data_final')
    engine = create_engine(engine_str, encoding='utf-8')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    colName = request.values.get('name')
    year = request.values.get('year')
    datas = session.execute("SELECT province.`name`, SUM(bigdata."+colName+") AS 'value' FROM bigdata,city,province WHERE bigdata.`name` = city.`name` AND city.provincecode = province.`code` AND bigdata.`year` = "+year+" GROUP BY province.`name`")
    resultList = []
    for i in datas.fetchall():
        temp = bigVisualData(str(i.name).replace('市', '').replace('省', '').replace(' ',''), i.value)
        resultList.append(temp)
    return ApiResponse.success(
        data=O2d.obj_to_list(resultList)
    )


class bigVisualData:
    def __init__(self, name, value):
        self.name = name
        self.value = value
