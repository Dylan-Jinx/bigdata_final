import numpy as np
from flask import Blueprint, request

from common.ApiResponse import ApiResponse
from model import BigData
from statistics.descriptive import data_descriptive_statistics
from utils.O2d import O2d
from utils.list_object_deal import get_list_attr_by_attrname
from sqlalchemy import not_

statisticsModule = Blueprint('statisticsModule', __name__)


@statisticsModule.route("/getAllDataDescription")
def get_all_data_description():

    datas = list(BigData.query.all())
    datas_ex_shenZhen = BigData.query.filter(not_(BigData.name == '深圳市')).all()
    datas_ex_cityIncomePopulationRatioIsZero = BigData.query.filter(not_(BigData.city_income_population_ratio == 0.0)).all()

    datas_ex_villageAbleIncomeRatio = BigData.query\
        .filter(not_(BigData.village_able_income_ratio == 0.0))\
        .filter(not_(BigData.name == '深圳市')) \
        .all()

    datas_ex_villagePopulationIsZero = BigData.query\
        .filter(not_(BigData.village_population == 0))\
        .all()

    datas_ex_villagePopulationRatio = BigData.query\
        .filter(not_(BigData.village_population_ratio == 0))\
        .all()

    datas_ex_villageIncome = BigData.query\
        .filter(not_(BigData.village_income == 0))\
        .all()

    whole_description = {}
    city_able_income = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'city_able_income')))
    village_able_income = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_shenZhen, 'village_able_income')))
    population = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'population')))
    city_population = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'city_population')))
    village_population = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas_ex_villagePopulationIsZero, 'village_population')))
    income = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'income')))
    city_income = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'city_income')))
    village_income = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas_ex_villageIncome, 'village_income')))
    city_able_income_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas, 'city_able_income_ratio')))
    city_population_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas, 'city_population_ratio')))
    village_able_income_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_villageAbleIncomeRatio, 'village_able_income_ratio')))
    village_population_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_villagePopulationRatio, 'village_population_ratio')))
    village_income_population_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_shenZhen, 'village_income_population_ratio')))
    city_income_population_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_cityIncomePopulationRatioIsZero, 'city_income_population_ratio')))
    theil_index = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas_ex_shenZhen, 'theil_index')))
    city_ratio = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'city_ratio')))

    whole_description.__setitem__("city_able_income", city_able_income)
    whole_description.__setitem__("village_able_income", village_able_income)
    whole_description.__setitem__("population", population)
    whole_description.__setitem__("city_population", city_population)
    whole_description.__setitem__("village_population", village_population)
    whole_description.__setitem__("income", income)
    whole_description.__setitem__("city_income", city_income)
    whole_description.__setitem__("village_income", village_income)
    whole_description.__setitem__("city_able_income_ratio", city_able_income_ratio)
    whole_description.__setitem__("city_population_ratio", city_population_ratio)
    whole_description.__setitem__("village_able_income_ratio", village_able_income_ratio)
    whole_description.__setitem__("village_population_ratio", village_population_ratio)
    whole_description.__setitem__("village_income_population_ratio", village_income_population_ratio)
    whole_description.__setitem__("city_income_population_ratio", city_income_population_ratio)
    whole_description.__setitem__("theil_index", theil_index)
    whole_description.__setitem__("city_ratio", city_ratio)

    return ApiResponse.success(
        data=whole_description
    )


@statisticsModule.route("/getAllDataDescriptionByColName")
def get_data_description_by_colName():
    datas = list(BigData.query.all())
    cityName = request.values.get('cityName')
    selectedVal = np.array(get_list_attr_by_attrname(datas, 'city_population'))
    result = O2d.obj_to_dic(data_descriptive_statistics(selectedVal))
    return ApiResponse.success(
        data=result
    )


@statisticsModule.route("/getDataDescriptionByCityName")
def get_data_description_by_cityName():
    cityName = request.values.get('cityName')
    print(cityName)
    datas = BigData.query.filter_by(name=cityName).all()
    whole_description = {}

    datas_ex_shenZhen = BigData.query.filter(not_(BigData.name == '深圳市')).all()
    datas_ex_cityIncomePopulationRatioIsZero = BigData.query.filter(
        not_(BigData.city_income_population_ratio == 0.0))\
        .filter_by(name=cityName)\
        .all()

    datas_ex_villageAbleIncomeRatio = BigData.query \
        .filter(not_(BigData.village_able_income_ratio == 0.0)) \
        .filter(not_(BigData.name == '深圳市')) \
        .filter_by(name=cityName)\
        .all()

    datas_ex_villagePopulationIsZero = BigData.query \
        .filter_by(name=cityName) \
        .filter(not_(BigData.village_population == 0)) \
        .all()

    datas_ex_villagePopulationRatio = BigData.query \
        .filter_by(name=cityName)\
        .filter(not_(BigData.village_population_ratio == 0)) \
        .all()

    datas_ex_villageIncome = BigData.query \
        .filter_by(name=cityName)\
        .filter(not_(BigData.village_income == 0)) \
        .all()

    city_able_income = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'city_able_income')))
    village_able_income = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_shenZhen, 'village_able_income')))
    population = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'population')))
    city_population = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'city_population')))
    village_population = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_villagePopulationIsZero, 'village_population')))
    income = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'income')))
    city_income = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'city_income')))
    village_income = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_villageIncome, 'village_income')))
    city_able_income_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas, 'city_able_income_ratio')))
    city_population_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas, 'city_population_ratio')))
    village_able_income_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_villageAbleIncomeRatio, 'village_able_income_ratio')))
    village_population_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_villagePopulationRatio, 'village_population_ratio')))
    village_income_population_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_shenZhen, 'village_income_population_ratio')))
    city_income_population_ratio = data_descriptive_statistics(
        np.array(get_list_attr_by_attrname(datas_ex_cityIncomePopulationRatioIsZero, 'city_income_population_ratio')))
    theil_index = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas_ex_shenZhen, 'theil_index')))
    city_ratio = data_descriptive_statistics(np.array(get_list_attr_by_attrname(datas, 'city_ratio')))

    whole_description.__setitem__("city_able_income", city_able_income)
    whole_description.__setitem__("village_able_income", village_able_income)
    whole_description.__setitem__("population", population)
    whole_description.__setitem__("city_population", city_population)
    whole_description.__setitem__("village_population", village_population)
    whole_description.__setitem__("income", income)
    whole_description.__setitem__("city_income", city_income)
    whole_description.__setitem__("village_income", village_income)
    whole_description.__setitem__("city_able_income_ratio", city_able_income_ratio)
    whole_description.__setitem__("city_population_ratio", city_population_ratio)
    whole_description.__setitem__("village_able_income_ratio", village_able_income_ratio)
    whole_description.__setitem__("village_population_ratio", village_population_ratio)
    whole_description.__setitem__("village_income_population_ratio", village_income_population_ratio)
    whole_description.__setitem__("city_income_population_ratio", city_income_population_ratio)
    whole_description.__setitem__("theil_index", theil_index)
    whole_description.__setitem__("city_ratio", city_ratio)
    return ApiResponse.success(
        msg=cityName,
        data=whole_description
    )
