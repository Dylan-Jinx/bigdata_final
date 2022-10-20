import os
import shutil

import numpy as np
import seaborn as sns
from matplotlib import cm
from matplotlib import pyplot as plt
from sqlalchemy import not_

from model import BigData
from utils.imageConvert import return_img_stream
from utils.list_object_deal import get_list_selected_attr_by_attrname, get_key_val_by_query_datas

# 中文乱码解决方法
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def draw_pie_chart_by_value_and_label(values, title, colors):
    income_label = '城市', '农村'
    explode = (0, 0)
    plt.pie(values, explode=explode, labels=income_label, autopct='%1.1f%%',
            shadow=False, startangle=90, colors=colors)
    plt.axis('equal')
    plt.title(title)


def draw_comparative_with_pie(datas):
    plt.subplot(2, 2, 1)
    city_income = get_list_selected_attr_by_attrname(datas, 'city_income')
    village_income = get_list_selected_attr_by_attrname(datas, 'village_income')
    income_list = (city_income[-1], village_income[-1])
    # 数据和颜色挂钩
    colors = cm.Paired(np.arange(len(income_list)) / len(income_list))
    draw_pie_chart_by_value_and_label(income_list, '城市与农村收入比', colors)

    plt.subplot(2, 2, 2)
    city_able_income = get_list_selected_attr_by_attrname(datas, 'city_able_income')
    village_able_income = get_list_selected_attr_by_attrname(datas, 'village_able_income')
    able_income_list = (city_able_income[-1], village_able_income[-1])
    colors = cm.Accent(np.arange(len(able_income_list)) / len(able_income_list))
    draw_pie_chart_by_value_and_label(able_income_list, '城市与农村可支配收入比', colors)

    plt.subplot(2, 2, 3)
    city_population = get_list_selected_attr_by_attrname(datas, 'city_population')
    village_population = get_list_selected_attr_by_attrname(datas, 'village_population')
    popu_list = (city_population[-1], village_population[-1])
    colors = cm.tab10(np.arange(len(popu_list)) / len(popu_list))
    draw_pie_chart_by_value_and_label(popu_list, '城市与农村人口比', colors)

    plt.subplot(2, 2, 4)
    city_ratio = get_list_selected_attr_by_attrname(datas, 'city_ratio')
    city_ratio_list = (city_ratio[-1], 1 - city_ratio[-1])
    colors = cm.Pastel1(np.arange(len(city_ratio_list)) / len(city_ratio_list))
    draw_pie_chart_by_value_and_label(popu_list, '城镇化', colors)
    plt.tight_layout()
    plt.savefig('pie.png')
    plt.close()
    return return_img_stream('pie.png')


def draw_dist_plot_by_data_and_info(
        datas, xlabel, title
):
    key, value = get_key_val_by_query_datas(datas)
    sns.distplot(value,
                 hist=True,
                 kde=True,  # 开启核密度曲线kernel density estimate (KDE)
                 kde_kws={'linestyle': '--', 'linewidth': '1', 'color': '#c72e29',
                          # 设置外框线属性
                          },
                 color='#098154'
                 )
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel("分布", fontsize=20)
    plt.title(title, fontsize=20)


def year_intensify_graph_picture(year):
    plt.figure(dpi=120, figsize=(15, 10))
    datas = BigData.query \
        .filter_by(year=year) \
        .all()
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

    plt.subplot(4, 4, 1)
    sns.kdeplot(village_income)
    plt.title("乡村收入")
    plt.subplot(4, 4, 2)
    sns.kdeplot(village_able_income_ratio)
    plt.title("乡村可支配收入")
    plt.subplot(4, 4, 3)
    sns.kdeplot(village_population_ratio)
    plt.title("乡村人口")
    plt.subplot(4, 4, 4)
    sns.kdeplot(village_income_population_ratio)
    plt.title("乡村收入与人口比")
    plt.subplot(4, 4, 5)
    sns.kdeplot(city_income_population_ratio)
    plt.title("城市收入与人口比")
    plt.subplot(4, 4, 6)
    sns.kdeplot(theil_index)
    plt.title("泰尔指数")
    plt.subplot(4, 4, 7)
    sns.kdeplot(city_ratio)
    plt.title("城镇化")
    plt.subplot(4, 4, 8)
    sns.kdeplot(village_able_income)
    plt.title("乡村可支配收入")
    plt.subplot(4, 4, 9)
    sns.kdeplot(population)
    plt.title("总人口")
    plt.subplot(4, 4, 10)
    sns.kdeplot(city_population)
    plt.title("城市人口")
    plt.subplot(4, 4, 11)
    sns.kdeplot(village_population)
    plt.title("乡村人口")
    plt.subplot(4, 4, 12)
    sns.kdeplot(income)
    plt.title("总收入")
    plt.subplot(4, 4, 13)
    sns.kdeplot(city_income)
    plt.title("城市收入")
    plt.subplot(4, 4, 14)
    sns.kdeplot(city_able_income)
    plt.title("城市可支配收入")
    plt.subplot(4, 4, 15)
    sns.kdeplot(city_able_income_ratio)
    plt.title("城市可支配收入比")
    plt.subplot(4, 4, 16)
    sns.kdeplot(city_population_ratio)
    plt.title("城市人口比")
    plt.legend()
    plt.tight_layout()
    plt.savefig("year_intensify.png")
    plt.close()
    return return_img_stream("year_intensify.png")


def total_intensify_graph_picture():
    plt.figure(dpi=120, figsize=(15, 10))
    datas = BigData.query \
        .all()
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

    plt.subplot(4, 4, 1)
    sns.kdeplot(village_income)
    plt.title("乡村收入")
    plt.subplot(4, 4, 2)
    sns.kdeplot(village_able_income_ratio)
    plt.title("乡村可支配收入")
    plt.subplot(4, 4, 3)
    sns.kdeplot(village_population_ratio)
    plt.title("乡村人口")
    plt.subplot(4, 4, 4)
    sns.kdeplot(village_income_population_ratio)
    plt.title("乡村收入与人口比")
    plt.subplot(4, 4, 5)
    sns.kdeplot(city_income_population_ratio)
    plt.title("城市收入与人口比")
    plt.subplot(4, 4, 6)
    sns.kdeplot(theil_index)
    plt.title("泰尔指数")
    plt.subplot(4, 4, 7)
    sns.kdeplot(city_ratio)
    plt.title("城镇化")
    plt.subplot(4, 4, 8)
    sns.kdeplot(village_able_income)
    plt.title("乡村可支配收入")
    plt.subplot(4, 4, 9)
    sns.kdeplot(population)
    plt.title("总人口")
    plt.subplot(4, 4, 10)
    sns.kdeplot(city_population)
    plt.title("城市人口")
    plt.subplot(4, 4, 11)
    sns.kdeplot(village_population)
    plt.title("乡村人口")
    plt.subplot(4, 4, 12)
    sns.kdeplot(income)
    plt.title("总收入")
    plt.subplot(4, 4, 13)
    sns.kdeplot(city_income)
    plt.title("城市收入")
    plt.subplot(4, 4, 14)
    sns.kdeplot(city_able_income)
    plt.title("城市可支配收入")
    plt.subplot(4, 4, 15)
    sns.kdeplot(city_able_income_ratio)
    plt.title("城市可支配收入比")
    plt.subplot(4, 4, 16)
    sns.kdeplot(city_population_ratio)
    plt.title("城市人口比")
    plt.legend()
    plt.tight_layout()
    plt.savefig("total_intensify.png")
    plt.close()
    return return_img_stream("total_intensify.png")
