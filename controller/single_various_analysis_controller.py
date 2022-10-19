import seaborn as sns
from flask import Blueprint
from matplotlib import pyplot as plt
from sqlalchemy import not_

from common.ApiResponse import ApiResponse
from model import BigData
from utils.list_object_deal import get_list_selected_attr_by_attrname
from utils.singleVariousGraphDrawUtil import draw_pie_chart_by_value_and_label

singleVariousModule = Blueprint('singleVariousModule', __name__)


@singleVariousModule.route('/getBoxPlotByCityName')
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


@singleVariousModule.route('/getPieChartByCityNameAndColName')
def get_pie_chart_by_cityName_and_ColName():
    datas = BigData.query \
        .filter_by(name='漳州市') \
        .all()
    city_income = get_list_selected_attr_by_attrname(datas, 'city_income')
    village_income = get_list_selected_attr_by_attrname(datas, 'village_income')
    print(city_income)
    print(village_income)

    income_label = 'village', 'city'
    plt.subplot(1,2,1)
    draw_pie_chart_by_value_and_label(income_label, (city_income[-1], village_income[-1]))
    plt.subplot(1, 2, 2)
    draw_pie_chart_by_value_and_label(income_label, (city_income[-1], village_income[-1]))
    plt.show()

    return ApiResponse.success()
