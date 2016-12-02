import math
class Frequent_Pattern:

    def __init__(self):
        self.file_name = "data.txt"
        self.input_data_lst = []
        self.label_input_data_lst = []
        self.label_data_lst = []
        self.line_one_input_data_lst = []
        self.line_two_input_data_lst = []
        self.line_three_input_data_lst = []
        self.line_four_input_data_lst = []
        self.line_five_input_data_lst = []
        self.line_six_input_data_lst = []
        self.line_one_measure = 0
        self.line_two_measure = 0
        self.line_three_measure = 0
        self.line_four_measure = 0
        self.line_five_measure = 0
        self.line_six_measure = 0

        self.frequent_data_lst = []
        self.frequent_data_map = {}
        self.reliability = 6

    def handle_data(self, one_index, two_index, three_index, four_index, five_index, six_index):
        with open(self.file_name) as rfp:
            for line in rfp.readlines():
                data_list = line.split("\t")
                input_data = []
                for i in range(len(data_list)-1):
                    input_data.append(float(data_list[i]))
                self.input_data_lst.append(input_data)
                self.label_data_lst.append(int(data_list[-1]))
        rfp.close()

        for input_data in self.input_data_lst:
            self.line_one_input_data_lst.append(input_data[0])
            self.line_two_input_data_lst.append(input_data[1])
            self.line_three_input_data_lst.append(input_data[2])
            self.line_four_input_data_lst.append(input_data[3])
            self.line_five_input_data_lst.append(input_data[4])
            self.line_six_input_data_lst.append(input_data[5])

        self.line_one_input_data_lst = sorted(self.line_one_input_data_lst)
        self.line_two_input_data_lst= sorted(self.line_two_input_data_lst)
        self.line_three_input_data_lst= sorted(self.line_three_input_data_lst)
        self.line_four_input_data_lst=sorted(self.line_four_input_data_lst)
        self.line_five_input_data_lst=sorted(self.line_five_input_data_lst)
        self.line_six_input_data_lst= sorted(self.line_six_input_data_lst)

        self.line_one_measure = self.line_one_input_data_lst[int(len(self.line_one_input_data_lst)*one_index)]
        self.line_two_measure = self.line_two_input_data_lst[int(len(self.line_two_input_data_lst)*two_index)]
        self.line_three_measure = self.line_three_input_data_lst[int(len(self.line_three_input_data_lst)*three_index)]
        self.line_four_measure = self.line_four_input_data_lst[int(len(self.line_four_input_data_lst)*four_index)]
        self.line_five_measure = self.line_five_input_data_lst[int(len(self.line_five_input_data_lst)*five_index)]
        self.line_six_measure = self.line_six_input_data_lst[int(len(self.line_six_input_data_lst)*six_index)]

        for i in range(len(self.input_data_lst)):
            input_data = self.input_data_lst[i]
            label_input_data = []
            if input_data[0] > self.line_one_measure:
                label_input_data.append(1)
            else:
                label_input_data.append(0)
            if input_data[1] > self.line_two_measure:
                label_input_data.append(1)
            else:
                label_input_data.append(0)
            if input_data[2] > self.line_three_measure:
                label_input_data.append(1)
            else:
                label_input_data.append(0)
            if input_data[3] > self.line_four_measure:
                label_input_data.append(1)
            else:
                label_input_data.append(0)
            if input_data[4] > self.line_five_measure:
                label_input_data.append(1)
            else:
                label_input_data.append(0)
            if input_data[5] > self.line_six_measure:
                label_input_data.append(1)
            else:
                label_input_data.append(0)
            if self.label_data_lst[i] == 1:
                label_input_data.append(1)
                label_input_data.append(0)
                label_input_data.append(0)
                label_input_data.append(0)
            elif self.label_data_lst[i] == 2:
                label_input_data.append(0)
                label_input_data.append(1)
                label_input_data.append(0)
                label_input_data.append(0)
            elif self.label_data_lst[i] == 3:
                label_input_data.append(0)
                label_input_data.append(0)
                label_input_data.append(1)
                label_input_data.append(0)
            elif self.label_data_lst[i] == 4:
                label_input_data.append(0)
                label_input_data.append(0)
                label_input_data.append(0)
                label_input_data.append(1)
            self.label_input_data_lst.append(label_input_data)

    def output_data(self):
        with open("mid_result.txt","w") as wfp:
            for label_input_data in self.label_input_data_lst:
                wfp.write(str(label_input_data) + "\n")
        wfp.close()

    def get_data(self):
        with open("mid_result.txt") as rfp:
            i = 0
            for line in rfp.readlines():
                i += 1
                str_data_lst = line[1:line.find("]")].split(",")
                int_data_lst = []
                for str_data in str_data_lst:
                    int_data_lst.append(int(str_data))
                self.frequent_data_lst.append(int_data_lst)
        rfp.close()

    def pre_init_data(self):
        for i in range(pow(2,10)):
            self.frequent_data_map[i] = 0
            lst = []
            temp = i
            j = 0
            while temp > 0:
                if temp % 2 == 1:
                    lst.append(j)
                temp = int(temp / 2)
                j += 1

            for frequent_data in self.frequent_data_lst:
                flag = True
                for k in range(len(lst)):
                    num = lst[k]
                    if frequent_data[num] == 0:
                        flag = False
                        break
                if flag:
                    self.frequent_data_map[i] += 1
        self.frequent_data_map[0] = 900

        for i in range(1,pow(2,10)).__reversed__():
            for j in range(0,i).__reversed__():
                if i & j == j:
                    self.frequent_data_map[j] -= self.frequent_data_map[i]

        with open("test.txt","w") as wfp:
            for key in self.frequent_data_map.keys():
                if self.frequent_data_map[key] > self.reliability:
                    wfp.write("key = " + str(key) + "  value = " + str(self.frequent_data_map[key]) + "\n")
        wfp.close()

    def handle_frequent(self):
        one = 0
        two = 0
        three = 0
        four = 0
        frequent_set_lst = []
        diff_value_lst = [1,3,7,15,31,63,127,255,511,
                          2,6,14,30,62,126,254,510,
                          4,12,28,60,124,252,508,
                          8,24,56,120,248,504,
                          16,48,112,240,496,
                          32,96,224,480,
                          64,192,448,
                          128,384,
                          256]
        lst = [64,128,256,512]
        for i in [1,2,4,8,32]:
            for j in [64,128,256,512]:
                lst.append(i+j)
        frequent_lst = []
        for i in range(10):
            for example in lst:
                if self.frequent_data_map[example] > self.reliability:
                    frequent_lst.append(example)
            frequent_lst = sorted(list(set(frequent_lst)))
            lst = []
            for i in range(len(frequent_lst)-1):
                for j in range(len(frequent_lst)):
                    if j > i and (frequent_lst[j] - frequent_lst[i]) in diff_value_lst and self.frequent_data_map[frequent_lst[i]|frequent_lst[j]] > self.reliability:
                        flag = True
                        next_c = frequent_lst[i] | frequent_lst[j]
                        for temp_num in range(next_c - 1):
                            temp = temp_num + 1
                            if self.frequent_data_map[temp & next_c] < self.reliability:
                                flag = False
                                break
                        if flag:
                            lst.append(frequent_lst[i] | frequent_lst[j])

            for frequent_data in frequent_lst:
                frequent_set_lst.append(frequent_data)
            frequent_lst = []
            lst = sorted(list(set(lst)))

        frequent_set_lst = sorted(list(set(frequent_set_lst)))
        wfp = open("result_test_1.txt", "a")
        wfp.write("frequent_set_lst : ")
        wfp.write(str(frequent_set_lst) + "\n")
        mid_frequest_set_lst = []
        for frequent_data in frequent_set_lst:
            if frequent_data >= 64:
                mid_frequest_set_lst.append(frequent_data)
        frequent_set_lst = mid_frequest_set_lst
        mid_frequest_set_lst = []
        two_pow = [1,2,4,8,16,32]
        div_lst = [192,320,384,576,640,768]
        for i in range(len(frequent_set_lst) -1 ):
            for j in range(i+1, len(frequent_set_lst)):
                if frequent_set_lst[i] ^ frequent_set_lst[j] in div_lst:
                    mid_frequest_set_lst.append(frequent_set_lst[i])
                    mid_frequest_set_lst.append(frequent_set_lst[j])
                    break

        mid_frequest_set_lst = list(sorted(set(mid_frequest_set_lst)))
        wfp.write("mid_frequest_set_lst = ")
        wfp.write(str(mid_frequest_set_lst) + "\n")
        for frequent_data in mid_frequest_set_lst:
            frequent_set_lst.remove(frequent_data)
        wfp.write("frequent_set_lst : ")
        wfp.write(str(frequent_set_lst) + "\n")

        for frequent_data in frequent_set_lst:
            if frequent_data >= 64 and frequent_data < 128:
                one += self.frequent_data_map[frequent_data]
            elif frequent_data >= 128 and frequent_data < 256:
                two += self.frequent_data_map[frequent_data]
            elif frequent_data >= 256 and frequent_data < 512:
                three += self.frequent_data_map[frequent_data]
            elif frequent_data >= 512 and frequent_data < 1024:
                four += self.frequent_data_map[frequent_data]

        wfp.write("one = " + str(one) + "\n")
        wfp.write("two = " + str(two) + "\n")
        wfp.write("three = " + str(three) + "\n")
        wfp.write("four = " + str(four) + "\n")
        wfp.write("all = " + str(one + two + three + four) + "\n")
        wfp.close()

if __name__ == "__main__":
    fp = Frequent_Pattern()
    fp.handle_data(4/6, 3/6, 2/6, 1/6, 4/6, 5/6)
    fp.output_data()
    fp.get_data()
    fp.pre_init_data()
    fp.handle_frequent()
    """
    for one in range(1,6):
        for two in range(1,6):
            for three in range(1,6):
                for four in range(1,6):
                    for five in range(1,6):
                        for six in range(1,6):
                            fp = Frequent_Pattern()
                            fp.handle_data(one/6, two/6, three/6, four/6, five/6, six/6)
                            fp.output_data()
                            fp.get_data()
                            fp.pre_init_data()
                            fp.handle_frequent()
    """
