import numpy as np
import pandas as pd
from flask import Blueprint, request
from matplotlib import pyplot as plt
from matplotlib.pyplot import scatter
from scipy.stats import gaussian_kde

from common.ApiResponse import ApiResponse
import seaborn as sns

from model import BigData
from utils.imageConvert import return_img_stream
from utils.list_object_deal import get_list_selected_attr_by_attrname

doubleVariousModule = Blueprint('doubleVariousModule', __name__)


@doubleVariousModule.route("/correlation")
def correlation():
    # 相关系数矩阵
    np.random.seed(1)  # 随机种子
    mat = pd.DataFrame(np.random.rand(3, 6), columns=list('abcdef')).corr()
    sns.heatmap(mat, cmap='YlGnBu', fmt='.3f', annot=True)
    plt.show()

    return ApiResponse.success()


@doubleVariousModule.route("/scatterByColName")
def scatter_graph_by_colName():
    col_name1 = request.values.get('colName1')
    col_name2 = request.values.get('colName2')
    datas = BigData.query.all()
    data1_list = []
    fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
    d1 = get_list_selected_attr_by_attrname(datas, col_name1)
    d2 = get_list_selected_attr_by_attrname(datas, col_name2)
    xy = np.vstack([d1, d2])
    z = gaussian_kde(xy)(xy)
    scatter = ax.scatter(d1, d2, marker='o', c=z, s=15, label='LST', cmap='Spectral_r')
    cbar = plt.colorbar(scatter, shrink=1, orientation='vertical', extend='both', pad=0.015, aspect=30,
                        label='frequency')  # ori
    plt.title("相关联系散点图")
    plt.tight_layout()
    plt.savefig('scatter.png')
    pic1 = return_img_stream('scatter.png')
    plt.close()
    return ApiResponse.success(
        data=pic1
    )
