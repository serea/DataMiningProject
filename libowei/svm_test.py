# coding=utf-8
from libowei.svmutil import *
from libowei.svm import *
from libowei.makedata import *
import pandas as pd
import json


def makedata(inputFile, trainFile, testFile):
    return make_dataset(inputFile, trainFile, testFile)


def readCsv(fileName):
    y = []
    x = []
    file = open(fileName)
    for line in file:
        list = line.split()
        y.append(int(list.pop(0)))
        x.append([float(i) for i in list])
    return y, x


def runsvm(c, g, trainData):
    params = '-c %f -g %f -q' % (c, g)
    y, x = readCsv(trainData)
    print(y, x)
    prob = svm_problem(y, x)
    param = svm_parameter(params)
    m = svm_train(prob, param)
    return m


def getAccuracy(model, testFile):
    Y, X = readCsv(testFile)
    pred_labels, (ACC, MSE, SCC), pred_values = svm_predict(Y, X, model)

    # 覆盖率
    cover = [[0, 0], [0, 0], [0, 0], [0, 0]]

    for i in range(len(Y)):
        index = Y[i] - 1
        cover[index][1] += 1
        # 预测正确
        if int(pred_labels[i]) == Y[i]:
            cover[index][0] += 1
    print(cover)
    jsonDic = {}
    labels = ['H1', 'H2', 'H3', 'H4']
    for i in range(4):
        jsonDic[labels[i]] = cover[i]
    jsonDic['acc'] = ACC
    return json.dumps(jsonDic)


# 保存训练的模型
def saveModel(modelFile, model):
    return svm_save_model(modelFile, model)


def loadModel(modelFile):
    return svm_load_model(modelFile)


if __name__ == '__main__':
    model = loadModel('../libowei/model.txt')
    json = getAccuracy(model, '../libowei/test.txt')
    print(json)
