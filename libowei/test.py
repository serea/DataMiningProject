# coding=utf-8
from svmutil import *
from svm import *
from makedata import *
import pandas as pd


def readCsv(fileName):
    y = []
    x = []

    file = open(fileName)
    for line in file:
        list = line.split()
        y.append(int(list.pop(0)))
        x.append([float(i) for i in list])
    return y, x


def runsvm(c, g):
    params = '-c %f -g %f -q' % (c, g)
    y, x = readCsv('data/train.txt')
    prob = svm_problem(y, x)
    param = svm_parameter(params)
    m = svm_train(prob, param)
    return m


def getAccuracy(model):
    Y, X = readCsv('data/test.txt')
    pred_labels, (ACC, MSE, SCC), pred_values = svm_predict(Y, X, model)
    return ACC


def kcrossvalidation(k):
    data = pd.read_excel('data/output.xls')
    indexes = [i for i in data.index]

    # 打乱顺序
    random.shuffle(indexes)

    acc = 0.0

    # 交叉验证
    for time in range(k):

        split = time * int(len(indexes) / k)
        length = int(len(indexes) / k)
        if time == 0:
            testSet = indexes[:length]
            trainSet = indexes[length + 1:]
        else:
            testSet = indexes[split:split + length]
            trainSet = indexes[:split - 1]
            trainSet.extend(indexes[split + length + 1:])

        data = data.replace('H1', '1').replace('H2', '2').replace('H3', '3').replace('H4', '4')
        rows = []
        for index in testSet:
            sample = [i for i in data.loc[index]]
            rows.append(sample[7] + ' ' + str(sample[0]) + ' ' + str(sample[1]) + ' ' + \
                        str(sample[2]) + ' ' + str(sample[3]) + ' ' + str(sample[4]) + '\n')
        writeFile('data/test.txt', rows)
        rows = []
        for index in trainSet:
            sample = [i for i in data.loc[index]]
            rows.append(sample[7] + ' ' + str(sample[0]) + ' ' + str(sample[1]) + ' ' + \
                        str(sample[2]) + ' ' + str(sample[3]) + ' ' + str(sample[4]) + '\n')
        writeFile('data/train.txt', rows)

        acc += getAccuracy(runsvm(100, 50))
    return acc / k


def test_process():
    cList = [100]
    gList = [50]

    result = []
    for g in gList:
        for c in cList:

            acc = 0.0
            for k in range(100):
                make_dataset()
                acc += float(runsvm(c, g))
            result.append("%f,%f,%f" % (c, g, acc / 100))

    for s in result:
        print(s)


if __name__ == '__main__':
    c = 100
    g = 50
    # make_dataset()
    # model = runsvm(c, g)

    # print(getAccuracy(model))

    acc = kcrossvalidation(10)
    print(acc)
