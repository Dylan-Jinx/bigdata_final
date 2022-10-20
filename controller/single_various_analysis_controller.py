import numpy as np
import seaborn as sns
from flask import Blueprint, request
from matplotlib import pyplot as plt
from sqlalchemy import not_

from app import db
from common.ApiResponse import ApiResponse
from model import BigData
from utils.O2d import O2d
from utils.imageConvert import return_img_stream
from utils.list_object_deal import get_list_selected_attr_by_attrname, get_key_val_by_query_datas
from utils.singleVariousGraphDrawUtil import draw_comparative_with_pie, draw_dist_plot_by_data_and_info, \
    total_intensify_graph_picture, year_intensify_graph_picture

singleVariousModule = Blueprint('singleVariousModule', __name__)


@singleVariousModule.route('/getBoxPlotByCityName')
# TODO:
def get_box_plot_by_cityName():
    datas = BigData.query.all()
    whole_description = {}

    datas_ex_shenZhen = BigData.query.filter(not_(BigData.name == '深圳市')).all()
    datas_ex_cityIncomePopulationRatioIsZero = BigData.query.filter(
        not_(BigData.city_income_population_ratio == 0.0)).all()

    datas_ex_villageAbleIncomeRatio = BigData.query \
        .filter(not_(BigData.village_able_income_ratio == 0.0)) \
        .filter(not_(BigData.name == '深圳市')) \
        .all()

    datas_ex_villagePopulationIsZero = BigData.query \
        .filter(not_(BigData.village_population == 0)) \
        .all()

    datas_ex_villagePopulationRatio = BigData.query \
        .filter(not_(BigData.village_population_ratio == 0)) \
        .all()

    datas_ex_villageIncome = BigData.query \
        .filter(not_(BigData.village_income == 0)) \
        .all()

    village_able_income = get_list_selected_attr_by_attrname(datas_ex_villageAbleIncomeRatio, 'village_able_income')
    population = get_list_selected_attr_by_attrname(datas, 'population')

    city_population = get_list_selected_attr_by_attrname(datas, 'city_population')
    village_population = get_list_selected_attr_by_attrname(datas, 'village_population')
    income = get_list_selected_attr_by_attrname(datas, 'population')

    city_income = get_list_selected_attr_by_attrname(datas, 'city_income')
    city_able_income = get_list_selected_attr_by_attrname(datas, 'city_able_income')

    city_able_income_ratio = get_list_selected_attr_by_attrname(datas, 'city_able_income_ratio')
    city_population_ratio = get_list_selected_attr_by_attrname(datas, 'city_population_ratio')
    village_able_income_ratio = get_list_selected_attr_by_attrname(datas, 'village_able_income_ratio')

    village_population_ratio = get_list_selected_attr_by_attrname(datas, 'village_population_ratio')
    village_income_population_ratio = get_list_selected_attr_by_attrname(datas, 'village_income_population_ratio')
    city_income_population_ratio = get_list_selected_attr_by_attrname(datas, 'city_income_population_ratio')

    theil_index = get_list_selected_attr_by_attrname(datas, 'theil_index')
    city_ratio = get_list_selected_attr_by_attrname(datas, 'city_ratio')
    village_income = get_list_selected_attr_by_attrname(datas, 'village_income')

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

    keyList = []

    for i in whole_description.keys():
        keyList.append(i)

    for temp in keyList:
        sns.boxplot(temp, whole_description.get(temp), width=0.3)
    plt.show()

    return ApiResponse.success(
    )


@singleVariousModule.route('/getPieChartDataByCityName')
def get_pie_chart_data_by_cityName():
    cityName = request.values.get('cityName')
    datas = BigData.query \
        .filter_by(name=cityName) \
        .all()
    return ApiResponse.success(data=O2d.obj_to_list(datas))


@singleVariousModule.route('/getPieChartByCityNameAndColName')
def get_pie_chart_by_cityName_and_ColName():
    cityName = request.values.get('cityName')
    datas = BigData.query \
        .filter_by(name=cityName) \
        .all()
    result = draw_comparative_with_pie(datas)
    print(result)
    return ApiResponse.success(
        data=result
    )


@singleVariousModule.route("/getHistogramChartByYear")
def get_histogram_chart_by_cityName():
    year = request.values.get('year')
    print(year)
    datas = db.session.query(BigData.name, BigData.population) \
        .filter(not_(BigData.population == 0)) \
        .filter_by(year=year) \
        .all()
    plt.figure(dpi=120, figsize=(30, 13))
    plt.subplot(1, 2, 1)
    draw_dist_plot_by_data_and_info(datas, "人口值", "人口密度曲线")
    plt.subplot(1, 2, 2)
    datas = db.session.query(BigData.name, BigData.income).filter(not_(BigData.income == 0)) \
        .filter_by(year=year) \
        .all()
    draw_dist_plot_by_data_and_info(datas, "收入值", "收入密度曲线")
    plt.savefig("displot1.png")
    pic1 = return_img_stream("displot1.png")
    plt.close()
    datas = db.session.query(BigData.name, BigData.city_ratio) \
        .filter(not_(BigData.city_ratio == 0)) \
        .filter_by(year=year) \
        .all()
    plt.figure(dpi=120, figsize=(30, 13))
    plt.subplot(1, 2, 1)
    draw_dist_plot_by_data_and_info(datas, "城镇化率", "城镇化率曲线")
    plt.subplot(1, 2, 2)
    datas = db.session.query(BigData.name, BigData.theil_index).filter(not_(BigData.theil_index == 0)) \
        .filter_by(year=year) \
        .all()
    draw_dist_plot_by_data_and_info(datas, "泰尔指数", "泰尔指数密度曲线")
    plt.savefig("displot2.png")
    pic2 = return_img_stream("displot2.png")
    plt.close()
    result = {
        "pic1": pic1,
        "pic2": pic2
    }
    return ApiResponse.success(
        data=result
    )


@singleVariousModule.route("/getIntensifyChartByYear")
def get_intensify_chart_by_cityName():
    year = request.values.get("year")
    pic1 = total_intensify_graph_picture()
    pic2 = year_intensify_graph_picture(year)
    result = {
        "pic1": pic1,
        "pic2": pic2
    }
    return ApiResponse.success(
        data=result
    )
