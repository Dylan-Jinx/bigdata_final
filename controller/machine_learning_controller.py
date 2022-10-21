from datetime import datetime
import tensorflow as tf
from flask import Blueprint
from keras import Sequential
from keras.layers import Dense
from keras.losses import mean_squared_error
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from model import BigData
from utils.list_object_deal import all_data_convert_dataFrame

machineLearningModule = Blueprint('machineLearningModule', __name__)
# 中文乱码解决方法
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


@machineLearningModule.route("/useMultiLayerPerception")
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
