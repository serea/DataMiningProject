import numpy
import math
import random
import json
from numpy import genfromtxt, zeros

import os

sysPath = '/'.join(os.getcwd().split('/')[:-1])+'/liuxin'

# 均值，#有字符串的情况暂时不会处理~,先这么着吧...
def mean(numbers):
    if (numbers[0] == 'H1')or(numbers[0] == 'H2')or(numbers[0] == 'H3')or(numbers[0] == 'H4'):
        return numbers[0]
    else:
        return sum(numbers) / float(len(numbers))


# 标准方差
def stdev(numbers):
    if (numbers[0] == 'H1') or (numbers[0] == 'H2') or (numbers[0] == 'H3') or (numbers[0] == 'H4'):
        return 0
    else:
        avg = mean(numbers)
        variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
        return math.sqrt(variance)


def splitDataset(dataMat, splitRatio):
    trainSize = int(len(dataMat) * splitRatio)
    trainSet = []
    copy = list(dataMat)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return [trainSet, copy]

def summarizeByClass(dataMat):
    separated = separateByClass(dataMat)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries

def summarize(dataMat):
	summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataMat)]
	del summaries[-1]
	return summaries

def separateByClass(dataMat):
    separated = {}
    for i in range(len(dataMat)):
        vector = dataMat[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated
#把高斯和这个结合起来
def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions

def predict(summaries, inputVector):
	probabilities = calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.items():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel

def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities

def calculateProbability(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
	return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent


def getAccuracy(testSet, predictions):
	correct = 0
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0



def getCoverate(testSet, trainSet,predictions):
    countH1 = 0
    LabelH1 = 0
    countH2 = 0
    LabelH2 = 0
    countH3 = 0
    LabelH3 = 0
    countH4 = 0
    LabelH4 = 0

    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            if predictions[i] == "H1":  # 计算标签数
                countH1 += 1
            elif predictions[i] == 'H2':
                countH2 += 1
            elif predictions[i] == 'H3':
                countH3 += 1
            else:
                countH4 += 1

        if testSet[i][-1] == 'H1':#计算标签数
            LabelH1+=1
        elif testSet[i][-1] == 'H2':
            LabelH2+=1
        elif testSet[i][-1] == 'H3':
            LabelH3 += 1
        else:
            LabelH4+=1
    return countH1/LabelH1*100,countH2/LabelH2*100,countH3/LabelH3*100,countH4/LabelH4*100


def main():
    freadn = sysPath+'/hw2.csv'
    fread = open(freadn, 'r')
    # 读取数据集
    dataMat = genfromtxt(freadn, delimiter=',', usecols=(0, 1, 2, 3, 4, 5))
    dataMat = dataMat.tolist()
    # 病程阶段
    target = genfromtxt(freadn, delimiter=',', usecols=(6), dtype=str)
    target = target.tolist()
#因numpy的arraynd不能容纳不同类型的数据故转换成list进行拼接
    fread.close()

#list拼接
    count = 0
    while count < len(dataMat):
        dataMat[count].append(target[count])
        count = count+1
    splitRatio = 0.1 #训练集和测试集的比例
    trainingSet, testSet = splitDataset(dataMat, splitRatio)

    # prepare model
    summaries = summarizeByClass(trainingSet)
    # test model
    predictions = getPredictions(summaries, testSet)
    accuracy = getAccuracy(testSet, predictions)
    coverH1,coverH2,coverH3,coverH4 = getCoverate(testSet,trainingSet,predictions)

    # print(accuracy)
    # print(coverH1)
    # print(coverH2)
    # print(coverH3)
    # print(coverH4)

    return accuracy,coverH1,coverH2,coverH3,coverH4

def getJsonResult():
    accuracy, coverH1, coverH2, coverH3, coverH4 = main()
    return json.dumps({
        "correctRate": "%2.3f%%" % ( accuracy),
        "coverRateH1": "%2.3f%%" % (coverH1),
        "coverRateH2": "%2.3f%%" % (coverH2),
        "coverRateH3": "%2.3f%%" % (coverH3),
        "coverRateH4": "%2.3f%%" % (coverH4),
    })

main()

