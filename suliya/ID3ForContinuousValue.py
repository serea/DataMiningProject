# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:44:31 2016

@author: Serea
"""

import operator
from math import log
import math
import time
import csv
from sklearn import tree

path = './continuousdata.csv'


def createDataSet(path):
    dataSet = []
    with open(path) as f:
        f_csv = csv.reader(f)
        labels = []
        labels = next(f_csv)   
        for row in f_csv:
            dataSet.append(row)
    return dataSet,labels

    
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for feaVec in dataSet:
        currentLabel = feaVec[-1]
        #取的最后的分类结果，根据这个算
        if currentLabel not in labelCounts:
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

#将数据按照特征分为小于等于value的部分
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] <= value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            #把数据中该项的特征去掉
            retDataSet.append(reducedFeatVec)
    return retDataSet   

#将数据按照特征分为大于value的部分
def splitDataSetFalse(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] > value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            #把数据中该项的特征去掉
            retDataSet.append(reducedFeatVec)
    return retDataSet 

#选出最后数据集中的大多数标签
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote] += 1
    return max(classCount)
    
def chooseBestFeatureAndValueToSplit(dataSet,labels):
    numFeatures = len(dataSet[0]) - 1 #最后一项是标签
    #print(dataSet[0])
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    #print("numFeatures:")
    #print(numFeatures)
    for i in (range(numFeatures)):
        #print(labels[i])
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        #featList得到所有的feature值
        uniqueVals=sorted(uniqueVals)
        #print("uniqueVals：" )
        #print(uniqueVals)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            subDataSet2 = splitDataSetFalse(dataSet,i,value)
            prob = len(subDataSet) / float(len(dataSet))
            prob2 = 1-prob
            newEntropy = prob * calcShannonEnt(subDataSet) + prob2 * calcShannonEnt(subDataSet2)
            infoGain=baseEntropy-newEntropy
            if infoGain > bestInfoGain:
                bestInfoGain = infoGain
                bestFeature = i
                bestFeatureValue=value
    return (bestFeature,bestFeatureValue)
        
        

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]#从后往前赋值
    #取最后一列的所有值
    if classList.count(classList[0])==len(classList):
        #统计与classlist【0】相同的项的个数
        #类别相同停止划分
        #print(labels)
        #print("stop for same class")
        return classList[0]
    if len(dataSet[0])==1:
        #所有特征用完
        #print(labels)
        #print("stop for no feature")
        return majorityCnt(classList)
    #print(dataSet[0])
    (bestFeat,featValue) = chooseBestFeatureAndValueToSplit(dataSet,labels)
    print(bestFeat,featValue,labels[bestFeat])
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    #print(labels)
    del(labels[bestFeat])
    #featValues = [example[bestFeat] for example in dataSet]#bestFeat 有哪些值
    #uniqueVals = set(featValues)
    #for value in uniqueVals:
    subLabels = labels[:]
    myTree[bestFeatLabel][featValue] = createTree(splitDataSet(dataSet,bestFeat,featValue),subLabels)
    subLabels = labels[:]
    myTree[bestFeatLabel][featValue+'false'] = createTree(splitDataSetFalse(dataSet,bestFeat,featValue),subLabels)
    return myTree


#打印文本形式的tree，还未写完
def PrintTree(tree,index):
    for (item,value) in tree.items():
        if type(value)!=dict:
            #print("not dict")
            print(index + item + ':' + value)
        else:
            index = item
            PrintTree(value,index)

#对数据带入树中求标签
def Test(myTree,row,label):
    flag = ['H1','H2','H3','H4']
    if type(myTree)==dict:
        for (index,value) in myTree.items():
            for i in value.keys():
                if i[-5:]=='false':
                    num = i
            num = num[0:-5]
            for j,k in enumerate(label):
                if k==index:
                    point = j
            if row[j]>num:
                result = Test(value[num+'false'],row,label)
                return result      
            else:
                result = Test(value[num],row,label)
                return result 
    else:
        result = myTree
        return result

#求正确率
def FindAccuracy(datatest,trainnum,testnum,myTree,label):
    rightnum=0
    wrongnum=0
    for item in datatest:
        resultFromTree = Test(myTree,item,label)
        print(resultFromTree)
        print("rightresult:")
        print(item[-1])
        if item[-1]==resultFromTree:
            rightnum += 1
        else:
            wrongnum += 1
    print(rightnum,wrongnum)
    return rightnum/len(datatest)        

#将数据集分为训练和测试集
def Divide(dataSet):
    length = len(dataSet)
    lenOfTrain = math.floor(9/10*length)
    lenOfTest = length-lenOfTrain
    datatrain=dataSet[-lenOfTrain:]
    datatest = dataSet[0:-lenOfTrain]
    #datatrain=dataSet[0:lenOfTrain]
    #datatest = dataSet[lenOfTrain+1:]
    return datatrain,datatest,lenOfTrain,lenOfTest
    

def main():
    data,label = createDataSet(path)
    #print(data)
    #print("label:")
    #print(label)
    (datatrain,datatest,trainnum,testnum) = Divide(data)
    print(trainnum,testnum)
    print(len(datatrain),len(datatest))
    myTree = createTree(datatrain,label)
    #print(myTree)
    accuracy = FindAccuracy(datatest,trainnum,testnum,myTree,label)
    print("accuracy")
    print(accuracy)
    
    #PrintTree(myTree,'ROOT')
       

if __name__=='__main__':
    main()
    