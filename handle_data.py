import xlrd

def hanlde_data():
    data = xlrd.open_workbook("hw2data.xls")
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    with open("aa.txt", "w") as wfp:
        for row in range(nrows-1):
            flag = True
            linestr = ""
            for col in range(6):
                if str(table.cell(row + 1, col).value) == "":
                    flag = False
                    break
                else:
                    linestr += str(table.cell(row + 1, col).value) + "\t"
            if flag:
                if str(table.cell(row + 1, 7).value) == "":
                    continue
                else:
                    if row == nrows - 2:
                        linestr += str(table.cell(row + 1, 7).value)[-1]
                    else:
                        linestr += str(table.cell(row + 1, 7).value)[-1] + "\n"
                    wfp.write(linestr)

if __name__ == "__main__":
    hanlde_data()