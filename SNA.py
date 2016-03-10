#coding=utf-8
from igraph import *
from LoadDateset import *

color_dict = {0: "pink", 1: "green",2:"purple",3:"orange",4:"blue",5:"yellow",6:"red",7:"#8B2500",8:"#87CEEB",9:"#707070",
              10:"#FFF68F",11:"#FFEFD5",12:"#FFE4E1",13:"#FFDEAD",14:"#FFC1C1",15:"#FFB90F",16:"#FFA54F",17:"#FF8C00",
              18:"black",19:"#FF6EB4",20:"#FF4500",21:"#FF3030",22:"#F5DEB3",23:"#F0FFFF",24:"#F08080",25:"#EED2EE",26:"#EECFA1",
              27:"#EECBAD",28:"#EEC900",29:"#DDA0DD",30:"#E3E3E3",31:"#DB7093",32:"#D8BFD8",33:"#D2B48C",34:"#CDCDB4",
              35:"#CDAD00",36:"#CD853F",37:"#CD5555",38:"#CAE1FF",39:"#BCEE68",40:"#A0522D",41:"#AEEEEE",42:"#9AFF9A",
              43:"#B03060",44:"#8B6508",45:"#8B475D",46:"#8B1A1A",47:"#836FFF",48:"#7A378B",49:"#76EEC6",50:"#698B69"}


class NetworkAnalyse:

    def __init__(self, matrixfile, labelfile=None):
        self.graph, self.weights, self.label = self.createGraph(matrixfile, labelfile)
        self.result = None
        self.listresult = None

    def createGraph(self, matrixfile, labelfile):
        data = LoadData(matrixfile, labelfile)
        matrix = data.matrix
        nodes = data.matrix.__len__()
        label = data.label
        g = Graph(nodes)
        g.vs["name"] = label.values()
        g.vs["label"] = label.values()
        edges = []
        weights = []
        for i in range(0, matrix.__len__()):
            for j in range(0, matrix.__len__()):
                if matrix[i][j] > 0:
                    edges += [(i, j)]
                    weights.append(matrix[i][j])
        g.add_edges(edges)
        return g, weights, label

    def findTopK(self, attribute):
        attrlist = self.analyse(attribute)
        list_top = []
        k = 3
        sorted_list = sorted(attrlist, reverse=True)
        for i in range(0, k, 1):
            list_top.append(attrlist.index(sorted_list[i]))
        for i in list_top:
            if i is None:
                continue
            print self.label[i],
        return list_top

    def analyse(self, attribute="authority_score"):
        if attribute == "authority_score":
            attrlist = self.graph.authority_score(weights=self.weights)
        elif attribute == "hub_score":
            attrlist = self.graph.hub_score(weights=self.weights)
        elif attribute == "pagerank":
            attrlist = self.graph.pagerank(weights=self.weights)
        elif attribute == "degree":
            attrlist = self.graph.degree()
        elif attribute == "betweeness":
            attrlist = self.graph.betweenness()
        elif attribute == "closeness":
            attrlist = self.graph.closeness()
        elif attribute == "evcent":
            attrlist = self.graph.evcent()
        else:
            attrlist = None
        return attrlist

    def community_detect(self):
        algorithm = 'fastgreedy'
        if algorithm == 'BGLL':
            self.result = self.graph.community_multilevel(self.weights)
        elif algorithm == 'walitrap':
            se = self.graph.community_walktrap(self.weights, steps=4)
            ss = se.as_clustering()
            self.result = [[]for i in range(ss.__len__())]
            for i in range(0, ss.__len__(), 1):
                    self.result[i] = (ss.__getitem__(i))
        elif algorithm == 'fastgreedy':
            se = self.graph.community_walktrap(self.weights, steps=4)
            ss = se.as_clustering()
            self.result = [[]for i in range(ss.__len__())]
            for i in range(0, ss.__len__(), 1):
                    self.result[i] = (ss.__getitem__(i))
        elif algorithm == 'LPA':
            se=self.graph.community_label_propagation(weights=self.weights)
            self.result=[[]for i in range(se.__len__())]
            for i in range(0, se.__len__(),1):
                self.result[i]=(se.__getitem__(i))
        else:
            self.result = None
        self.listresult = [0 for i in range(self.graph.vcount())]
        for i in range(0, self.result.__len__(), 1):
            for j in range(0, self.result[i].__len__(), 1):
                self.listresult[self.result[i][j]] = i


    def drawGraph(self, attribute):
        list_top = self.findTopK(attribute)
        graph = self.graph
        self.community_detect()
        layout = self.graph.layout_fruchterman_reingold()
        v_size=[]
        vs = 15
        for i in range(0, self.graph.vcount(), 1):
            if i in list_top:
                v_size.append(vs*1.8)
            else:
                v_size.append(vs)
        p = Plot()
        p.background = "#ffffff"     #将背景改为白色，默认是灰色网格
        p.add(graph,
        bbox=(50, 50, 550, 550),    #设置图占窗体的大小，默认是(0,0,600,600)
        layout =layout,                        #图的布局
        vertex_size=v_size,      #点的尺寸
        edge_width=0.5, edge_color="grey", #边的宽度和颜色，建议灰色，比较好看
        vertex_label_size=10,           #点标签的大小
        vertex_color = [color_dict[i % 50] for i in self.listresult]) #为每个点着色
        p.save("SNA.png")  #将图保存到特定路径，igraph只支持png和pdf
        p.remove(graph)         #清除图像



if __name__ == '__main__':
    matrixfile = '/media/quincy1994/软件/礼明/项目/数据集/小型数据集整理/悲惨世界人物关系77节点/l_data.xls'
    labelfile = '/media/quincy1994/软件/礼明/项目/数据集/小型数据集整理/悲惨世界人物关系77节点/l_labels.xls'
    network = NetworkAnalyse(matrixfile, labelfile)
    print "----result-----"
    print "degree:", network.drawGraph("degree")
    print "evcent:", network.drawGraph("evcent")
    print "pagerank:", network.drawGraph("pagerank")
    print "authority_score:", network.drawGraph("authority_score")
























