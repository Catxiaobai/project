# incoding:utf-8
#State,初始状态集
# Trans,初始迁移集
# State2,合并后的状态集
# T，生成的模型
import codecs
import copy
import sys
from collections import defaultdict
import numpy as np
from lzy_Complete.Main import judgeFeasibility

writepath = './file/'
filepath = './file/'
class completeModel:
    """Instances of this class represent a EFSM machine.
    A machine is set of states and trsitions.
    """
    def __init__ (self):
        """       """
        self.states_label = []
        self.TransSet=[]###迁移列表
        self.StateSet = {}#####状态列表
        self.TraceSet = [] #初始trace集合
        self.startState=[]#初始状态名称及内容
        self.Trace = []
        self.clockSet = [] # 时钟变量集合
        self.lastState={}#最终建成的模型的状态集
        self.StateLabel= [] # 状态的标号
        self.lastState2={} #补全的状态
        self.lastT=[]#######最终建成的模型的迁移集
        self.lastT2 = []  #######最终建成的模型的迁移集<=x<=,S0->START
        self.completeT=[]   #补全的迁移
        self.TLabel=[] #迁移的标号
    def copyText(self,inputfile1,inputfile2):
        # 1. 用r方式打开a.txt
        f = open(inputfile1, "r")
        # 2. 读取a.txt的内容
        buf = f.read()
        # 3. 关闭a.txt
        f.close
        # 4. 用w或者a的方式打开b.txt
        f = open(inputfile2, "w")
        # 5. 将文件写入b.txt中
        f.write(buf)
        # 6. 关闭b.txt
        f.close()
    def readModel(self,name):
        self.name = name.split('/')[-1]
        name, src, tgt, event, condition, action = "", "", "", "", "", ""
        cond2 = ""
        k = 0
        lines = open(self.name, 'r', encoding="utf-8").readlines()
        for line in lines:
            if line.strip() == "State:":  # ignore
                continue
            line = line.strip()
            if "label" in line:
                label = line.split("label=")[1]
            if "name" in line and "name=t" not in line:
                name = line.split("name=")[1]
                self.lastState[label] = name
            if line.strip() == "Transition:":  # ignore
                continue
            line = line.strip()
            if "name" in line:
                name = line.split("name=")[1]
                # Trans.append(name)
            if "src" in line:
                src = line.split("src=")[1]
                # Trans.append(src)
            if "tgt" in line:
                tgt = line.split("tgt=")[1]
                # Trans.append(tgt)
            if "event" in line:
                event = line
                event1=line.split("event=")[1]
                if event1=="null":
                    event="event="
            if "condition" in line:
                cond2 = line
                cond = line.replace("==", "=")
                cond1 = cond.split("condition=")[1]
                # print(cond1)
                if cond1=="null":
                    condition = "condition="
                else:
                    condition = "condition="
                    cond1 = cond1.split(" & ")
                    # print(cond1)
                    condList = []
                    for i in range(0, len(cond1)):
                        item = cond1[i].split("(")[1].split(")")[0]
                        condList.append(item)
                    # print(condList)
                    l = len(condList)
                    condList2 = []
                    for i in range(0, l - 1):
                        if ">=" in condList[i] and "<=" in condList[i + 1]:
                            item1 = condList[i].split(">=")[0]
                            vaule1 = condList[i].split(">=")[1]
                            item2 = condList[i + 1].split("<=")[0]
                            vaule2 = condList[i + 1].split("<=")[1]
                            if item1 == item2:
                                item = vaule1 + "<=" + item1 + "<=" + vaule2
                                condList[i + 1] = item
                            else:
                                item = condList[i]
                            condList2.append(item)
                        else:
                            item = condList[i]
                            if item not in condList2:
                                condList2.append(item)
                    if ">=" in condList[l - 2] and "<=" in condList[l - 1]:
                        item1 = condList[l - 2].split(">=")[0]
                        vaule1 = condList[l - 2].split(">=")[1]
                        item2 = condList[l - 1].split("<=")[0]
                        vaule2 = condList[l - 1].split("<=")[1]
                        if item1 == item2:
                            item = vaule1 + "<=" + item1 + "<=" + vaule2
                        else:
                            item = condList[l - 1]
                        if item not in condList:
                            condList2.append(item)
                    else:
                        item = condList[l - 1]
                        condList2.append(item)
                    # print(condList2)
                    l2 = len(condList2)
                    for i in range(0, l2 - 1):
                        condition += condList2[i] + ","
                    condition += condList2[l2 - 1]
            if "action" in line:
                action = line
                action1 = line.split("action=")[1]
                if action1 == "null":
                    action= "action="
                # Trans.append(action)
                self.lastT.append([name, src, tgt, event, condition, action])
                self.lastT2.append([name, src, tgt, event, cond2, action])
                name, src, tgt, event, condition, action = "", "", "", "", "", ""
                cond2 = ""
        print(self.lastState)
        for i in range(0, len(self.lastT2)):
            if self.lastT2[i][1] == "S0":
                self.lastT2[i][1] = "START"
            if self.lastT2[i][2] == "S0":
                self.lastT2[i][2] = "START"
        print(self.lastT2)
    def writeModel(self,State2,T,outputfile):
        wf = codecs.open(outputfile, 'w', encoding="utf-8")
        # wf1 = codecs.open("judgeFeasibility/model/resultModel2.txt", 'w', encoding="utf-8")
        for key in sorted(State2.keys(), key=lambda x: int(x[1:])):
            # if key == 'S0':
            #     wf1.write("State:\n\tname=" + 'START' + '\n')
            # else:
            #     wf1.write("State:\n\tname=" + key + '\n')
            wf.write("State:\n\tlabel=" + key + '\n\t' + "name=" + State2[key] + '\n')
        for line in T:
            if line[4].strip().split('=')[1] == "null" or not line[4].strip().split('=')[1]:
                line[4] = "condition="
            else:
                lastCond = line[4].strip().split('=', 1)[1]
                lastCond1 = lastCond.strip().split(',')
                # num_con = len(con)
                i = 0
                for j in range(0, len(lastCond1)):
                    if "!=" not in lastCond1[j] and ">=" not in lastCond1[j] and "<=" not in lastCond1[j] and "=" in \
                            lastCond1[j]:
                        lastCond1[j] = lastCond1[j].replace("=", "==")
                    if "<=" in lastCond1[j]:
                        re = lastCond1[j].split("<=")
                        if len(re) > 2:
                            lastCond1[j] = re[1] + ">=" + re[0] + ") & (" + re[1] + "<=" + re[2]
                        else:
                            lastCond1[j] = re[0] + "<=" + re[1]
                    lastCond1[j] = "(" + lastCond1[j] + ")"
                    # print(lastCond1)
                line[4] = "condition=" + " & ".join(lastCond1)
            line[5] = line[5].replace(',', ';')
            wf.write("Transition:\n\tname=" + line[0] + '\n\tsrc=' + line[1] + '\n\ttgt=' + line[2] + '\n\t' + line[
                3] + '\n\t' + line[4] + '\n\t' + line[5] + "\n")
    def judgeModelClockComplete(self):#判断时钟条件是否连续
        T2= copy.deepcopy(self.lastT)
        for i in range(0, len(T2)):
            if T2[i][1] == "S0":
                T2[i][1] = "START"
            if T2[i][2] == "S0":
                T2[i][2] = "START"
        # print(State2)
        lines = open('clockSet.txt', 'r', encoding="utf-8").readlines()
        for item in lines:
            if "," in item:
                self.clockSet+=item.split(",")
        print("时钟变量集合为：",self.clockSet)
        # 存储所有的从同一个源节点出发的时钟迁移分支集
        clockTSet = defaultdict(list)
        branchLabel=[]
        print("模型的迁移为：",T2)
        for i in range(0, len(T2) - 1):
            t1 = T2[i][0]
            src1 = T2[i][1]
            tgt1 = T2[i][2]
            event1 = T2[i][3].split("event=")[1]
            cond1 = T2[i][4]
            action1 = T2[i][5]
            flag=1
            for j in range(i + 1, len(T2)):
                t2 = T2[j][0]
                src2 = T2[j][1]
                tgt2 = T2[j][2]
                event2 = T2[j][3].split("event=")[1]
                # print(event2)
                if t1 != t2 and src1 == src2  and event1!=event2 and tgt1!=tgt2 and (event1=="" or event2==""):
                    # 时钟约束迁移分支
                    clockBranch = set()
                    if t1 not in branchLabel or t2 not in branchLabel:
                        clockBranch.add(t1)
                        clockBranch.add(t2)
                        clockTSet[src1].append(clockBranch)
                elif t1 != t2 and src1 == src2 and event1!=event2 and tgt1 == tgt2 and (event1=="" or event2==""):
                    clockBranch = set()
                    if t1 not in branchLabel or t2 not in branchLabel:
                        clockBranch.add(t1)
                        clockBranch.add(t2)
                        clockTSet[src1].append(clockBranch)
                elif t1 != t2 and src1 == src2  and event1==event2 and tgt1!=tgt2:
                    # print(src1)
                    # 时钟约束迁移分支
                    clockBranch = set()
                    if t1 not in branchLabel or t2 not in branchLabel:
                        clockBranch.add(t1)
                        clockBranch.add(t2)
                        clockTSet[src1].append(clockBranch)
                elif t1 != t2 and src1 == src2  and event1==event2 and tgt1==tgt2:
                    # print(src1)
                    # 时钟约束迁移分支
                    clockBranch = set()
                    if t1 not in branchLabel or t2 not in branchLabel:
                        clockBranch.add(t1)
                        clockBranch.add(t2)
                        clockTSet[src1].append(clockBranch)
        output = open('clockT.txt', 'w+')
        output.write(str(clockTSet))
        output.close()
        print("aaa",clockTSet)
        clockTSet2 = []
        for key, value in clockTSet.items():
            # 每个节点的时钟约束分支集
            p = list(clockTSet[key])
            for i in range(0, len(p)):
                # 获取每个节点的每一对时钟约束分支
                clockBranchLabel = list(p[i])
                # p[0]=['t1', 't7']
                clockTSet2.append(clockBranchLabel)
        print("获得时钟分支集：",clockTSet2)
        # 根据时钟分支集的时钟范围连续性获得新的迁移
        # 如果模型不全，所补的迁移
        completeT = []
        # #获取时钟迁移分支标记对应的迁移
        for i in range(0, len(clockTSet2)):
            clockBranch2 = clockTSet2[i]
            # 获取一对时钟迁移分支
            clockBranchT = []
            for value in clockBranch2:
                for i in range(0, len(T2)):
                    t = T2[i][0]
                    if t == value:
                        # print(T[i])
                        clockBranchT.append(T2[i])
            # print(clockBranchT)
            clockRangeDict = {}  # 获得时间对立分支中每一个迁移的时间范围
            for i in range(0, len(clockBranchT)):
                label = clockBranchT[i][0]
                tgt = clockBranchT[i][2]
                condition = clockBranchT[i][4].split("condition=")[1]
                Range = []
                for j in range(0, len(self.clockSet)):
                    R1 = "<=" + self.clockSet[j] + "<="
                    R2 = self.clockSet[j] + "="
                    if R1 in condition:
                        if "," in condition:
                            valueRange = condition.split(",")[1:]
                            l = len(valueRange)
                            clockRange2 = valueRange[l - 1]
                            num1 = clockRange2.split(R1)[0]
                            num2 = clockRange2.split(R1)[1]
                            Range.append(int(num1))
                            Range.append(int(num2))
                            clockRangeDict[label] = Range
                        else:
                            num1 = condition.split(R1)[0]
                            num2 = condition.split(R1)[1]
                            Range.append(int(num1))
                            Range.append(int(num2))
                            clockRangeDict[label] = Range
                    elif R2 in condition:
                        num1 = condition.split(R2)[1]
                        Range.append(int(num1))
                        clockRangeDict[label] = Range
                    # # 去除最后一个时钟范围后面的-1标志
                    # clockRange = clockRange[:-1]
            # print(clockRangeDict)
            clockRange = []  # 获取时钟范围值
            clockRangeDict2 = {}
            for key, value in clockRangeDict.items():
                clockRange.append(value)
                maxValue = max(value)
                clockRangeDict2[key] = maxValue
            clockRangeDict2 = sorted(clockRangeDict2.items(), key=lambda x: x[1])
            # 因为items是键值对元组，所以需再转回字典
            clockRangeDict2 = dict(clockRangeDict2)
            clockBranchT2 = []  # 将时间约束分支集中的迁移按时钟约束范围值排序
            for key in clockRangeDict2.keys():
                for i in range(0, len(clockBranchT)):
                    if key == clockBranchT[i][0]:
                        clockBranchT2.append(clockBranchT[i])
            print(clockBranchT2)
            # print(clockRange)
            # 将时间约束按序分布
            for i in range(0, len(clockRange) - 1):
                if max(clockRange[i]) > max(clockRange[i + 1]):
                    clockRange[i], clockRange[i + 1] = clockRange[i + 1], clockRange[i]
            print(clockRange)
            clockRangeValue=[] #判断前面的时钟在后面时钟
            for i in range(0,len(clockRange)):
                for j in range(0,len(clockRange[i])):
                    clockRangeValue.append(clockRange[i][j])
            print("所有时钟值",clockRangeValue)
            for i in range(0,len(clockRangeValue)-2): #判断时间是否连续，存在交集
                if clockRangeValue[i] in range(clockRangeValue[i+1],clockRangeValue[i+2]+1):
                    clockRange.clear()
            print(clockRange)
            clockRange2 = []  # 获取新的时钟约束范围
            l = len(clockRange)
            if l>0:
                for i in range(0, l - 1):
                    if i == 0:
                        if min(clockRange[i]) != 1 and max(clockRange[i]) != min(clockRange[i + 1]) - 1:
                            p = []
                            minValue = 0
                            maxValue = min(clockRange[i])
                            p.append(minValue)
                            p.append(maxValue)
                            clockRange2.append(p)
                        elif min(clockRange[i]) == 1 and max(clockRange[i]) != min(clockRange[i + 1]) - 1:
                            p = []
                            minValue = min(clockRange[i])
                            maxValue = max(clockRange[i])
                            p.append(minValue)
                            p.append(maxValue)
                            clockRange2.append(p)
                        elif min(clockRange[i]) != 1 and max(clockRange[i]) == min(clockRange[i + 1]) - 1:
                            p = []
                            minValue = 0
                            maxValue = min(clockRange[i])
                            p.append(minValue)
                            p.append(maxValue)
                            clockRange2.append(p)
                    else:
                        if min(clockRange[i]) != max(clockRange[i - 1]) + 1 and max(clockRange[i]) != min(
                                clockRange[i + 1]) - 1:
                            p = []
                            minValue = max(clockRange[i - 1])
                            maxValue = min(clockRange[i])
                            p.append(minValue)
                            p.append(maxValue)
                            clockRange2.append(p)
                        elif min(clockRange[i]) == max(clockRange[i - 1]) + 1 and max(clockRange[i]) != min(
                                clockRange[i + 1]) - 1:
                            p = []
                            minValue = max(clockRange[i])
                            maxValue = min(clockRange[i + 1])
                            p.append(minValue)
                            p.append(maxValue)
                            clockRange2.append(p)
                        elif min(clockRange[i]) != max(clockRange[i - 1]) + 1 and max(clockRange[i]) == min(
                                clockRange[i + 1]) - 1:
                            p = []
                            minValue = max(clockRange[i - 1])
                            maxValue = min(clockRange[i])
                            p.append(minValue)
                            p.append(maxValue)
                            clockRange2.append(p)
                p = []
                if min(clockRange[l - 1]) != max(clockRange[l - 2]) + 1:
                    minValue = max(clockRange[l - 2])
                    maxValue = min(clockRange[l - 1])
                    p.append(minValue)
                    p.append(maxValue)
                    clockRange2.append(p)
            print(clockRange2)

            # 创建新的条件
            newCond = []
            l = len(clockRange2)
            for i in range(0, l):
                newCondition = ""
                condition = clockBranchT2[i][4].split("condition=")[1]
                newCondition += "condition="
                for j in range(0, len(self.clockSet)):
                    R1 = "<=" + self.clockSet[j] + "<="
                    R2 = self.clockSet[j] + "="
                    if R1 in condition:
                        if "," in condition:
                            conditionList = condition.split(",")
                            # print(conditionList)
                            lcond = len(conditionList)  # 计算条件列表的长度
                            for k in range(0, lcond - 1):
                                if R1 in conditionList[k]:
                                    if clockRange2[i][0] == 0:
                                        R = "<=" + self.clockSet[j] + "<"
                                    else:
                                        R = "<" + self.clockSet[j] + "<"
                                    item2 = str(clockRange2[i][0]) + R + str(clockRange2[i][1]) + ","
                                    newCondition += item2
                                else:
                                    newCondition += conditionList[k] + ","
                            if R1 in conditionList[lcond - 1]:
                                if clockRange2[i][0] == 0:
                                    R = "<=" + self.clockSet[j] + "<"
                                else:
                                    R = "<" + self.clockSet[j] + "<"
                                item2 = str(clockRange2[i][0]) + R + str(clockRange2[i][1])
                                newCondition += item2
                            else:
                                newCondition += conditionList[lcond - 1]
                        else:
                            if clockRange2[i][0] == 0:
                                R = "<=" + self.clockSet[j] + "<"
                            else:
                                R = "<" + self.clockSet[j] + "<"
                            item2 = str(clockRange2[i][0]) + R + str(clockRange2[i][1])
                            newCondition += item2
                    elif R2 in condition:
                        if "," in condition:
                            conditionList = condition.split(",")
                            lcond = len(conditionList)  # 计算条件列表的长度
                            for k in range(0, lcond - 1):
                                if R2 in conditionList[k]:
                                    if clockRange2[i][0] == 0:
                                        R = "<=" + self.clockSet[j] + "<"
                                    else:
                                        R = "<" + self.clockSet[j] + "<"
                                    item2 = str(clockRange2[i][0]) + R + str(clockRange2[i][1]) + ","
                                    newCondition += item2
                                else:
                                    newCondition += conditionList[k] + ","
                            if R2 in conditionList[lcond - 1]:
                                if clockRange2[i][0] == 0:
                                    R = "<=" + self.clockSet[j] + "<"
                                else:
                                    R = "<" + self.clockSet[j] + "<"
                                item2 = str(clockRange2[i][0]) + R + str(clockRange2[i][1])
                                newCondition += item2
                            else:
                                newCondition += conditionList[lcond - 1]
                        else:
                            if clockRange2[i][0] == 0:
                                R = "<=" + self.clockSet[j] + "<"
                            else:
                                R = "<" + self.clockSet[j] + "<"
                            item2 = str(clockRange2[i][0]) + R + str(clockRange2[i][1])
                            newCondition += item2
                newCond.append(newCondition)
            # print("bbb",clockBranchT2)
            print("aaa:", newCond)
            # 获取新的迁移
            l = len(newCond)
            # print(l)
            if l == 0:
                continue
            elif l >= 2:
                downNewT = []  # 根据上下界构造两条新的迁移
                downNewT.append(clockBranchT2[0][0])
                downNewT.append(clockBranchT2[0][1])
                downNewT.append(clockBranchT2[0][2])
                downNewT.append(clockBranchT2[0][3])
                downNewT.append(newCond[0])
                # print(clockSet)
                action = "action="
                downNewT.append(action)
                # downNewT.append(clockBranchT2[0][5])
                self.completeT.append(downNewT)
                for i in range(1, l):
                    downNewT = []  # 根据上下界构造两条新的迁移
                    upNewT = []
                    downNewT.append(clockBranchT2[i - 1][0])
                    downNewT.append(clockBranchT2[i - 1][1])
                    downNewT.append(clockBranchT2[i - 1][2])
                    downNewT.append(clockBranchT2[i - 1][3])
                    downNewT.append(newCond[i])
                    # print(clockSet)
                    action = "action="
                    downNewT.append(action)
                    # downNewT.append(clockBranchT2[i-1][5])
                    upNewT.append(clockBranchT2[i][0])
                    upNewT.append(clockBranchT2[i][1])
                    upNewT.append(clockBranchT2[i][2])
                    upNewT.append(clockBranchT2[i][3])
                    upNewT.append(newCond[i])
                    action = "action="
                    upNewT.append(action)
                    # upNewT.append(clockBranchT2[i][5])
                    self.completeT.append(downNewT)
                    self.completeT.append(upNewT)
            else:
                downNewT = []  # 根据上下界构造两条新的迁移
                downNewT.append(clockBranchT2[0][0])
                downNewT.append(clockBranchT2[0][1])
                downNewT.append(clockBranchT2[0][2])
                downNewT.append(clockBranchT2[0][3])
                downNewT.append(newCond[0])
                # print(clockSet)
                action = "action="
                downNewT.append(action)
                # downNewT.append(clockBranchT2[0][5])
                self.completeT.append(downNewT)
        print("待补全的时钟迁移：",self.completeT)
        completeT2 = copy.deepcopy(self.completeT)
        self.completeT.clear()
        for item in completeT2:
            if item not in self.completeT:
                self.completeT.append(item)
        print(self.completeT)
        maxStateLabel = 0  # 计算当前状态标签的最大值
        for key in self.lastState:
            if key!="START":
                item = int(key.split("S")[1])
                if maxStateLabel < int(item):
                    maxStateLabel = item
        print(maxStateLabel)
        flagTar =1
        for i in range(0, len(self.completeT)):
            self.completeT[i][2] = "S" + str(maxStateLabel + flagTar)
            flagTar+= 1
        maxTLabel = 0  # 计算当前状态标签的最大值
        for i in range(0, len(self.lastT)):
            item = int(self.lastT[i][0].split("t")[1])
            if maxTLabel < int(item):
                maxTLabel = item
        print(maxTLabel)
        flagT=1
        for i in range(0,len(self.completeT)):
            self.completeT[i][0]="t"+str(maxTLabel+flagT)
            flagT+=1
        print(self.completeT)
    def judgeModelCondComplete(self):  # 判断条件是否对立分支完整
        # print(stateLabel)
        maxStateLabel = 0  # 计算当前状态标签的最大值
        for i in range(0, len(self.completeT)):
            if self.completeT[i][2]!="START":
                item = int(self.completeT[i][2].split("S")[1])
                if maxStateLabel < int(item):
                    maxStateLabel = item
        print(maxStateLabel)
        maxTLabel = 0  # 计算当前状态标签的最大值
        for i in range(0, len(self.completeT)):
            item = int(self.completeT[i][0].split("t")[1])
            if maxTLabel < int(item):
                    maxTLabel = item
        print(maxTLabel)
        # print(self.lastT)
        print(self.clockSet)
        print(self.lastT)
        # # TBound={}#标记计数条件是否完整，0代表有下界 1代表有上界
        counterCondSet = {}
        for i in range(0, len(self.lastT)):
            # # 存储没有找到条件对立分支的条件及其所在迁移
            # counterCondSet = {}
            t1 = self.lastT[i][0]
            src1 = self.lastT[i][1]
            tgt1 = self.lastT[i][2]
            event1 = self.lastT[i][3]
            cond1 = self.lastT[i][4].split("condition=")[1]
            # print(cond1)
            if cond1 == "null" or not cond1:
                continue
            else:
                cond1 = cond1.split(",")
                l= len(cond1)
                for k in range(0, l):
                    flag = 1
                    # 寻找每一个条件的对立分支
                    for j in range(0, len(self.lastT)):
                        t2 = self.lastT[j][0]
                        src2 = self.lastT[j][1]
                        tgt2 = self.lastT[j][2]
                        event2 = self.lastT[j][3]
                        cond2 = self.lastT[j][4].split("condition=")[1]
                        flag2=1
                        if t2 != t1:
                            if src2 == src1 and (cond2 != "null" or not cond2):
                                cond2 = cond2.split(",")
                                for index in range(0, len(cond2)):
                                    print(t1)
                                    print(t2)
                                    print("当前的条件为：" + cond1[k])
                                    print("寻找待匹配的条件：" + cond2[index])
                                    # print(cond2[k])
                                    # print(cond1[k])
                                    # if cond1[0:k]==cond2[0:k]
                                    if "!=" in cond1[k] and "=" in cond2[index] and "!=" not in cond2[index] and "<=" not in cond2[index] and ">=" not in cond2[index]:
                                        variable1 = cond1[k].split("!=")
                                        variable2 = cond2[index].split("=")
                                        # print(variable1)
                                        # print(variable2)
                                        # print("aaa")
                                        if variable1[0] in self.clockSet and variable2[0] in self.clockSet:
                                            flag = 0
                                            flag2 = 1
                                            break
                                        if variable1 == variable2:
                                            flag = 0
                                            flag2 = 1
                                            break
                                    elif "!=" in cond2[index] and "=" in cond1[k] and "!=" not in cond1[k] and "<=" not in \
                                            cond1[k] and ">=" not in cond1[k]:
                                        variable1 = cond1[k].split("=")
                                        variable2 = cond2[index].split("!=")
                                        # print("bbb")
                                        # print(variable1[0])
                                        # print(variable2[0])
                                        if variable1[0] in self.clockSet and variable2[0] in self.clockSet:
                                            flag = 0
                                            flag2 = 0
                                            break
                                        if variable1 == variable2:
                                            flag = 0
                                            flag2 = 0
                                            break
                                    elif "=" in cond1[k] and "!=" not in cond1[k] and "<=" not in \
                                            cond1[k] and ">=" not in cond1[k] and "=" in cond2[index] and "!=" not in cond2[index] and "<=" not in \
                                            cond2[index] and ">=" not in cond2[index]:
                                        variable1 = cond1[k].split("=")
                                        variable2 = cond2[index].split("=")
                                        # print("ccc")
                                        # print(variable1)
                                        # print(variable2)
                                        if variable1[0] in self.clockSet and variable2[0] in self.clockSet:
                                            flag = 0
                                            flag2 =0
                                            break
                                        if variable1[0] == variable2[0]:
                                            flag = 0
                                            flag2 =0
                                            break
                                    elif "<=" in cond1[k] and ">" in cond2[index] and ">=" not in cond2[index]:
                                        variable1 = cond2[index].split(">")[0]
                                        # print(variable1)
                                        # print("ddd")
                                        value1 = cond2[index].split(">")[1]
                                        listInequality = cond1[k].split("<=")
                                        # print(listInequality)
                                        if len(listInequality) == 3:
                                            variable2 = listInequality[1]
                                            value2 = listInequality[-1]
                                            # print(variable2)
                                            # print(value2)
                                            valueMin = listInequality[0]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        else:
                                            variable2 = listInequality[0]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif "<=" in cond2[index] and ">" in cond1[k] and ">=" not in cond1[k]:
                                        variable1 = cond1[k].split(">")[0]
                                        # print("fff")
                                        # print(variable1)
                                        value1 = cond1[k].split(">")[1]
                                        listInequality = cond2[index].split("<=")
                                        if len(listInequality) == 3:
                                            variable2 = listInequality[1]
                                            value2 = listInequality[-1]
                                            valueMin = listInequality[0]
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        else:
                                            variable2 = listInequality[0]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif "<=" in cond2[index] and "=" in cond1[k] and ">=" not in cond1[k] and "!=" not in \
                                            cond1[k] and "<=" not in cond1[k]:
                                        # print("ggg")
                                        variable1 = cond1[k].split("=")[0]
                                        # print(variable1)
                                        value1 = cond1[k].split("=")[1]
                                        listInequality = cond2[index].split("<=")
                                        if len(listInequality) == 3:
                                            variable2 = listInequality[1]
                                            value2 = listInequality[-1]
                                            valueMin = listInequality[0]
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        else:
                                            variable2 = listInequality[0]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        # print(value2)
                                        # print(flag)
                                    elif "<=" in cond1[k] and "=" in cond2[index] and ">=" not in cond2[index] and "!=" not in \
                                            cond2[index] and "<=" not in cond2[index]:
                                        # print("hhh")
                                        variable1 = cond2[index].split("=")[0]
                                        # print(variable1)
                                        value1 = cond2[index].split("=")[1]
                                        # print(value1)
                                        listInequality = cond1[k].split("<=")
                                        # print(listInequality)
                                        if len(listInequality) == 3:
                                            variable2 = listInequality[1]
                                            value2 = listInequality[-1]
                                            # print(variable2)
                                            # print(value2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        else:
                                            variable2 = listInequality[0]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif "<=" in cond2[index] and "!=" in cond1[k]:
                                        # print("ll")
                                        variable1 = cond1[k].split("!=")[0]
                                        # print(variable1)
                                        value1 = cond1[k].split("!=")[1]
                                        listInequality = cond2[index].split("<=")
                                        if len(listInequality) == 3:
                                            variable2 = listInequality[1]
                                            value2 = listInequality[-1]
                                            valueMin = listInequality[0]
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        else:
                                            variable2 = listInequality[0]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif "<=" in cond1[k] and "!=" in cond2[index]:
                                        # print("pp")
                                        variable1 = cond2[index].split("!=")[0]
                                        # print(variable1)
                                        value1 = cond2[index].split("!=")[1]
                                        # print(value1)
                                        listInequality = cond1[k].split("<=")
                                        # print(listInequality)
                                        if len(listInequality) == 3:
                                            variable2 = listInequality[1]
                                            value2 = listInequality[-1]
                                            # print(variable2)
                                            # print(value2)
                                            valueMin = listInequality[0]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        else:
                                            variable2 = listInequality[0]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif ">" in cond1[k] and ">=" not in cond1[k] and "<=" in cond2[index]:
                                        variable1 = cond1[k].split(">")[0]
                                        # print("iii")
                                        # print(variable1)
                                        value1 = cond1[k].split(">")[1]
                                        # print(value1)
                                        listInequality = cond2[index].split("<=")
                                        if len(listInequality) == 3:
                                            variable2 = listInequality[1]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            valueMin = listInequality[0]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        else:
                                            variable2 = listInequality[0]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif "<=" in cond1[k] and ">" in cond2[index] and ">=" not in cond2[index]:
                                        variable1 = cond2[index].split(">")[0]
                                        # print("jjj")
                                        # print(variable1)
                                        value1 = cond2[index].split(">")[1]
                                        # print(value1)
                                        listInequality = cond1[k].split("<=")
                                        if len(listInequality) == 3:
                                            variable2 = listInequality[1]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        else:
                                            variable2 = listInequality[0]
                                            # print(variable2)
                                            value2 = listInequality[-1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif "<" in cond1[k] and "<=" not in cond1[k] and "<=" in \
                                            cond2[index]:
                                        # print("kkk")
                                        listInequality1 = cond1[k].split("<")
                                        listInequality2 = cond2[index].split("<=")
                                        if len(listInequality1) == 3 and len(listInequality2) == 3:
                                            variable1 = listInequality1[1]
                                            variable2 = listInequality2[1]
                                            # print(variable1)
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        if len(listInequality1) == 3 and len(listInequality2) != 3:
                                            variable1 = listInequality1[1]
                                            variable2 = listInequality2[0]
                                            # print(variable1)
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        if len(listInequality1) != 3 and len(listInequality2) == 3:
                                            variable1 = listInequality1[0]
                                            variable2 = listInequality2[1]
                                            # print(variable1)
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif "<=" in cond1[k] and "<" in cond2[index] and "<=" not in cond2[index]:
                                        # print("lll")
                                        listInequality1 = cond2[index].split("<")
                                        listInequality2 = cond1[k].split("<=")
                                        if len(listInequality1) == 3 and len(listInequality2) == 3:
                                            # print(variable1)
                                            # print(variable2)
                                            variable1 = listInequality1[1]
                                            variable2 = listInequality2[1]
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        if len(listInequality1) == 3 and len(listInequality2) != 3:
                                            variable1 = listInequality1[1]
                                            variable2 = listInequality2[0]
                                            # print(variable1)
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        if len(listInequality1) != 3 and len(listInequality2) == 3:
                                            variable1 = listInequality1[0]
                                            variable2 = listInequality2[1]
                                            # print(variable1)
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                    elif "<=" in cond1[k] and "<=" in cond2[index]:
                                        # print("mmm")
                                        listInequality1 = cond1[k].split("<=")
                                        listInequality2 = cond2[index].split("<=")
                                        if len(listInequality1) == 3 and len(listInequality2) == 3:
                                            variable1 = listInequality1[1]
                                            variable2 = listInequality2[1]
                                            # print(variable1)
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        if len(listInequality1) == 3 and len(listInequality2) != 3:
                                            variable1 = listInequality1[1]
                                            variable2 = listInequality2[0]
                                            # print(variable1)
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                                        if len(listInequality1) != 3 and len(listInequality2) == 3:
                                            variable1 = listInequality1[0]
                                            variable2 = listInequality2[1]
                                            # print(variable1)
                                            # print(variable2)
                                            if variable1 in self.clockSet and variable2 in self.clockSet:
                                                flag = 0
                                                flag2 = 0
                                                break
                                            if variable1 == variable2:
                                                flag = 0
                                                flag2 = 0
                                                break
                        if flag2==0:
                            break
                        else:
                            continue
                    # 如果没有找到该条件的分支
                    # print(flag)
                    if flag == 1:
                        counterCondSet[cond1[k]] = t1
        print(counterCondSet)
        if len(counterCondSet) > 0:
            # print(counterCondSet)
            countValue = 1
            for key, value in counterCondSet.items():
                # 需要补全的迁移及后续迁移
                needChangeCond = key
                newSatateLabel = ""
                completeT = []
                flag = 1
                for j in range(0, len(self.lastT)):
                    t = self.lastT[j][0]
                    src = self.lastT[j][1]
                    target = self.lastT[j][2]
                    event = self.lastT[j][3].split("event=")[1]
                    cond = self.lastT[j][4].split("condition=")[1]
                    action = self.lastT[j][5].split("action=")[1]
                    if t == value:
                        src1 = "source:" +self.lastState[src]
                        target1 = "target:" + target + ":" + self.lastState[target]
                        # existKey = []
                        # for index in StateSet.keys():
                        #     existKey.append(index)
                        # maxStateLabe = existKey[-1]
                        event1 = "event:" + event
                        cond1 = "condition:" + cond
                        action1 = "action:" + action
                        # print(event)
                        # print(cond)
                        completeT.append("Transition:")
                        completeT.append(src1)
                        completeT.append(event1)
                        completeT.append(cond1)
                        completeT.append(action1)
                        completeT.append(target1)
                        break
                # print(completeT)
                # print("需要："+needChangeCond)
                if "!=" in needChangeCond:
                    newChangeCond = needChangeCond.split("!=")[0] + "=" + needChangeCond.split("!=")[1]
                elif "<=" in needChangeCond:
                    newChangeCond = needChangeCond.split("<=")
                    # print(newChangeCond)
                    if len(newChangeCond) == 3:
                        if newChangeCond[0] != '0':
                            newChangeCond = "(" + newChangeCond[1] + "<" + newChangeCond[0] + ") | (" + newChangeCond[
                                1] + ">" + newChangeCond[2] + ")"
                        else:
                            newChangeCond = newChangeCond[1] + ">" + newChangeCond[2]
                    else:
                        newChangeCond = newChangeCond[0] + ">" + newChangeCond[1]
                elif ">=" in needChangeCond:
                    newChangeCond = needChangeCond.split(">=")[0] + "<" + needChangeCond.split(">=")[1]
                elif "=" in needChangeCond:
                    newChangeCond = needChangeCond.split("=")
                    if newChangeCond[1].isdigit():
                        newChangeCond = "(" + newChangeCond[0] + "<" + newChangeCond[1] + ") | (" + newChangeCond[
                            0] + ">" + newChangeCond[1] + ")"
                    else:
                        newChangeCond = newChangeCond[0] + "!=" + newChangeCond[1]
                elif ">" in needChangeCond:
                    newChangeCond = needChangeCond.split(">")[0] + "<" + needChangeCond.split(">")[1]
                elif "<" in needChangeCond:
                    newChangeCond = needChangeCond.split("<")
                    # print(newChangeCond)
                    if len(newChangeCond) == 3:
                        if newChangeCond[0] != '0':
                            newChangeCond = "(" + newChangeCond[1] + "<=" + newChangeCond[0] + ") | (" + newChangeCond[
                                1] + ">=" + newChangeCond[2] + ")"
                        else:
                            newChangeCond = newChangeCond[1] + ">=" + newChangeCond[2]
                    else:
                        newChangeCond = newChangeCond[0] + ">=" + newChangeCond[1]
                # print(needChangeCond)
                newCond = completeT[3].split(needChangeCond)[0] + newChangeCond + completeT[3].split(needChangeCond)[1]
                print("新构成的条件为：" + newCond)
                newSatateLabel = "S" + str(maxStateLabel + countValue)
                newCond2 = newCond.split("condition:")[1]  # 推荐加入的对立分支条件
                addT = []
                label = "t" + str(int(maxTLabel) + countValue)
                addT.append(label)
                addT.append(src)
                addT.append(newSatateLabel)
                addevent = "event=" + event
                addnewCond = "condition=" + newCond2
                addaction = "action=null"
                addT.append(addevent)
                addnewCond2 = addnewCond
                addT.append(addnewCond2)
                addT.append(addaction)
                print(addT)
                self.completeT.append(addT)
                countValue += 1
        print(self.completeT)
    def completeModel(self):
        existKey = []  # 已经存在的状态编号
        for index in self.lastState.keys():
            existKey.append(index)
        print("已存在的状态", existKey)
        completeT2 = copy.deepcopy(self.completeT)
        T2=copy.deepcopy(self.lastT)
        if len(completeT2) > 0:
            print("时钟条件的时钟范围不连续，模型不完整,需要补全")
            print(completeT2)
            for i in range(0, len(completeT2)):
                event = completeT2[i][3].split("event=")[1]
                condition = completeT2[i][4].split("condition=")
                action = completeT2[i][5].split("action=")
                if event == "null":
                    event = ""
                    completeT2[i][3] = "event=" + event
                if condition[1] == "null":
                    condition = ""
                    completeT2[i][4] = "condition=" + condition
                else:
                    if "," in condition[1]:
                        lastCond1 = condition[1].split(",")
                        # print(lastCond1)
                        for j in range(0, len(lastCond1)):
                            if "!=" not in lastCond1[j] and ">=" not in lastCond1[j] and "<=" not in lastCond1[
                                j] and "=" in \
                                    lastCond1[j]:
                                lastCond1[j] = lastCond1[j].replace("=", "==")
                            if "<=" in lastCond1[j] and ") | (" not in lastCond1[j]:
                                re = lastCond1[j].split("<=")
                                # print(re)
                                if len(re) > 2:
                                    lastCond1[j] = re[1] + ">=" + re[0] + ") & (" + re[1] + "<=" + re[2]
                                elif "<" in re[1]:
                                    re1 = re[1].split("<")
                                    lastCond1[j] = re1[0] + ">=" + re[0] + ") & (" + re1[0] + "<" + re1[1]
                                else:
                                    lastCond1[j] = re[0] + "<=" + re[1]
                            if "<" in lastCond1[j]:
                                re = lastCond1[j].split("<")
                                # print(re)
                                if len(re) > 2:
                                    lastCond1[j] = re[1] + ">" + re[0] + ") & (" + re[1] + "<" + re[2]
                                elif "<=" in re[1]:
                                    re1 = re[1].split("<=")
                                    lastCond1[j] = re1[0] + ">" + re[0] + ") & (" + re1[0] + "<=" + re1[1]
                                else:
                                    lastCond1[j] = re[0] + "<" + re[1]
                            lastCond1[j] = "(" + lastCond1[j] + ")"
                        addnewCond = "condition=" + " & ".join(lastCond1)
                    else:
                        lastCond = condition
                        # print(lastCond[1])
                        if lastCond[1]:
                            if "!=" not in lastCond[1] and ">=" not in lastCond[1] and "<=" not in lastCond[
                                1] and "=" in \
                                    lastCond[1]:
                                lastCond[1] = lastCond[1].replace("=", "==")
                            if "<=" in lastCond[1]:
                                re = lastCond[1].split("<=")
                                # print(re)
                                if len(re) > 2:
                                    lastCond[1] = re[1] + ">=" + re[0] + ") & (" + re[1] + "<=" + re[2]
                                elif "<" in re[1]:
                                    re1 = re[1].split("<")
                                    lastCond[1] = re1[0] + ">=" + re[0] + ") & (" + re1[0] + "<" + re1[1]
                                else:
                                    lastCond[1] = re[0] + "<=" + re[1]
                            if "<" in lastCond[1]:
                                re = lastCond[1].split("<")
                                # print(re)
                                if len(re) > 2:
                                    lastCond[1] = re[1] + ">" + re[0] + ") & (" + re[1] + "<" + re[2]
                                elif "<=" in re[1]:
                                    re1 = re[1].split("<=")
                                    lastCond[1] = re1[0] + ">" + re[0] + ") & (" + re1[0] + "<=" + re1[1]
                                else:
                                    lastCond[1] = re[0] + "<" + re[1]
                                lastCond[1] = "(" + lastCond[1] + ")"
                        addnewCond = "condition=" + lastCond[1]
                    completeT2[i][4] = addnewCond
                if action[1] == "null":
                    action = ""
                    completeT2[i][5] = "action=" + action
                else:
                    # print(condition)
                    action= action[1].replace(",", ";")
                    # print(action)
                    if "(" in action and ")" in action and "()" not in action:
                        t = action.split("(")
                        t2 = t[1].split(")")
                        # print(t2)
                        if ";" in t2[0]:
                            t2[0] = t2[0].replace(";", ",")
                        if t2[1]:
                            action = t[0] + "(" + t2[0] + ")" + t2[1]
                        else:
                            action = t[0] + "(" + t2[0] + ")"
                    completeT2[i][5] = "action=" + action
            print(completeT2)
            savedStdout = sys.stdout  # 保存标准输出流
            with open('failureTran/target2.txt', 'w+') as file:
                sys.stdout = file  # 标准输出重定向至文件
                index = len(T2)
                flagTar = 0  # target新的编号
                for i in range(0, len(completeT2)):
                    label =completeT2[i][0]
                    src = completeT2[i][1]
                    target = completeT2[i][2]
                    event = completeT2[i][3].split("event=")[1]
                    condition = completeT2[i][4].split("condition=")[1]
                    # print(condition)
                    action = completeT2[i][5].split("action=")[1]
                    print(label + ", " + src + ", " + target + ", " + event + ", " + condition + ", " + action + ",")
                    flagTar += 1
            sys.stdout = savedStdout  # 恢复标准输出流
            print(T2)
            newState = copy.deepcopy(self.lastState)  # 将状态列表复制一份
            newState2 = {}
            for key, value in newState.items():
                if key == "S0":
                    key = "START"
                newState2[key] = value
            print(newState2)
            # 输出成模型的标准形式，为后续可行性验证作准备
            savedStdout = sys.stdout  # 保存标准输出流
            with open('model/resultModel2.txt', 'w+') as file:
                sys.stdout = file  # 标准输出重定向至文件
                for key, value in newState2.items():
                    # print("State:\n\tlabel=" + key + '\n\t' + "name=" +value+ '\n')
                    print("State:\n\tname=" + key)
                for i in range(0, len(self.lastT2)):
                    print("Transition:\n\tname=" + self.lastT2[i][0] + '\n\tsrc=' + self.lastT2[i][1] + '\n\ttgt=' +
                          self.lastT2[i][2] + '\n\t' +
                          self.lastT2[i][3] + '\n\t' + self.lastT2[i][4] + '\n\t' + self.lastT2[i][5])
            sys.stdout = savedStdout  # 恢复标准输出流
            # 可行的迁移
            feasibleT = []
            result = judgeFeasibility("failureTran/target2.txt", "model/resultModel2.txt")
            print(result)
            for i in range(0, len(result)):
                if result[i][0] == 1 and result[i][1] == 1:  # 如果可行：
                    feasibleT.append(completeT2[i])
            print(feasibleT)
            if (len(feasibleT) > 0):
                maxTLabel = 0  # 计算当前状态标签的最大值
                for i in range(0, len(self.lastT)):
                    item = int(self.lastT[i][0].split("t")[1])
                    if maxTLabel < int(item):
                        maxTLabel = item
                # print(maxTLabel)
                maxStateLabel = 0  # 计算当前状态标签的最大值
                for key in self.lastState:
                    if key != "START":
                        item = int(key.split("S")[1])
                        if maxStateLabel < int(item):
                            maxStateLabel = item
                # print(maxStateLabel)
                savedStdout = sys.stdout  # 保存标准输出流
                with open(filepath + 'outNew.txt', 'w+', encoding='utf-8') as file:
                    sys.stdout = file  # 标准输出重定向至文件
                    print("N")
                    # for key, value in self.lastState.items():
                    #     print(key + "->" + value)
                    # print("推荐补全的迁移为:")
                    count=1
                    for i in range(len(feasibleT)):
                        # print("需要修改的条件所在的迁移为：")
                        # print(completeT)
                        # print("需要修改为其对立条件的条件分支:" + needChangeCond)
                        feasibleT[i][0]="t"+str(maxTLabel+count)
                        feasibleT[i][2]="S"+str(maxStateLabel+count)
                        print(feasibleT[i][0] + ", " + feasibleT[i][1] + ", " + feasibleT[i][2] + ", " + feasibleT[i][
                            3] + ", " + feasibleT[i][4] + ", " + feasibleT[i][5])
                        count+=1
                sys.stdout = savedStdout  # 恢复标准输出流
                self.completeT.clear()
            else:
                print("模型完整")
                savedStdout = sys.stdout  # 保存标准输出流
                with open(filepath + 'outNew.txt', 'w+') as file1:
                    sys.stdout = file1  # 标准输出重定向至文件
                    print("Y")
                    # for key, value in State2.items():
                    #     print(key + "->" + value)
                sys.stdout = savedStdout  # 恢复标准输出流
        else:
            print("模型完整")
            savedStdout = sys.stdout  # 保存标准输出流
            with open(filepath + 'outNew.txt', 'w+') as file1:
                sys.stdout = file1  # 标准输出重定向至文件
                print("Y")
                # for key, value in State2.items():
                #     print(key + "->" + value)
            sys.stdout = savedStdout  # 恢复标准输出流
if __name__ == '__main__':
    s=completeModel()
    s.readModel("resultModel.txt")
    s.judgeModelClockComplete()
    s.judgeModelCondComplete()
    s.completeModel()








