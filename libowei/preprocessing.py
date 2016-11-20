# coding=utf-8
import pandas as pd
import numpy as np

# 列名
cols = ['肝气郁结证型系数', '热毒蕴结证型系数', '冲任失调证型系数', \
        '气血两虚证型系数', '脾胃虚弱证型系数', '肝肾阴虚证型系数']

# 删除有空值的行
def dropNull(data):
    return data.dropna()


# 用均值填补空值
def fillNullWithMean(data):
    # 0值替换为空
    # data = data.replace(0, np.nan)

    # 空值用平均值填补
    for col in cols:
        mean = data[col].describe().loc['mean'];
        data[col] = data[col].replace(np.nan, mean)
    return data


def deleteOutliers(data):
    # 计算统计值
    statistics = data.describe()
    min = statistics.loc['min']
    max = statistics.loc['max']
    mean = statistics.loc['mean']
    q1 = statistics.loc['25%']
    q3 = statistics.loc['75%']
    # 异常值边界
    high = q3 + 1.5 * (q3 - q1)
    low = q1 - 1.5 * (q3 - q1)
    # 去掉异常值
    index = data[cols[0]] > 0
    for i in range(5):
        index &= (data[cols[i]] < high[i]) & (data[cols[i]] > low[i])
    return data[index]


if __name__ == '__main__':

    xls = pd.read_excel("data/hw2data.xls")

    # 根据TNM分期把数据分类
    datas = []
    for i in range(4):
        datas.append(xls[xls['TNM分期'] == 'H' + str(i + 1)])
    output = pd.DataFrame()

    # 处理每个类下的数据
    for data in datas:
        data = dropNull(data)
        # data = fillNullWithMean(data)
        # data = deleteOutliers(data)
        output = output.append(data)
    output.to_excel("data/output.xls")
