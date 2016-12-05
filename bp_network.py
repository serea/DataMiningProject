import math
import random

input_dim = 6
mid_dim = 8
output_dim = 4
data_size = 900
train_data_size = 700
predict_data_size = 200
data_file = "data.txt"
xite = 0.2

class BpNN:

    def __init__(self):
        self.input = []
        self.output = []
        self.times = 100
        self.mid_data = [[0] * mid_dim]
        self.output_data = [[0] * output_dim]
        self.train_list = random.sample(range(0,data_size),train_data_size)
        self.predict_data = []
        with open(data_file) as rfp:
            lines = []
            lines = rfp.readlines()
            for i in range(data_size):
                line = lines[i]
                if i in self.train_list:
                    self.input.append(line.split("\t")[:-1])

                    if line.split("\t")[-1][0] == "1":
                        self.output.append([1,0,0,0])
                    elif line.split("\t")[-1][0] == "2":
                        self.output.append([0, 0, 1, 0])
                    elif line.split("\t")[-1][0] == "3":
                        self.output.append([0, 0, 1, 0])
                    elif line.split("\t")[-1][0] == "4":
                        self.output.append([0, 0, 0, 1])
                    else:
                        print(len(line.split("\t")[-1]))
                else:
                    self.predict_data.append(line)
        rfp.close()

        self.mid_w1 = [[0] * input_dim] * mid_dim
        self.mid_b1 = [[0] * mid_dim]
        self.mid_w2 = [[0] * mid_dim] * output_dim
        self.mid_b2 = [[0] * output_dim]

    def __train__(self):

        print("Begin to train BP Network!")
        wfp = open("log.txt","w")
        for ii in range(self.times):
            ERROR = 0
            for jj in range(train_data_size):
                # 隐含层输出
                for i in range(mid_dim):
                    self.mid_data[0][i] = 0
                    for j in range(input_dim):
                        self.mid_data[0][i] += self.mid_w1[i][j] * float(self.input[jj][j])
                    self.mid_data[0][i] += self.mid_b1[0][i]
                    self.mid_data[0][i] = 1 / (1 + math.exp(- self.mid_data[0][i]))

                # 输出层输出
                for i in range(output_dim):
                    self.output_data[0][i] = 0
                    for j in range(mid_dim):
                        self.output_data[0][i] += self.mid_w2[i][j] * self.mid_data[0][j]
                    self.output_data[0][i] += self.mid_b2[0][i]
                error = [[0] * output_dim]
                for i in range(output_dim):
                    error[0][i] = self.output[jj][i] - self.output_data[0][i]
                    ERROR += abs(error[0][i])

                dw2 = [[0] * mid_dim] * output_dim
                db2 = [[0] * output_dim]
                for i in range(output_dim):
                    for j in range(mid_dim):
                        dw2[i][j] = error[0][i] * self.mid_data[0][j]
                    db2[0][i] = error[0][i]

                dw1 = [[0] * input_dim] * mid_dim
                db1 = [[0] * mid_dim]
                for i in range(input_dim):
                    for j in range(mid_dim):
                        dw1[j][i] = self.mid_data[0][j] * (1 - self.mid_data[0][j]) * float(self.input[0][i]) * (error[0][0] * self.mid_w2[0][j] + error[0][1] * self.mid_w2[1][j] + error[0][2] * self.mid_w2[2][j] + error[0][3] * self.mid_w2[3][j])
                        db1[0][j] = self.mid_data[0][j] * (1 - self.mid_data[0][j])  * (error[0][0] * self.mid_w2[0][j] + error[0][1] * self.mid_w2[1][j] + error[0][2] * self.mid_w2[2][j] + error[0][3] * self.mid_w2[3][j])

                for i in range(input_dim):
                    for j in range(mid_dim):
                        self.mid_w1[j][i] += xite * dw1[j][i]
                    self.mid_b1[0][i] += xite * db1[0][i]

                for i in range(output_dim):
                    for j in range(mid_dim):
                        self.mid_w2[i][j] += xite * dw2[i][j]
                    self.mid_b2[0][i] += xite * db2[0][i]
            wfp.write("ERROR == ", )
            wfp.write(str(ERROR) + "\n")

    def __predict__(self):
        count = 0
        wfp = open("result.txt","w")
        for raw_data in self.predict_data:
            data = raw_data.split("\t")[:-1]
            result = raw_data.split("\t")[-1]
            # 隐含层输出
            for i in range(mid_dim):
                self.mid_data[0][i] = 0
                for j in range(input_dim):
                    self.mid_data[0][i] += self.mid_w1[i][j] * float(data[j])
                self.mid_data[0][i] += self.mid_b1[0][i]
                self.mid_data[0][i] = 1 / (1 + math.exp(- self.mid_data[0][i]))

            # 输出层输出
            for i in range(output_dim):
                self.output_data[0][i] = 0
                for j in range(mid_dim):
                    self.output_data[0][i] += self.mid_w2[i][j] * self.mid_data[0][j]
                self.output_data[0][i] += self.mid_b2[0][i]
            wfp.write(str(raw_data) + "\n")
            wfp.write(str(self.output_data[0]) + "\n")
            num = []
            for output_data in self.output_data[0]:
                num.append(float(output_data))
            if (int(result) == num.index(max(num)) + 1):
                count += 1
        print(count)
        wfp.close()

if __name__ == "__main__":
    bpnn = BpNN()
    bpnn.__train__()
    bpnn.__predict__()