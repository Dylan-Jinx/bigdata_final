import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.set_option('display.max_row', None)
data_file_path = 'static/data.xlsx'
# data_file_path = '/Users/jinx/Desktop/Python_big_data_final/bigdata_final/static/data.xlsx'
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
fig_width = 600
fig_heigh = 600


def data_loading():
    datas = pd.read_excel(data_file_path)
    return datas


def select_province_data(datas, province_name):
    return datas[datas['dum'].__eq__(province_name)]


def graph():
    datas = data_loading()
    temp = select_province_data(datas, '北京市')
    print(temp)
    # plt.figure(figsize=(fig_width, fig_heigh))
    plt.subplot(221)
    sns.lineplot(x='year', y='P1/P', data=temp)
    plt.subplot(222)
    sns.lineplot(x='year', y='P2/P', data=temp)
    plt.subplot(223)
    sns.lineplot(x='year', y='城镇化率', data=temp)
    plt.subplot(224)
    sns.lineplot(x='year', y='泰尔指数', data=temp)
    plt.tight_layout()
    plt.savefig('test.png', dpi=600)



