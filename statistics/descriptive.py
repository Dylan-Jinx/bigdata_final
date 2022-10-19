import numpy as np

from utils.O2d import O2d


def data_descriptive_statistics(data: np.ndarray) -> dict:
    desc = Description(
        data.min(), data.max(), data.mean(), data.std(), np.median(data), data.var(), data.ptp()
    )
    return O2d.obj_to_dic(desc)


class Description:
    def __init__(self, minVal, maxVal, avgVal, stdVal, midVal, varianceVal, rangeVal):
        self.minVal = minVal
        self.maxVal = maxVal
        self.avgVal = avgVal
        # 标准差
        self.stdVal = stdVal
        self.midVal = midVal
        # 方差
        self.varianceVal = varianceVal
        # 极差
        self.rangeVal = rangeVal

