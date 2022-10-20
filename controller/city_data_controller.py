from flask import Blueprint, request
from sqlalchemy import between

from app import db
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


@cityDataModule.route("getCityNames")
def get_city_names():
    datas = db.session.query(BigData.name).all()
    result = []
    for i in datas:
        result.append(i[0])
    return ApiResponse.success(data=list(set(result)))


@cityDataModule.route("getCityHeader")
def get_city_header():
    whole_description = {}
    whole_description.__setitem__("city_able_income", "城市可支配收入")
    whole_description.__setitem__("village_able_income", "乡村可支配收入")
    whole_description.__setitem__("population", "人口")
    whole_description.__setitem__("city_population", "城市人口")
    whole_description.__setitem__("village_population", "乡村人口")
    whole_description.__setitem__("income", "收入")
    whole_description.__setitem__("city_income", "城市收入")
    whole_description.__setitem__("village_income", "乡村收入")
    whole_description.__setitem__("city_able_income_ratio", "城市可支配收入比")
    whole_description.__setitem__("city_population_ratio", "城市人口比")
    whole_description.__setitem__("village_able_income_ratio", "乡村可支配收入比")
    whole_description.__setitem__("village_population_ratio", "乡村人口比")
    whole_description.__setitem__("village_income_population_ratio", "乡村可支配收入与人口比")
    whole_description.__setitem__("city_income_population_ratio", "城市收入与人口比")
    whole_description.__setitem__("theil_index", "泰尔指数")
    whole_description.__setitem__("city_ratio", "城镇化率")
    return ApiResponse.success(
        data=whole_description
    )
