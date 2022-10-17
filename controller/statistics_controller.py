import numpy as np
from flask import Blueprint, request

from common.ApiResponse import ApiResponse
from model import BigData
from statistics.descriptive import data_descriptive_statistics
from utils.O2d import O2d
from utils.list_object_deal import get_list_attr_by_attrname

statisticsModule = Blueprint('statisticsModule', __name__)


@statisticsModule.route("/getAllDataDescription")
def get_all_data_description():
    datas = list(BigData.query.all())
    selectedVal = np.array(get_list_attr_by_attrname(datas, 'city_population'))
    result = O2d.obj_to_dic(data_descriptive_statistics(selectedVal))
    return ApiResponse.success(
        data=result
    )


@statisticsModule.route("/getDataDescriptionByCityName")
def get_data_description_by_cityName():
    cityName = request.values.get('cityName')
    cityDatas = list(BigData.query.filter_by(name=cityName))
    selectedVal = np.array(get_list_attr_by_attrname(cityDatas, 'city_population'))
    result = O2d.obj_to_dic(data_descriptive_statistics(selectedVal))
    return ApiResponse.success(
        data=result
    )