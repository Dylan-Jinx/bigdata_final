import json

from flask import Blueprint, request
from sqlalchemy import between, and_

from common.ApiResponse import ApiResponse
from model import BigData
from utils.O2d import O2d

cityDataModule = Blueprint('cityDataModule', __name__)


@cityDataModule.route("dataPreview")
def data_preview():
    result = list(BigData.query.all())
    return ApiResponse.success(
        data=O2d.obj_to_list(result)
    )


@cityDataModule.route("/getDataByCityName")
def get_data_by_cityName():
    cityName = request.values.get('cityName')
    result = list(BigData.query.filter_by(name=cityName))
    return ApiResponse.success(
        data=O2d.obj_to_list(result)
    )


@cityDataModule.route("/getCityDataByNameAndYearOrYears")
def get_city_data_by_name_and_year_years():
    cityName = request.values.get('cityName')
    start_year = request.values.get('startYear')
    if request.values.get('yearFlag') == "0":
        result = list(BigData.query.filter_by(name=cityName, year=start_year))
    else:
        end_year = request.values.get('endYear')
        # filter用于区间函数 filter用于普通where
        result = list(BigData.query
                      .filter_by(name=cityName)
                      .filter(between(BigData.year, start_year, end_year)))
    return ApiResponse.success(
        data=O2d.obj_to_list(result)
    )


@cityDataModule.route("getCityMultipleData", methods=["POST"])
def get_city_single_data():
    cityNames = request.json
    print(cityNames)
    result = list(BigData.query.filter(BigData.name.in_(['北京市', '厦门市']))
                  )
    return ApiResponse.success(
        data=O2d.obj_to_list(result)
    )
