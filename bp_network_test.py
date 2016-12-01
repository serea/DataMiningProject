import math
import random

class BP_Net:

    def __init__(self):
        self.input_dim = 6
        self.mid_dim = 5
        self.output_dim = 4

        self.data_file = "data.txt"
        self.data_size = 900
        self.train_data_size = 700
        self.predict_data_size = 200

        self.train_list = random.sample(range(0, self.data_size), self.train_data_size)
        self.input_train_data = [[0] * self.input_dim] * self.train_data_size
        self.output_train_data = [[0] * self.output_dim] * self.train_data_size
        self.input_predict_data = [[0] * self.input_dim] * self.predict_data_size
        self.output_predict_data = [[0] * self.predict_data_size]

        self.mid_train_data_result = [[0] * self.mid_dim]
        self.output_train_data_result = [[0] * self.output_dim]
        self.mid_train_w1 = [[0] * self.mid_dim] * self.input_dim
        self.mid_train_b1 = [[0] * self.mid_dim] * self.input_dim
        self.mid_train_w2 = [[0] * self.output_dim] * self.mid_dim
        self.mid_train_b2 = [[0] * self.output_dim] * self.mid_dim
        self.output_train_error = [[0] * self.output_dim]
        self.mid_train_error = [[0] * self.mid_dim]
        self.xite = 0.5

        self.mid_predict_data_result = [[0] * self.mid_dim]
        self.output_predict_data_result = [[0] * self.output_dim]

        self.times = 1000

    def input_data(self):
        with open(self.data_file) as rfp:
            train_line = 0
            predict_line = 0
            for line_index in range(self.data_size):
                line = rfp.readline()[:-1]
                if line_index in self.train_list:
                    train_lst = line.split("\t")
                    for input_index in range(self.input_dim):
                        self.input_train_data[train_line][input_index] = float(train_lst[input_index])
                    self.output_train_data[train_line][int(train_lst[-1]) - 1] = 1
                    train_line += 1
                else:
                    predict_lst = line.split("\t")
                    for input_index in range(self.input_dim):
                        self.input_predict_data[predict_line][input_index] = float(predict_lst[input_index])
                    self.output_predict_data[0][predict_line] = int(predict_lst[-1])
                    predict_line += 1

    def train(self):
        for time in range(self.times):
            for train_index in range(self.train_data_size):
                #隐藏层输出
                for mid_index in range(self.mid_dim):
                    self.mid_train_data_result[0][mid_index] = 0
                    for input_index in range(self.input_dim):
                        self.mid_train_data_result[0][mid_index] += self.mid_train_w1[input_index][mid_index] * self.input_train_data[train_index][input_index]
                    self.mid_train_data_result[0][mid_index] += self.mid_train_b1[0][mid_index]
                    self.mid_train_data_result[0][mid_index] = 1 / (1 + math.exp(self.mid_train_data_result[0][mid_index]))

                #输出层输出
                for output_index in range(self.output_dim):
                    self.output_train_data_result[0][output_index] = 0
                    for mid_index in range(self.mid_dim):
                        self.output_train_data_result[0][output_index] += self.mid_train_w2[mid_index][output_index] * self.mid_train_data_result[0][mid_index]
                    self.output_train_data_result[0][output_index] += self.mid_train_b2[0][output_index]
                    self.output_train_data_result[0][output_index] = 1 / (1 + math.exp(self.output_train_data_result[0][output_index]))

                #计算输出层ERROR
                for output_index in range(self.output_dim):
                    self.output_train_error[0][output_index] = self.output_train_data_result[0][output_index] * (1 - self.output_train_data_result[0][output_index]) * (self.output_train_data[train_index][output_index] - self.output_train_data_result[0][output_index])

                #计算隐藏层ERROR
                for mid_index in range(self.mid_dim):
                    derror = 0
                    for output_index in range(self.output_dim):
                        derror += self.output_train_error[0][output_index] * self.mid_train_w2[mid_index][output_index]
                    self.mid_train_error[0][mid_index] = self.mid_train_data_result[0][mid_index] * (1 - self.mid_train_data_result[0][mid_index]) * derror

                #修正隐藏层参数
                for mid_index in range(self.mid_dim):
                    for output_index in range(self.output_dim):
                        self.mid_train_w2[mid_index][output_index] += self.xite * self.output_train_error[0][output_index] * self.mid_train_data_result[0][mid_index]
                for output_index in range(self.output_dim):
                    self.mid_train_b2[0][output_index] += self.xite * self.output_train_error[0][output_index]

                #修正输入层参数
                for input_index in range(self.input_dim):
                    for mid_index in range(self.mid_dim):
                        self.mid_train_w1[input_index][mid_index] += self.xite * self.mid_train_error[0][mid_index] * self.input_train_data[train_index][input_index]
                for mid_index in range(self.mid_dim):
                    self.mid_train_b1[0][mid_index] += self.xite * self.mid_train_error[0][mid_index]
    def predict(self):
        count = 0
        for predict_index in range(self.predict_data_size):
            #隐藏层输出
            for mid_index in range(self.mid_dim):
                self.mid_predict_data_result[0][mid_index] = 0
                for input_index in range(self.input_dim):
                    self.mid_predict_data_result[0][mid_index] += self.mid_train_w1[input_index][mid_index] * self.input_predict_data[predict_index][input_index]
                self.mid_predict_data_result[0][mid_index] += self.mid_train_b1[0][mid_index]
                self.mid_predict_data_result[0][mid_index] = 1 / (1 + math.exp(self.mid_predict_data_result[0][mid_index]))

            # 输出层输出
            for output_index in range(self.output_dim):
                self.output_predict_data_result[0][output_index] = 0
                for mid_index in range(self.mid_dim):
                    self.output_predict_data_result[0][output_index] += self.mid_train_w2[mid_index][output_index] * self.mid_predict_data_result[0][mid_index]
                self.output_predict_data_result[0][output_index] += self.mid_train_b2[0][output_index]
                self.output_predict_data_result[0][output_index] = 1 / (1 + math.exp(self.output_predict_data_result[0][output_index]))

            if self.output_predict_data_result[0].index(max(self.output_predict_data_result[0])) == self.output_predict_data[0][predict_index] - 1:
                count += 1
        print(count)
def main():
    bpn = BP_Net()
    print("read start")
    bpn.input_data()
    print("read ok")
    print("train start")
    bpn.train()
    print("train ok")
    print("predict start")
    bpn.predict()
    print("predict ok")
if __name__ == "__main__":
    if __name__ == '__main__':
        main()