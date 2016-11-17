# encoding: utf-8

from numpy import *
import operator
import random

# 预处理
def preproces(rawDataPath, cleanDataPath):
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

# 把预处理过的数据按9:1的比例随机分为训练集和测试集
def divDataSet(cleanDataPath, trainDataPath, testDataPath):
    with open(cleanDataPath,'r') as f:
        lines = f.readlines()

    random.shuffle(lines)
    trainData = lines[len(lines)/10:]
    testData = lines[:len(lines)/10]

    with open(trainDataPath,'w') as f:
        f.writelines(trainData)
    with open(testDataPath,'w') as f:
        f.writelines(testData)

def createDataSet(dataPath):
    group = []
    labels = []
    with open(dataPath,'r') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            groupItem = map(float, line[:-1])
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
    sortedDistIndicies = getLpDistances(lp,inX,dataSet).argsort()
    classCount = {}
    for i in range(k):
        voteLabel = labels[sortedDistIndicies[i]]
        classCount[voteLabel] = classCount.get(voteLabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

def dataClassTest(trainDataPath, testDataPath, k, lp,testNum):
    trainSet, trainLabels = createDataSet(trainDataPath)
    testSet, testLabels = createDataSet(testDataPath)

    testSetSize = testSet.shape[0]
    errorCount = 0
    testCount = 0

    for inX in testSet:
        classifierResult = classify(inX, trainSet, trainLabels, k, lp)
        if classifierResult == testLabels[testCount]:
            pass
            # print "[Correct Classification] the classifier came back with : %s, the real answer is: %s"\
            #       % (classifierResult,testLabels[testNum])
        else:
            errorCount += 1
            # print "[Wrong Classification] the classifier came back with : %s, the real answer is: %s" \
            #       % (classifierResult, testLabels[testNum])
        testCount += 1
    print "[testNum: %d, k: %d, lp: %d] The error rate is :%.3f%%" %(testNum,k,lp,errorCount/float(testSetSize)*100)
    return errorCount/float(testSetSize)

def findBestArgs(cleanDataPath,trainDataPath,testDataPath, testNum, maxK, maxLp):
    minRecord = {"k":None,"lp":None,"minErrorRate":1}   # 记录最小错误率以及对应的k,lp
    for k in range(1,maxK+1):
        for lp in range(1,maxLp+1):
            totalRate = 0.0
            for testNum in range(testNum):
                divDataSet(cleanDataPath, trainDataPath, testDataPath)
                totalRate += dataClassTest(trainDataPath, testDataPath, k, lp,testNum)
            totalRate /= testNum
            print("totalRate: %f%%, k: %d, lp: %d" %(totalRate*100,k,lp))
            if totalRate < minRecord["minErrorRate"]:
                minRecord['k'] = k;
                minRecord['lp'] = lp;
                minRecord['minErrorRate'] = totalRate;
    return minRecord


if __name__ == "__main__":
    rawDataPath = unicode("C:/Users/Mr.x/repos/DataMiningProject/zanwen/data/rawdata.csv",'utf-8')
    cleanDataPath = unicode("C:/Users/Mr.x/repos/DataMiningProject/zanwen/data/cleandata.csv",'utf-8')
    trainDataPath = unicode("C:/Users/Mr.x/repos/DataMiningProject/zanwen/data/traindata.csv",'utf-8')
    testDataPath = unicode("C:/Users/Mr.x/repos/DataMiningProject/zanwen/data/testdata.csv",'utf-8')

    testNum=1000
    maxK= 1
    maxLp= 3
    minRecord = findBestArgs(cleanDataPath,trainDataPath,testDataPath, testNum, maxK, maxLp)
    print "Minimal error rate: %f%%, when k: %d, lp: %d"%(minRecord['minErrorRate']*100,minRecord['k'], minRecord['lp'])
