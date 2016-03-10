#coding=utf-8
import re
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LoadData:

    def __init__(self, matrixfile, labelfile=None):
        self.matrix = self.Data2Matrix(matrixfile)
        self.label = None
        if labelfile is not None:
            self.label = self.DataIsLabel(labelfile)

    @staticmethod
    def Data2Matrix(filename):
        if re.match('(.*xls)|(.*txt)', filename):
            matrix = LoadData.DataIsxls(filename)
            return matrix
        if re.match('.*csv', filename):
            matrix = LoadData.DataIscsv(filename)
            return matrix
        
    @staticmethod
    def DataIscsv(filename):
        file_object = open(filename)
        max1 = -1
        max2 = -1
        line = file_object.readline()
        matrix = [[0 for col in range(5000)]for row in range(5000)]
        tag = re.match('\d.*', line)
        if not tag:
            line = file_object.readline()
        while line:
            m = re.match('\d.*,\d.*,\d.*', line)
            if m:
                temp = m.group().strip().split(',')
                matrix[int(temp[0])][int(temp[1])] = int(temp[2])
                max1 = max(max1, int(temp[0]))
                max2 = max(max2, int(temp[1]))
            line = file_object.readline()
        max1 = max(max1, max2)+1
        file_object.close()
        newMatrix = [[0 for col in range(max1)]for row in range(max1)]
        for i in range(0, max1, 1):
            for j in range(0, max1, 1):
                newMatrix[i][j] = matrix[i][j]
        return newMatrix

    @staticmethod
    def DataIsxls(filename):
        fname = filename
        bk = xlrd.open_workbook(fname)
        sh = bk.sheet_by_name("Sheet1")
        nrows = sh.nrows
        max1 = -1
        max2 = -1
        tag = re.match('\d.*',str(sh.cell_value(0, 0)))
        start = 1
        if tag:
            start = 0
        for row in range(start, nrows, 1):
            max1 = max(max1, int(sh.cell_value(row, 0)))
            max2 = max(max2, int(sh.cell_value(row, 1)))
        max1 = max(max1, max2)+1
        matrix = [[0 for col in range(max1)]for row in range(max1)]
        for row in range(start, nrows, 1):
            matrix[int(sh.cell_value(row, 0))][int(sh.cell_value(row, 1))] = sh.cell_value(row, 2)
        return matrix

    @staticmethod
    def DataIsLabel(filename):
        filename=filename.decode('utf-8')
        bk=xlrd.open_workbook(filename)
        sh=bk.sheet_by_name("Sheet1")
        nrows = sh.nrows
        dict_label = {}
        tag = re.match('\d.*', str(sh.cell_value(0, 0)))
        start = 1
        if tag:
            start = 0
        for row in range(start, nrows, 1):
            dict_label[int(sh.cell_value(row, 0))] = sh.cell_value(row, 1)
        return dict_label