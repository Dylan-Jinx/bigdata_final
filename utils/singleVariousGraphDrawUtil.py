import os
import shutil

import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt

from utils.imageConvert import return_img_stream
from utils.list_object_deal import get_list_selected_attr_by_attrname

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
