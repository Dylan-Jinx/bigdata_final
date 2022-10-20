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
def get_box_plot_by_cityName():
    year = request.values.get("year")
    datas = list(BigData.query.filter(not_(BigData.city_ratio == 0))
                 .filter(not_(BigData.income == 0))
                 .filter(not_(BigData.theil_index == 0))
                 .filter(not_(BigData.population == 0))
                 .filter_by(year=year))
    data1_list = []
    data1_list.append(get_list_selected_attr_by_attrname(datas, "income"))
    data1_list.append(get_list_selected_attr_by_attrname(datas, "population"))

    plt.figure(figsize=(8.4, 4.8))  # 画布
    plt.subplot(1, 2, 1)
    plt.grid(True)  # 显示网格
    plt.boxplot(data1_list,
                labels=("总收入", "人口"),  # 为箱线图添加标签，类似于图例的作用
                sym="g+",  # 异常点形状，默认为蓝色的“+”
                showmeans=True  # 是否显示均值，默认不显示
                )
    plt.title("总收入与总人口指标的箱线图")

    plt.subplot(1, 2, 2)
    data2_list = []
    data2_list.append(get_list_selected_attr_by_attrname(datas, "city_ratio"))
    data2_list.append(get_list_selected_attr_by_attrname(datas, "theil_index"))
    plt.boxplot(data2_list,
                labels=("城镇化率", "泰尔指数"),
                sym="g+",  # 异常点形状，默认为蓝色的“+”
                showmeans=True  # 是否显示均值，默认不显示
                )
    plt.title("城镇化率、泰尔指数指标的箱线图")
    plt.tight_layout()
    plt.savefig('box_line.png')
    pic1 = return_img_stream('box_line.png')
    plt.close()
    return ApiResponse.success(
        data=pic1
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
    return ApiResponse.success(
        data=result
    )


@singleVariousModule.route("/getHistogramChartByYear")
def get_histogram_chart_by_cityName():
    year = request.values.get('year')
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
