# encoding: utf-8

from numpy import *
import operator
import random
import os

Path = '/'.join(os.getcwd().split('/')[:-1])+'/zanwen'
rawDataPath = Path + '/data/rawdata.csv'
cleanDataPath = Path + '/data/cleandata.csv'

labelsDict = {'H1': 0, 'H2': 1, 'H3': 2, 'H4': 3}
# 预处理
def preproces():
    outstream = ""
    dataSet = []
    sample = []
    with open(rawDataPath, 'r') as f:
        f.readline()
        for line in f.readlines():
            line = line.split(',')
            sample = line[:6]
            sample.append(line[7])
            if "" not in sample:
                # sample[6] = TNMDict[sample[6]]
                dataSet.append(sample)

    for sample in dataSet:
        for x in sample:
            outstream += x + ','
        outstream = outstream.strip(',') + '\n'

    with open(cleanDataPath, 'w') as f:
        f.write(outstream)

# 交叉验证法，第i份化入测试集，其他九分化为训练集
def divDataSet( i):
    trainData = {"group":[],"labels":[]}
    testData = {"group":[],"labels":[]}
    group,labels = createDataSet(cleanDataPath)
    # 随机划分
    dataSetIndicies = list(range(len(group)))
    random.shuffle(dataSetIndicies)

    if i >= 0 and i < 10:
        trainDataIndex = dataSetIndicies[:len(group) // 10 * i]
        trainDataIndex.extend(dataSetIndicies[len(group) // 10 * (i+1):])
        testDataIndex = dataSetIndicies[len(group) // 10 * i:len(group) // 10 * (i+1)]

        for index in trainDataIndex:
            trainData["group"].append(group[index])
            trainData["labels"].append(labels[index])
        trainData["group"] = array(trainData["group"])

        for index in testDataIndex:
            testData["group"].append(group[index])
            testData["labels"].append(labels[index])
        testData["group"] = array(testData["group"])
    else:
        print("Num should be a int in 0..9")

    return trainData,testData

def createDataSet(dataPath):
    group = []
    labels = []
    with open(dataPath,'r') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            groupItem = list(map(float, line[:-1]))
            group.append(groupItem)
            labels.append(line[-1])
    dataSet = array(group)
    return dataSet, labels

# 计算两个向量的lp范数
def getLpDistances(lp, inX, dataSet):
    if not isinstance(lp, int):
        raise TypeError("lp must be a integer.")
    dataSetSize = dataSet.shape[0]

    diffMat = absolute(tile(inX, (dataSetSize, 1)) - dataSet)

    lpDiffMat = diffMat ** lp
    lpDistances = lpDiffMat.sum(axis = 1)
    distances = lpDistances ** (1.0/lp)
    return distances

def classify(inX, dataSet, labels, k, lp):
    Distances = getLpDistances(lp,inX,dataSet)
    sortedDistIndicies = Distances.argsort()
    classCount = {}

    for i in range(k):
        voteLabel = labels[sortedDistIndicies[i]]
        classCount[voteLabel] = classCount.get(voteLabel,0) + 1
    sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

def dataClassTest(k, lp,i):
    trainData, testData = divDataSet(i)

    trainSet = trainData["group"]
    trainLabels = trainData["labels"]
    testSet = testData["group"]
    testLabels = testData["labels"]

    testSetSize = testSet.shape[0]
    errorCount = 0
    testCount = 0


    labelsCount = array([0,0,0,0])
    classCoverCount = array([0,0,0,0])
    for inX in testSet:
        classifierResult = classify(inX, trainSet, trainLabels, k, lp)
        labelsCount[labelsDict[trainLabels[testCount]]] += 1
        if classifierResult == testLabels[testCount]:
            classCoverCount[labelsDict[trainLabels[testCount]]] += 1
            # print("[Correct Classification] the classifier came back with : %s, the real answer is: %s"\
            #       % (classifierResult,testLabels[testCount]))
        else:
            errorCount += 1
            # print("[Wrong Classification] the classifier came back with : %s, the real answer is: %s" \
            #       % (classifierResult, testLabels[testCount]))
        testCount += 1
    # print("[testNum: %d, k: %d, lp: %d] The error rate is :%.3f%%" %(testNum,k,lp,errorCount/float(testSetSize)*100))
    errorRate = errorCount/float(testSetSize)
    classCoverRate = classCoverCount/labelsCount
    return errorRate,classCoverRate

def crossValidation(k, lp):
    totalRate = 0.0
    totalClassCoverRate = 0
    for i in range(10):
        errorRate, classCoverRate = dataClassTest( k, lp, i)
        totalRate += errorRate
        totalClassCoverRate += classCoverRate
    totalRate /= 10
    totalClassCoverRate /= 10
    return totalRate,totalClassCoverRate

def findBestArgs( maxK, maxLp):
    minRecord = {"k":None,"lp":None,"minErrorRate":1}   # 记录最小错误率以及对应的k,lp
    for k in range(1,maxK+1):
        for lp in range(1,maxLp+1):
            totalRate,totalClassCoverRate= crossValidation(k, lp)
            print("totalRate: %f%%, k: %d, lp: %d" %(totalRate*100,k,lp))
            if totalRate < minRecord["minErrorRate"]:
                minRecord['k'] = k;
                minRecord['lp'] = lp;
                minRecord['minErrorRate'] = totalRate;
    return minRecord


def hello():
    return  "hello"


if __name__ == "__main__":

    # testNum=100
    # maxK= 5
    # maxLp= 5
    # minRecord = findBestArgs(cleanDataPath, maxK, maxLp)
    # print("Minimal error rate: %f%%, when k: %d, lp: %d"%(minRecord['minErrorRate']*100,minRecord['k'], minRecord['lp']))

    totalRate, totalClassCoverRate = crossValidation(2,3)
    print( totalRate, totalClassCoverRate)
