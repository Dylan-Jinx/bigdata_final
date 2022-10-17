import numpy as np


def data_descriptive_statistics(data: np.ndarray):
    desc = Description(
        data.min(), data.max(), data.mean(), data.std(), np.median(data), data.var(), data.ptp()
    )
    return desc


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

