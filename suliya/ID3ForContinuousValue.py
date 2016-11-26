# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 11:44:31 2016

@author: Serea
"""

import operator
import json
from math import log
import math
import time
import csv
from sklearn import tree
import random

import os

sysPath = '/'.join(os.getcwd().split('/')[:-1])+'/suliya'

path = sysPath + '/continuousdata.csv'

#读取csv数据，存放到dataset，单独把标签提出来
def createDataSet(path):
    dataSet = []
    with open(path) as f:
        f_csv = csv.reader(f)
        labels = []
        labels = next(f_csv)   
        for row in f_csv:
            dataSet.append(row)
    return dataSet,labels

#计算数据集中的香农熵，看数据的标签分布    
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

#找到最大熵增益的特征及特征取值    
def chooseBestFeatureAndValueToSplit(dataSet,labels):
    numFeatures = len(dataSet[0]) - 1 #最后一项是标签
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in (range(numFeatures)):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        #featList得到所有的feature值
        uniqueVals=sorted(uniqueVals)
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
        
        
#创建决策树，使用熵增益评判
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]#从后往前赋值
    #取最后一列的所有值
    if classList.count(classList[0])==len(classList):
        #统计与classlist【0】相同的项的个数
        #类别相同停止划分
        return classList[0]
    if len(dataSet[0])==1:
        #所有特征用完，数据只有标签列
        return majorityCnt(classList)
    (bestFeat,featValue) = chooseBestFeatureAndValueToSplit(dataSet,labels)
    #print(bestFeat,featValue,labels[bestFeat])
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    subLabels = labels[:]
    del(subLabels[bestFeat])
    myTree[bestFeatLabel][featValue] = createTree(splitDataSet(dataSet,bestFeat,featValue),subLabels)
    subLabels = labels[:]
    del(subLabels[bestFeat])
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
            if index[-2:]=='系数':
                for i in value.keys():
                    if i[-5:]=='false':
                        num = i
                num = num[0:-5]
                for j in range(len(label)):
                    if label[j]==index:  
                        point = j
                if row[point]>num:
                    result = Test(value[num+'false'],row,label)
                    return result      
                else:
                    result = Test(value[num],row,label)
                    return result
            else:
                result = Test(value,row,label)
                return result
                
    else:
        result = myTree
        return result

#求正确率
def FindAccuracy(datatest,trainnum,testnum,myTree,label,tolflag):
    rightnum=0
    wrongnum=0
    rightflag={}
    for item in datatest:
        resultFromTree = Test(myTree,item,label)
        if item[-1]==resultFromTree:
            rightnum += 1
            if item[-1] not in rightflag.keys():
                rightflag[item[-1]]=0
            rightflag[item[-1]] += 1
        else:
            wrongnum += 1
    print("rightnum:",rightnum)
    print("wrongnum:",wrongnum)
    for (key,item) in tolflag.items():
        if key in rightflag:
            rightflag[key] = rightflag[key]/float(tolflag[key])
        else:
            rightflag[key] = 0 

    return rightnum/len(datatest),rightflag       

#统计测试数据每种标签数
def staflag(datatest,testnum):
    flag = {}
    for item in datatest:
        if item[-1] not in flag.keys():
            flag[item[-1]]=0
        flag[item[-1]] += 1
    for (k,f) in flag.items():
        f = f/testnum
    return flag
  
#main()
def main():
    data,label = createDataSet(path)
    '''
    print(label)
    myTree = createTree(data,label)
    print(label)
    result = Test(myTree,data[0],label)
    print(myTree)
    print(result)
    '''
    tolaccu=0
    tolcover={'H1':0,'H2':0,'H3':0,'H4':0}
    lengthOfData=len(data)
    random.shuffle(data)
    split=math.floor(len(data)/10)

    for time in range(10):
        datatrain=[]
        datatest=[]
        for i in range(lengthOfData):
            if i > split*(time) and i < split*(time+1)-1:
                datatest.append(data[i])
            else:
                datatrain.append(data[i])
        trainnum=len(datatrain)
        testnum=len(datatest)
        print("test for",time+1,":")
        print("trainnum:",trainnum)
        print("testnum:",testnum)
        myTree = createTree(datatrain,label)
        #print(myTree)
        tolflag = staflag(datatest,testnum)
        (accuracy,cover) = FindAccuracy(datatest,trainnum,testnum,myTree,label,tolflag)
        print("accuracy:",accuracy)
        print("cover:",cover)
        tolaccu=tolaccu+accuracy
        for (key,value) in tolcover.items():
            tolcover[key]=tolcover[key]+cover[key]
    tolaccu = tolaccu/10
    for (key,value) in tolcover.items():
        tolcover[key]=tolcover[key]/10
    return tolaccu,tolcover
    print("average accuracy:",tolaccu)
    print("average cover:",tolcover)       



def getJsonResult():
    totalRate, totalClassCoverRate = main()
    return json.dumps({
        "correctRate": "%2.3f%%" % (( totalRate) * 100),
        "coverRateH1": "%2.3f%%" % (totalClassCoverRate['H1']* 100),
        "coverRateH2": "%2.3f%%" % (totalClassCoverRate['H2']* 100),
        "coverRateH3": "%2.3f%%" % (totalClassCoverRate['H3']* 100),
        "coverRateH4": "%2.3f%%" % (totalClassCoverRate['H4']* 100)
    })


if __name__=='__main__':
    # main()
    print(getJsonResult())