import xlrd

def handle_data():
    data = xlrd.open_workbook("hw2data.xls")
    table = data.sheet_by_index(0)
    nrows = table.nrows
    nlst = []
    nFlag = True
    with open("aa.txt", "w") as wfp:
        for i in range(nrows-1):
            nlst = []
            nFlag = True
            for j in range(6):
                if len(str(table.cell(i+1, j).value)) != 0:
                    nlst.append(table.cell(i+1, j).value)
                else:
                    nFlag = False
                    break
            if nFlag:
                if len(str(table.cell(i+1,7).value)) != 0:
                    nlst.append(str(table.cell(i+1,7).value)[1])
                    for data in nlst:
                        wfp.write(str(data))
                        wfp.write("\t")
                    wfp.write("\n")
            else:
                continue
if __name__ == "__main__":
    handle_data()