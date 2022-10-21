import os
from datetime import datetime

import tensorflow as tf
from flask import Blueprint, request
from keras import Sequential
from keras.layers import Dense
from keras.losses import mean_squared_error
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from common.ApiResponse import ApiResponse
from model import BigData
from utils.imageConvert import return_img_stream
from utils.list_object_deal import all_data_convert_dataFrame

machineLearningModule = Blueprint('machineLearningModule', __name__)
# 中文乱码解决方法
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Microsoft YaHei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


@machineLearningModule.route("/useMultiLayerPerception", methods=['POST'])
def use_multilayer_perception():
    os.popen("tensorboard --logdir=./ --port 6018 --host 0.0.0.0")
    datas = BigData.query.all()
    df = all_data_convert_dataFrame(datas)

    param1 = request.json.get('param1')
    param2 = request.json.get('param2')
    para_batch = int(request.json.get('batch'))
    para_feature_hidden = int(request.json.get('feature_hidden'))
    para_max_epoch = int(request.json.get('max_epoch'))


    # 分割测试集和训练集
    X_train, X_test, y_train, y_test = train_test_split(df[[param1, param2]], df[['总收入']],
                                                        test_size=0.3,
                                                        random_state=0)

    # 数据规范化处理
    X_train = MinMaxScaler().fit_transform(X_train)
    y_train = MinMaxScaler().fit_transform(y_train)
    X_test = MinMaxScaler().fit_transform(X_test)
    y_test = MinMaxScaler().fit_transform(y_test)

    # 多层感知机模型参数定义
    m = len(X_train)  # 维度
    feature = 2  # 特征数
    feature_hidden = para_batch  # 隐藏层的神经元数量
    # 超参数
    batch = para_feature_hidden
    eta = 0.01
    max_epoch = para_max_epoch

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
    ln_x_test = range(len(X_test))
    plt.title('测试集数值')
    plt.plot(ln_x_test, y_test, 'blue', lw=2, label='测试值')
    ln_y_test_pred = range(len(y_test_pred))
    plt.savefig('ml_test.png')
    plt.close()
    plt.title('测试集预测值')
    plt.plot(ln_y_test_pred, y_test_pred, 'orange', lw=2, label='测试预测值')
    plt.savefig('ml_test_pred.png')
    plt.close()

    r2 = r2_score(y_test, y_test_pred)
    rmse = mean_squared_error(y_test, y_test_pred)
    pic1 = return_img_stream('ml_test.png')
    pic2 = return_img_stream('ml_test_pred.png')
    result = {
            "pic1": pic1,
            "pic2": pic2,
            "r2": r2,
            "rmse": "{1:f}".format(r2, rmse[-1])
        }
    return ApiResponse.success(
        data=result
    )


