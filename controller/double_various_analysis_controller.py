from datetime import datetime

import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from flask import Blueprint, request
from keras import Sequential
from keras.layers import Dense
from keras.losses import mean_squared_error
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from common.ApiResponse import ApiResponse
from model import BigData
from utils.imageConvert import return_img_stream
from utils.list_object_deal import get_list_selected_attr_by_attrname, all_data_convert_dataFrame

doubleVariousModule = Blueprint('doubleVariousModule', __name__)
# 中文乱码解决方法
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


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


@doubleVariousModule.route("/getAllRelativeGraph")
def get_all_relative_graph():
    datas = BigData.query.all()
    df = all_data_convert_dataFrame(datas)
    sns.set(style="ticks", font=['Arial Unicode MS', 'Microsoft YaHei', 'SimHei', 'sans-serif'])
    sns.pairplot(df, kind='reg', diag_kind='kde')
    plt.tight_layout()
    plt.savefig('回归分析.png', dpi=300)
    plt.close()
    pic1 = return_img_stream('回归分析.png')
    return ApiResponse.success(
        data=pic1
    )


@doubleVariousModule.route("/getRelativeHeatmap")
def get_relative_heatmap():
    datas = BigData.query.all()
    df = all_data_convert_dataFrame(datas)
    _, ax = plt.subplots(figsize=(16, 13))
    plt.title('城市与乡村各项指标基于Pearson相关系数的热力图', fontsize=20)
    corr = df.corr(method='pearson')
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, cmap="Blues", square=True, annot=True, ax=ax, annot_kws={'fontsize': 16},
                cbar_kws={'shrink': .9})
    plt.savefig('pearson1.png')
    plt.show()
    plt.close()
    corr = df.corr(method='spearman')
    _, ax = plt.subplots(figsize=(16, 13))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, cmap=cmap, square=True, annot=True, ax=ax, annot_kws={'fontsize': 16},
                cbar_kws={'shrink': .9})
    plt.title('城市与乡村各项指标基于Spearman相关系数的热力图', fontsize=20)
    plt.savefig('pearson2.png')
    plt.close()


    pic1 = return_img_stream('pearson1.png')
    pic2 = return_img_stream('pearson2.png')

    return ApiResponse.success(
        data={
            "pic1": pic1,
            "pic2": pic2
        }
    )


@doubleVariousModule.route("/useMultiLayerPerception")
def use_multilayer_perception():
    datas = BigData.query.all()
    df = all_data_convert_dataFrame(datas)
    # 分割测试集和训练集
    X_train, X_test, y_train, y_test = train_test_split(df[['城镇化', '总收入', '泰尔指数', '总人口']], df[['总收入']],
                                                        test_size=0.3,
                                                        random_state=0)

    # 数据规范化处理
    X_train = MinMaxScaler().fit_transform(X_train)
    y_train = MinMaxScaler().fit_transform(y_train)
    X_test = MinMaxScaler().fit_transform(X_test)
    y_test = MinMaxScaler().fit_transform(y_test)

    # 多层感知机模型参数定义
    m = len(X_train)  # 维度
    feature = 4  # 特征数
    feature_hidden = 20  # 隐藏层的神经元数量
    # 超参数
    batch = 20
    eta = 0.01
    max_epoch = 100

    model = Sequential()
    model.add(Dense(feature_hidden, input_dim=feature, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.summary()

    model.compile(loss='mean_squared_error', optimizer='adam')

    log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=max_epoch, batch_size=batch, verbose=1,
              callbacks=[tensorboard_callback])

    model.save('train_model/' + datetime.now().strftime("%Y%m%d-%H%M%S") + '/')

    y_test_pred = model.predict(X_test)
    y_train_pred = model.predict(X_train)
    r2 = r2_score(y_test, y_test_pred)
    rmse = mean_squared_error(y_test, y_test_pred)
    print(r2)
    print(rmse)
    print("R2 : {0:f}, RMSE : {1:f}".format(r2, rmse[-1]))
