import pandas as pd
import random


def writeFile(filename, lines):
    file = open(filename, 'w')
    file.writelines(lines)
    file.close()


def make_dataset(inputFile, trainFile, testFile):
    testNum = 0
    trainNum = 0

    data = pd.read_excel(inputFile)
    indexes = [i for i in data.index]

    # 打乱顺序
    random.shuffle(indexes)

    # 取前10%为测试集，其余为训练集
    testSet = indexes[:int(len(data) / 10)]
    trainSet = indexes[int(len(data) / 10) + 1:]

    data = data.replace('H1', '1').replace('H2', '2').replace('H3', '3').replace('H4', '4')

    rows = []
    for index in testSet:
        sample = [i for i in data.loc[index]]
        rows.append(sample[7] + ' ' + str(sample[0]) + ' ' + str(sample[1]) + ' ' + \
                    str(sample[2]) + ' ' + str(sample[3]) + ' ' + str(sample[4]) + '\n')
    writeFile(testFile, rows)
    testNum = len(rows)

    rows = []
    for index in trainSet:
        sample = [i for i in data.loc[index]]
        rows.append(sample[7] + ' ' + str(sample[0]) + ' ' + str(sample[1]) + ' ' + \
                    str(sample[2]) + ' ' + str(sample[3]) + ' ' + str(sample[4]) + '\n')
    writeFile(trainFile, rows)
    trainNum = len(rows)
    return trainNum, testNum
