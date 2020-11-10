# # incoding:utf-8
# #State,初始状态集
# # Trans,初始迁移集
# # State2,合并后的状态集
# # T，生成的模型
# import copy
# import sys
# # from constructModel1 import getTransState1, constructModel1
# from lzy_Complete.Main import judgeFeasibility
#
# writepath = './file/'
# filepath = './file/'
# #badCond是指每次查到这个不可行的条件，但是补的对立不可行，就去除这个条件，不再进行完整性判断，初始传入None
# def judgeModelComplete1():
#     T = []
#     name, src, tgt, event, condition, action = "", "", "", "", "",""
#     cond2=""
#     k = 0
#     # 状态列表
#     State2= {}
#     T2=[]
#     lines = open(filepath+'result.txt', 'r', encoding="utf-8").readlines()
#     for line in lines:
#         if line.strip() == "State:":  # ignore
#             continue
#         line = line.strip()
#         if "label" in line:
#             label= line.split("label=")[1]
#         if "name" in line and "name=t" not in line:
#             name= line.split("name=")[1]
#             State2[label]=name
#         if line.strip() == "Transition:":  # ignore
#             continue
#         line = line.strip()
#         if "name" in line:
#             name = line.split("name=")[1]
#             # Trans.append(name)
#         if "src" in line:
#             src = line.split("src=")[1]
#             # Trans.append(src)
#         if "tgt" in line:
#             tgt = line.split("tgt=")[1]
#             # Trans.append(tgt)
#         if "event" in line:
#             event = line
#             # Trans.append(src)
#         if "condition" in line:
#             cond2=line
#             cond=line.replace("==", "=")
#             cond1= cond.split("condition=")[1]
#             # print(cond1)
#             if not cond1:
#                 condition="condition=null"
#             else:
#                 condition= "condition="
#                 cond1=cond1.split(" & ")
#                 print(cond1)
#                 condList=[]
#                 for i in range(0,len(cond1)):
#                     item=cond1[i].split("(")[1].split(")")[0]
#                     condList.append(item)
#                 # print(condList)
#                 l=len(condList)
#                 condList2=[]
#                 for i in range(0, l-1):
#                     if ">=" in condList[i] and "<=" in condList[i+1]:
#                         item1 = condList[i].split(">=")[0]
#                         vaule1=condList[i].split(">=")[1]
#                         item2 = condList[i+1].split("<=")[0]
#                         vaule2 = condList[i+1].split("<=")[1]
#                         if item1==item2:
#                             item=vaule1+"<="+item1+"<="+vaule2
#                             condList[i+1]=item
#                         else:
#                             item=condList[i]
#                         condList2.append(item)
#                     else:
#                         item = condList[i]
#                         if item not in condList2:
#                             condList2.append(item)
#                 if ">=" in condList[l-2] and "<=" in condList[l-1]:
#                     item1 = condList[l-2].split(">=")[0]
#                     vaule1 = condList[l-2].split(">=")[1]
#                     item2 = condList[l-1].split("<=")[0]
#                     vaule2 = condList[l-1].split("<=")[1]
#                     if item1 == item2:
#                         item = vaule1 + "<=" + item1 + "<=" + vaule2
#                     else:
#                         item = condList[l-1]
#                     if item not in condList:
#                         condList2.append(item)
#                 else:
#                     item = condList[l-1]
#                     condList2.append(item)
#                 # print(condList2)
#                 l2=len(condList2)
#                 for i in range(0,l2-1) :
#                     condition+=condList2[i]+","
#                 condition+=condList2[l2-1]
#         if "action" in line:
#             action =line
#             # Trans.append(action)
#             T.append([name, src, tgt, event, condition, action])
#             T2.append([name, src, tgt, event, cond2, action])
#             name,src, tgt, event, condition, action = "", "", "", "", "",""
#             cond2=""
#     print(State2)
#     stateLabel = []
#     for key in State2.keys():
#         stateLabel.append(key)
#     print(stateLabel)
#     maxStateLabel = 0 #计算当前状态标签的最大值
#     for i in range(0, len(stateLabel)):
#             item= int(stateLabel[i].split("S")[1])
#             if maxStateLabel<int(item):
#                 maxStateLabel=item
#     print(maxStateLabel)
#     print(T)
#     print(T2)
#     newState = copy.deepcopy(State2)  # 将状态列表复制一份
#     newState2 = {}
#     for key, value in newState.items():
#         if key == "S0":
#             key = "START"
#         newState2[key] = value
#     print(newState2)
#     for i in range(0,len(T2)):
#         if T2[i][1] == "S0":
#             T2[i][1] = "START"
#         if T2[i][2] == "S0":
#             T2[i][2] = "START"
#     print(T2)
#     # 输出成模型的标准形式，为后续可行性验证作准备
#     savedStdout = sys.stdout  # 保存标准输出流
#     with open(filepath+'resultModel2.txt', 'w+') as file:
#         sys.stdout = file  # 标准输出重定向至文件
#         for key, value in newState2.items():
#             # print("State:\n\tlabel=" + key + '\n\t' + "name=" +value+ '\n')
#             print("State:\n\tname=" + key)
#         for i in range(0, len(T2)):
#             print("Transition:\n\tname=" + T2[i][0] + '\n\tsrc=' + T2[i][1] + '\n\ttgt=' +
#                   T2[i][2] + '\n\t' +
#                   T2[i][3] + '\n\t' + T2[i][4] + '\n\t' + T2[i][5])
#     sys.stdout = savedStdout  # 恢复标准输出流
#
#     # 存储没有找到条件对立分支的条件及其所在迁移
#     counterCondSet = {}
#     for i in range(0, len(T)):
#         # # 存储没有找到条件对立分支的条件及其所在迁移
#         # counterCondSet = {}
#         t1 = T[i][0]
#         src1 = T[i][1]
#         tgt1 = T[i][2]
#         event1 = T[i][3]
#         cond1 = T[i][4].split("condition=")[1]
#         if cond1 == "null":
#             continue
#         else:
#             cond1 = cond1.split(",")
#             l = len(cond1)
#             for k in range(0, len(cond1)):
#                 flag = 1
#                 # 寻找每一个条件的对立分支
#                 for j in range(0, len(T)):
#                     t2 = T[j][0]
#                     src2 = T[j][1]
#                     tgt2 = T[j][2]
#                     event2 = T[j][3]
#                     cond2 = T[j][4].split("condition=")[1]
#                     if t2 != t1:
#                         if src2 == src1 and tgt2 != tgt1 and event2 == event1 and cond2 != "null":
#                             cond2 = cond2.split(",")
#                             # print(t1)
#                             # print(t2)
#                             # print(cond1)
#                             # print(cond2)
#                             count = 0
#                             if k == 0:
#                                 count = 0
#                             else:
#                                 for n in range(0, k):
#                                     if cond1[n] == cond2[n]:
#                                         count += 1
#                             if count == k:
#                                 if "!=" in cond1[k] and "=" in cond2[k]:
#                                     variable1 = cond1[k].split("!=")
#                                     variable2 = cond2[k].split("=")
#                                     # print(variable1)
#                                     # print(variable1)
#                                     if variable1 == variable2:
#                                         flag = 0
#                                 elif "!=" in cond2[k] and "=" in cond1[k]:
#                                     variable1 = cond1[k].split("=")
#                                     variable2 = cond2[k].split("!=")
#                                     # print(variable1)
#                                     # print(variable1)
#                                     if variable1 == variable2:
#                                         flag = 0
#                                 elif "<=" in cond1[k] and ">" in cond2[k]:
#                                     variable1 = cond1[k].split("<=")
#                                     variable2 = cond2[k].split(">")
#                                     # print(t1)
#                                     # print(t2)
#                                     # print(variable1)
#                                     # print(variable1)
#                                     if variable1 == variable2:
#                                         flag = 0
#                                 elif "<=" in cond2[k] and ">" in cond1[k]:
#                                     variable1 = cond1[k].split(">")
#                                     variable2 = cond2[k].split("<=")
#                                     # print(variable1)
#                                     # print(variable1)
#                                     if variable1 == variable2:
#                                         flag = 0
#                                 elif "=" in cond1[k] and "<=" in cond2[k]:
#                                     variable1 = cond1[k].split("=")[0]
#                                     variable2 = cond2[k].split("<=")[1].split("<=")[0]
#                                     # print(variable1)
#                                     # print(variable1)
#                                     if variable1 == variable2:
#                                         flag = 0
#                                     # print(flag)
#                                 elif "=" in cond2[k] and "<=" in cond1[k]:
#                                     variable1 = cond1[k].split("<=")[1].split("<=")[0]
#                                     variable2 = cond2[k].split("=")[0]
#                                     # print(variable1)
#                                     # print(variable2)
#                                     if variable1 == variable2:
#                                         flag = 0
#                                     # print(flag)
#                                 elif ">" in cond1[k] and "<=" in cond2[k]:
#                                     variable1 = cond1[k].split(">")[0]
#                                     variable2 = cond2[k].split("<=")[1].split("<=")[0]
#                                     # print(variable1)
#                                     # print(variable2)
#                                     if variable1 == variable2:
#                                         flag = 0
#                                 elif "<=" in cond1[k] and ">" in cond2[k]:
#                                     variable1 = cond1[k].split("<=")[1].split("<=")
#                                     variable2 = cond2[k].split(">")[0]
#                                     print(variable1)
#                                     print(variable1)
#                                     if variable1 == variable2:
#                                         flag = 0
#                     else:
#                         continue
#                 # 如果没有找到该条件的分支
#                 if flag == 1:
#                     counterCondSet[cond1[k]] = t1
#
#                 else:
#                     break
#     print(counterCondSet)
#     forCompleteT = []  # 新加入的待推荐的迁移
#     if len(counterCondSet) > 0:
#         # print(counterCondSet)
#         countValue= 1
#         for key, value in counterCondSet.items():
#             # 需要补全的迁移及后续迁移
#             needChangeCond = key
#             newSatateLabel = ""
#             completeT = []
#             flag = 1
#             for j in range(0, len(T)):
#                 t = T[j][0]
#                 src = T[j][1]
#                 target = T[j][2]
#                 event = T[j][3].split("event=")[1]
#                 cond = T[j][4].split("condition=")[1]
#                 action = T[j][5].split("action=")[1]
#                 if t == value:
#                     src1 = "source:" + State2[src]
#                     target1 = "target:" + target + ":" + State2[target]
#                     # existKey = []
#                     # for index in StateSet.keys():
#                     #     existKey.append(index)
#                     # maxStateLabe = existKey[-1]
#                     event1 = "event:" + event
#                     cond1 = "condition:" + cond
#                     action1 = "action:" + action
#                     # print(event)
#                     # print(cond)
#                     completeT.append("Transition:")
#                     completeT.append(src1)
#                     completeT.append(event1)
#                     completeT.append(cond1)
#                     completeT.append(action1)
#                     completeT.append(target1)
#                     break
#             # print(completeT)
#             print("需要："+needChangeCond)
#             if "!=" in needChangeCond:
#                 newChangeCond = needChangeCond.split("!=")[0] + "=" + needChangeCond.split("!=")[1]
#             elif "<=" in needChangeCond:
#                 newChangeCond = needChangeCond.split("<=")
#                 # print(newChangeCond)
#                 if len(newChangeCond)==3:
#                     if newChangeCond[0]!='0':
#                         newChangeCond="("+newChangeCond[1]+"<"+newChangeCond[0]+") | ("+newChangeCond[1]+">"+newChangeCond[2]+")"
#                     else:
#                         newChangeCond = newChangeCond[1] + ">" +newChangeCond[2]
#                 else:
#                     newChangeCond = newChangeCond[0] + ">" + newChangeCond[1]
#             elif ">=" in needChangeCond:
#                 newChangeCond = needChangeCond.split(">=")[0] + "<" + needChangeCond.split(">=")[1]
#             elif "=" in needChangeCond:
#                 newChangeCond = needChangeCond.split("=")[0] + "!=" + needChangeCond.split("=")[1]
#             elif ">" in needChangeCond:
#                 newChangeCond = needChangeCond.split(">")[0] + "<" + needChangeCond.split(">")[1]
#             elif "<" in needChangeCond:
#                 newChangeCond = needChangeCond.split("<")[1]
#                 leftCond = needChangeCond.split("<")[0]
#                 if "<" in newChangeCond:
#                     var = newChangeCond.split("<")[0]
#                     varMaxVule = newChangeCond.split("<")[1]
#                     varMinValue = leftCond
#                     if varMaxVule != '0':
#                         newChangeCond = var + ">=" + varMaxVule
#                     else:
#                         newChangeCond = var + "<=" + varMinValue + "V" + var + ">=" + varMaxVule
#                     newChangeCond = var + "<=" + varMinValue + "," + var + ">=" + varMaxVule
#                 else:
#                     newChangeCond = leftCond + ">=" + newChangeCond
#             # print(newChangeCond)
#             # print(needChangeCond)
#
#             newCond = completeT[3].split(needChangeCond)[0] + newChangeCond + completeT[3].split(needChangeCond)[1]
#             print(newCond)
#             newSatateLabel = "S" + str(maxStateLabel+countValue)
#             newCond2 = newCond.split("condition:")[1]  # 推荐加入的对立分支条件
#             l=len(T)
#             maxTLabel=T[l-1][0].split("t")[1]
#             addT=[]
#             label = "t" + str(int(maxTLabel)+ countValue)
#             addT.append(label)
#             addT.append(src)
#             addT.append(newSatateLabel)
#             addevent = "event=" + event
#             addnewCond = "condition=" + newCond2
#             addaction = "action=null"
#             addT.append(addevent)
#             addnewCond2=addnewCond
#             print(addnewCond2)
#             if "," in addnewCond2:
#                 lastCond = addnewCond2.split("condition=")
#                 lastCond1 = lastCond[1].split(",")
#                 print(lastCond1)
#                 for j in range(0, len(lastCond1)):
#                     if "!=" not in lastCond1[j] and ">=" not in lastCond1[j] and "<=" not in lastCond1[j] and "=" in \
#                             lastCond1[j]:
#                         lastCond1[j] = lastCond1[j].replace("=", "==")
#                     if "<=" in lastCond1[j] and ") | (" not in lastCond1[j]:
#                         re = lastCond1[j].split("<=")
#                         # print(re)
#                         if len(re) > 2:
#                             lastCond1[j] = re[1] + ">=" + re[0] + ") & (" + re[1] + "<=" + re[2]
#                         else:
#                             lastCond1[j] = re[1] + "<=" + re[0]
#                     lastCond1[j] = "(" + lastCond1[j] + ")"
#                     print(lastCond1)
#                 addnewCond2= "condition=" + " & ".join(lastCond1)
#             else:
#                 lastCond = addnewCond2.split("condition=")
#                 # print(lastCond[1])
#                 if lastCond[1]:
#                     if "!=" not in lastCond[1] and ">=" not in lastCond[1] and "<=" not in lastCond[1] and "=" in \
#                             lastCond[1]:
#                         lastCond[1] = lastCond[1].replace("=", "==")
#                     if "<=" in lastCond[1]:
#                         re = lastCond[1].split("<=")
#                         # print(re)
#                         if len(re) > 2:
#                             lastCond[1] = "(" + re[1] + ">=" + re[0] + ") & (" + re[1] + "<=" + re[2] + ")"
#                         else:
#                             lastCond[1] ="("+re[0] + "<=" + re[1]+")"
#                     if ">=" in lastCond[1]:
#                         re = lastCond[1].split(">=")
#                         # print(re)
#                         lastCond[1] = "(" + re[0] + ">=" + re[1] + ")"
#                     if ">" in lastCond[1]:
#                         re = lastCond[1].split(">")
#                         # print(re)
#                         lastCond[1] = "(" + re[0] + ">" + re[1] + ")"
#                 addnewCond2= "condition=" + lastCond[1]
#             addT.append(addnewCond2)
#             addT.append(addaction)
#             forCompleteT.append(addT)
#             countValue+=1
#         print(forCompleteT)
#         savedStdout = sys.stdout  # 保存标准输出流
#         with open(filepath+'target2.txt', 'w+') as file:
#             sys.stdout = file  # 标准输出重定向至文件
#             for i in range(0,len(forCompleteT)):
#                 label=forCompleteT[i][0]
#                 src=forCompleteT[i][1]
#                 target=forCompleteT[i][2]
#                 event=forCompleteT[i][3].split("event=")[1]
#                 condition=forCompleteT[i][4].split("condition=")[1]
#                 action = forCompleteT[i][5].split("action=")[1]
#                 if event=="null":
#                     event=""
#                 if condition=="null":
#                     condition=""
#                 if action=="null":
#                     action=""
#                 print(label+", "+src+ ", " +target+ ", " + event + ", " + condition + ", " +action+",")
#         sys.stdout = savedStdout  # 恢复标准输出流
#     print(forCompleteT)
#     if len(forCompleteT)>0:
#         # 可行的迁移
#         feasibleT=[]
#         result = judgeFeasibility(filepath+"target2.txt",filepath+"resultModel2.txt")
#         print(result)
#         for i in range(0,len(result)):
#             if result[i][0]==1 and result[i][1]==1:#如果可行：
#                 feasibleT.append(forCompleteT[i])
#         print(feasibleT)
#         if (len(feasibleT)>0):
#             savedStdout = sys.stdout  # 保存标准输出流
#             with open(filepath+'outNew.txt', 'w+') as file:
#                 sys.stdout = file  # 标准输出重定向至文件
#                 print("N")
#                 # for key, value in State2.items():
#                 #     print(key + "->" + value)
#                 # print("推荐补全的迁移为:")
#                 for i in range(len(feasibleT)):
#                     # print("需要修改的条件所在的迁移为：")
#                     # print(completeT)
#                     # print("需要修改为其对立条件的条件分支:" + needChangeCond)
#                     print(feasibleT[i][0] + ", " + feasibleT[i][1] + ", " + feasibleT[i][2] + ", " + feasibleT[i][
#                         3] + ", " + feasibleT[i][4] + ", " + feasibleT[i][5])
#             sys.stdout = savedStdout  # 恢复标准输出流
#             counterCondSet.clear()
#         else:
#             print("模型完整")
#             savedStdout = sys.stdout  # 保存标准输出流
#             with open(filepath+'outNew.txt', 'w+') as file1:
#                 sys.stdout = file1  # 标准输出重定向至文件
#                 print("Y")
#                 # for key, value in State2.items():
#                 #     print(key + "->" + value)
#             sys.stdout = savedStdout  # 恢复标准输出流
#     else:
#         print("模型完整")
#         savedStdout = sys.stdout  # 保存标准输出流
#         with open(filepath+'outNew.txt', 'w+') as file1:
#             sys.stdout = file1  # 标准输出重定向至文件
#             print("Y")
#             # for key, value in State2.items():
#             #     print(key + "->" + value)
#         sys.stdout = savedStdout  # 恢复标准输出流
#     return counterCondSet
#
# incoding:utf-8
#State,初始状态集
# Trans,初始迁移集
# State2,合并后的状态集
# T，生成的模型
import copy
import sys

from lzy_Complete.Main import judgeFeasibility

writepath = './file/'
filepath = './file/'
def judgeModelComplete1():
    T = []
    name, src, tgt, event, condition, action = "", "", "", "", "",""
    cond2=""
    k = 0
    # 状态列表
    State2= {}
    T2=[]
    lines = open(filepath+'result.txt', 'r', encoding="utf-8").readlines()
    for line in lines:
        if line.strip() == "State:":  # ignore
            continue
        line = line.strip()
        if "label" in line:
            label= line.split("label=")[1]
        if "name" in line and "name=t" not in line:
            name= line.split("name=")[1]
            State2[label]=name
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
            # Trans.append(src)
        if "condition" in line:
            cond2=line
            cond=line.replace("==", "=")
            cond1= cond.split("condition=")[1]
            # print(cond1)
            if not cond1:
                condition="condition=null"
            else:
                condition= "condition="
                cond1=cond1.split(" & ")
                # print(cond1)
                condList=[]
                for i in range(0,len(cond1)):
                    item=cond1[i].split("(")[1].split(")")[0]
                    condList.append(item)
                # print(condList)
                l=len(condList)
                condList2=[]
                for i in range(0, l-1):
                    if ">=" in condList[i] and "<=" in condList[i+1]:
                        item1 = condList[i].split(">=")[0]
                        vaule1=condList[i].split(">=")[1]
                        item2 = condList[i+1].split("<=")[0]
                        vaule2 = condList[i+1].split("<=")[1]
                        if item1==item2:
                            item=vaule1+"<="+item1+"<="+vaule2
                            condList[i+1]=item
                        else:
                            item=condList[i]
                        condList2.append(item)
                    else:
                        item = condList[i]
                        if item not in condList2:
                            condList2.append(item)
                if ">=" in condList[l-2] and "<=" in condList[l-1]:
                    item1 = condList[l-2].split(">=")[0]
                    vaule1 = condList[l-2].split(">=")[1]
                    item2 = condList[l-1].split("<=")[0]
                    vaule2 = condList[l-1].split("<=")[1]
                    if item1 == item2:
                        item = vaule1 + "<=" + item1 + "<=" + vaule2
                    else:
                        item = condList[l-1]
                    if item not in condList:
                        condList2.append(item)
                else:
                    item = condList[l-1]
                    condList2.append(item)
                # print(condList2)
                l2=len(condList2)
                for i in range(0,l2-1) :
                    condition+=condList2[i]+","
                condition+=condList2[l2-1]
        if "action" in line:
            action =line
            # Trans.append(action)
            T.append([name, src, tgt, event, condition, action])
            T2.append([name, src, tgt, event, cond2, action])
            name,src, tgt, event, condition, action = "", "", "", "", "",""
            cond2=""
    print(State2)
    stateLabel = []
    for key in State2.keys():
        stateLabel.append(key)
    # print(stateLabel)
    maxStateLabel = 0 #计算当前状态标签的最大值
    for i in range(0, len(stateLabel)):
            item= int(stateLabel[i].split("S")[1])
            if maxStateLabel<int(item):
                maxStateLabel=item
    print(maxStateLabel)
    # print(T)
    # print(T2)
    newState = copy.deepcopy(State2)  # 将状态列表复制一份
    newState2 = {}
    for key, value in newState.items():
        if key == "S0":
            key = "START"
        newState2[key] = value
    print(newState2)
    for i in range(0,len(T2)):
        if T2[i][1] == "S0":
            T2[i][1] = "START"
        if T2[i][2] == "S0":
            T2[i][2] = "START"
    print(T2)
    # 输出成模型的标准形式，为后续可行性验证作准备
    savedStdout = sys.stdout  # 保存标准输出流
    with open(filepath+'resultModel2.txt', 'w+') as file:
        sys.stdout = file  # 标准输出重定向至文件
        for key, value in newState2.items():
            # print("State:\n\tlabel=" + key + '\n\t' + "name=" +value+ '\n')
            print("State:\n\tname=" + key)
        for i in range(0, len(T2)):
            print("Transition:\n\tname=" + T2[i][0] + '\n\tsrc=' + T2[i][1] + '\n\ttgt=' +
                  T2[i][2] + '\n\t' +
                  T2[i][3] + '\n\t' + T2[i][4] + '\n\t' + T2[i][5])
    sys.stdout = savedStdout  # 恢复标准输出流
    # 存储没有找到条件对立分支的条件及其所在迁移
    counterCondSet = {}
    # TBound={}#标记计数条件是否完整，0代表有下界 1代表有上界
    for i in range(0, len(T)):
        # # 存储没有找到条件对立分支的条件及其所在迁移
        # counterCondSet = {}
        t1 = T[i][0]
        src1 = T[i][1]
        tgt1 = T[i][2]
        event1 = T[i][3]
        cond1 = T[i][4].split("condition=")[1]
        if cond1 == "null":
            continue
        else:
            cond1 = cond1.split(",")
            l = len(cond1)
            for k in range(0, l):
                print("当前的条件为："+cond1[k])
                flag = 1
                # 寻找每一个条件的对立分支
                for j in range(0, len(T)):
                    t2 = T[j][0]
                    src2 = T[j][1]
                    tgt2 = T[j][2]
                    event2 = T[j][3]
                    cond2 = T[j][4].split("condition=")[1]
                    # print("寻找待匹配的条件："+cond2)
                    if t2 != t1:
                        if src2 == src1 and tgt2 != tgt1 and event2 == event1 and cond2 != "null":
                            cond2 = cond2.split(",")
                            # print(t1)
                            # print(t2)
                            # print(cond2[k])
                            # print(cond1[k])
                            # if cond1[0:k]==cond2[0:k]:
                            if "!=" in cond1[k] and "=" in cond2[k] and "!=" not in cond2[k] and "<=" not in cond2[
                                k] and ">=" not in cond2[k]:
                                variable1 = cond1[k].split("!=")
                                variable2 = cond2[k].split("=")
                                # print(variable1)
                                # print(variable2)
                                if variable1 == variable2 and cond1[0:k] == cond2[0:k]:
                                    flag = 0
                                    break
                            elif "!=" in cond2[k] and "=" in cond1[k] and "!=" not in cond1[k] and "<=" not in cond1[
                                k] and ">=" not in cond1[k]:
                                variable1 = cond1[k].split("=")
                                variable2 = cond2[k].split("!=")
                                # print(variable1)
                                # print(variable2)
                                if variable1 == variable2:
                                    flag = 0
                                    break
                            elif "=" in cond1[k] and "!=" not in cond1[k] and "<=" not in \
                                    cond1[k] and ">=" not in cond1[k] and "=" in cond2[k] and "!=" not in cond2[
                                k] and "<=" not in \
                                    cond2[k] and ">=" not in cond2[k]:
                                variable1 = cond1[k].split("=")
                                variable2 = cond2[k].split("=")
                                # print(variable1)
                                # print(variable2)
                                if variable1[0] == variable2[0] and cond1[0:k] == cond2[0:k]:
                                    flag = 0
                            elif "<=" in cond1[k] and ">" in cond2[k] and ">=" not in cond2[k]:
                                variable1 = cond1[k].split("<=")
                                variable2 = cond2[k].split(">")
                                # print(t1)
                                # print(t2)
                                # print(variable1)
                                # print(variable2)
                                if variable1 == variable2 and cond1[0:k] == cond2[0:k]:
                                    flag = 0
                                    break
                            elif "<=" in cond2[k] and ">" in cond1[k] and ">=" not in cond1[k]:
                                variable1 = cond1[k].split(">")
                                variable2 = cond2[k].split("<=")
                                # print(variable1)
                                # print(variable1)
                                if variable1== variable2 and cond1[0:k] == cond2[0:k]:
                                    flag = 0
                                    break
                            elif "<=" in cond2[k] and "=" in cond1[k] and ">=" not in cond1[k] and "!=" not in cond1[
                                k] and "<=" not in cond1[k]:
                                variable1 = cond1[k].split("=")[0]
                                value1 = cond1[k].split("=")[1]
                                listInequality = cond2[k].split("<=")
                                if len(listInequality) == 3:
                                    variable2 = listInequality[1]
                                    value2 = listInequality[-1]
                                    valueMin = listInequality[0]
                                    if variable1== variable2:
                                        flag = 0
                                        break
                                else:
                                    variable2 = listInequality[0]
                                    value2 = listInequality[-1]
                                    if variable1==variable2:
                                        flag = 0
                                        break
                                # print(variable2)
                                # print(value2)
                                # print(flag)
                            elif "<=" in cond1[k] and "=" in cond2[k] and ">=" not in cond2[k] and "!=" not in cond2[
                                k] and "<=" not in cond2[k]:
                                variable1 = cond2[k].split("=")[0]
                                # print(variable1)
                                value1 = cond2[k].split("=")[1]
                                # print(value1)
                                listInequality = cond1[k].split("<=")
                                # print(listInequality)
                                if len(listInequality) == 3:
                                    variable2 = listInequality[1]
                                    value2 = listInequality[-1]
                                    print(variable2)
                                    # print(value2)
                                    valueMin = listInequality[0]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                                else:
                                    variable2 = listInequality[0]
                                    value2 = listInequality[-1]
                                    if variable1 ==variable2:
                                        flag = 0
                                        break
                            elif ">" in cond1[k] and "<=" in cond2[k]:
                                variable1 = cond1[k].split(">")[0]
                                print(cond1)
                                print(variable1)
                                value1 = cond1[k].split(">")[1]
                                print(value1)
                                listInequality = cond2[k].split("<=")
                                if len(listInequality) == 3:
                                    variable2 = listInequality[1]
                                    value2 = listInequality[-1]
                                    valueMin = listInequality[0]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                                else:
                                    variable2 = listInequality[0]
                                    value2 = listInequality[-1]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                            elif "<=" in cond1[k] and ">" in cond2[k]:
                                variable1 = cond2[k].split(">")[0]
                                # print(variable1)
                                value1 = cond2[k].split(">")[1]
                                # print(value1)
                                listInequality = cond1[k].split("<=")
                                if len(listInequality) == 3:
                                    variable2 = listInequality[1]
                                    value2 = listInequality[-1]
                                    valueMin = listInequality[0]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                                else:
                                    variable2 = listInequality[0]
                                    value2 = listInequality[-1]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                            elif "<" in cond1[k] and "<=" in cond2[k]:
                                listInequality1 = cond1[k].split("<")
                                listInequality2 = cond2[k].split("<=")
                                if len(listInequality1) == 3 and len(listInequality2) == 3:
                                    variable1 = listInequality1[1]
                                    variable2 = listInequality2[1]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                                if len(listInequality1) == 3 and len(listInequality2) != 3:
                                    variable1 = listInequality1[1]
                                    variable2 = listInequality2[0]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                                if len(listInequality1) != 3 and len(listInequality2) == 3:
                                    variable1 = listInequality1[0]
                                    variable2 = listInequality2[1]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                            elif "<=" in cond1[k] and "<" in cond2[k]:
                                listInequality1 = cond2[k].split("<")
                                listInequality2 = cond1[k].split("<=")
                                if len(listInequality1) == 3 and len(listInequality2) == 3:
                                    variable1 = listInequality1[1]
                                    variable2 = listInequality2[1]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                                if len(listInequality1) == 3 and len(listInequality2) != 3:
                                    variable1 = listInequality1[1]
                                    variable2 = listInequality2[0]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                                if len(listInequality1) != 3 and len(listInequality2) == 3:
                                    variable1 = listInequality1[0]
                                    variable2 = listInequality2[1]
                                    if variable1 == variable2:
                                        flag = 0
                                        break
                                elif "<=" in cond1[k] and "<=" in cond2[k]:
                                    listInequality1 = cond1[k].split("<")
                                    listInequality2 = cond2[k].split("<=")
                                    if len(listInequality1) == 3 and len(listInequality2) == 3:
                                        variable1 = listInequality1[1]
                                        variable2 = listInequality2[1]
                                        if variable1 == variable2:
                                            flag = 0
                                            break
                                    if len(listInequality1) == 3 and len(listInequality2) != 3:
                                        variable1 = listInequality1[1]
                                        variable2 = listInequality2[0]
                                        if variable1 == variable2:
                                            flag = 0
                                            break
                                    if len(listInequality1) != 3 and len(listInequality2) == 3:
                                        variable1 = listInequality1[0]
                                        variable2 = listInequality2[1]
                                        if variable1 == variable2:
                                            flag = 0
                                            break
                                elif "<=" in cond1[k] and "<=" in cond2[k]:
                                    listInequality1 = cond2[k].split("<=")
                                    listInequality2 = cond1[k].split("<=")
                                    if len(listInequality1) == 3 and len(listInequality2) == 3:
                                        variable1 = listInequality1[1]
                                        variable2 = listInequality2[1]
                                        if variable1 == variable2:
                                            flag = 0
                                            break
                                    if len(listInequality1) == 3 and len(listInequality2) != 3:
                                        variable1 = listInequality1[1]
                                        variable2 = listInequality2[0]
                                        if variable1 == variable2:
                                            flag = 0
                                            break
                                    if len(listInequality1) != 3 and len(listInequality2) == 3:
                                        variable1 = listInequality1[0]
                                        variable2 = listInequality2[1]
                                        if variable1 == variable2:
                                            flag = 0
                                            break
                # 如果没有找到该条件的分支
                # print(flag)
                if flag == 1:
                    counterCondSet[cond1[k]]=t1
    print(counterCondSet)
    forCompleteT = []  # 新加入的待推荐的迁移
    if len(counterCondSet) > 0:
        # print(counterCondSet)
        countValue= 1
        for key, value in counterCondSet.items():
            # 需要补全的迁移及后续迁移
            needChangeCond = key
            newSatateLabel = ""
            completeT = []
            flag = 1
            for j in range(0, len(T)):
                t = T[j][0]
                src = T[j][1]
                target = T[j][2]
                event = T[j][3].split("event=")[1]
                cond = T[j][4].split("condition=")[1]
                action = T[j][5].split("action=")[1]
                if t == value:
                    src1 = "source:" + State2[src]
                    target1 = "target:" + target + ":" + State2[target]
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
                if len(newChangeCond)==3:
                    if newChangeCond[0]!='0':
                        newChangeCond="("+newChangeCond[1]+"<"+newChangeCond[0]+") | ("+newChangeCond[1]+">"+newChangeCond[2]+")"
                    else:
                        newChangeCond = newChangeCond[1] + ">" +newChangeCond[2]
                else:
                    newChangeCond = newChangeCond[0] + ">" + newChangeCond[1]
            elif ">=" in needChangeCond:
                newChangeCond = needChangeCond.split(">=")[0] + "<" + needChangeCond.split(">=")[1]
            elif "=" in needChangeCond:
                newChangeCond = needChangeCond.split("=")
                if newChangeCond[1].isdigit():
                    newChangeCond = "(" + newChangeCond[0] + "<" + newChangeCond[1] + ") | (" + newChangeCond[
                        0] + ">" + newChangeCond[1]+")"
                else:
                    newChangeCond = newChangeCond[0]+ "!=" + newChangeCond[1]
            elif ">" in needChangeCond:
                newChangeCond = needChangeCond.split(">")[0] + "<" + needChangeCond.split(">")[1]
            elif "<" in needChangeCond:
                newChangeCond = needChangeCond.split("<")[1]
                leftCond = needChangeCond.split("<")[0]
                if "<" in newChangeCond:
                    var = newChangeCond.split("<")[0]
                    varMaxVule = newChangeCond.split("<")[1]
                    varMinValue = leftCond
                    if varMaxVule != '0':
                        newChangeCond = var + ">=" + varMaxVule
                    else:
                        newChangeCond = var + "<=" + varMinValue + "|" + var + ">=" + varMaxVule
                    newChangeCond = var + "<=" + varMinValue + "," + var + ">=" + varMaxVule
                else:
                    newChangeCond = leftCond + ">=" + newChangeCond
            # print(newChangeCond)
            # print(needChangeCond)
            newCond = completeT[3].split(needChangeCond)[0] + newChangeCond + completeT[3].split(needChangeCond)[1]
            print("新构成的条件为："+newCond)
            newSatateLabel = "S" + str(maxStateLabel+countValue)
            newCond2 = newCond.split("condition:")[1]  # 推荐加入的对立分支条件
            l=len(T)
            maxTLabel=T[l-1][0].split("t")[1]
            addT=[]
            label = "t" + str(int(maxTLabel)+ countValue)
            addT.append(label)
            addT.append(src)
            addT.append(newSatateLabel)
            addevent = "event=" + event
            addnewCond = "condition=" + newCond2
            addaction = "action=null"
            addT.append(addevent)
            addnewCond2=addnewCond
            print(addnewCond2)
            if "," in addnewCond2:
                lastCond = addnewCond2.split("condition=")
                lastCond1 = lastCond[1].split(",")
                print(lastCond1)
                for j in range(0, len(lastCond1)):
                    if "!=" not in lastCond1[j] and ">=" not in lastCond1[j] and "<=" not in lastCond1[j] and "=" in \
                            lastCond1[j]:
                        lastCond1[j] = lastCond1[j].replace("=", "==")
                    if "<=" in lastCond1[j] and ") | (" not in lastCond1[j]:
                        re = lastCond1[j].split("<=")
                        # print(re)
                        if len(re) > 2:
                            lastCond1[j] = re[1] + ">=" + re[0] + ") & (" + re[1] + "<=" + re[2]
                        else:
                            lastCond1[j] = re[1] + "<=" + re[0]
                    lastCond1[j] = "(" + lastCond1[j] + ")"
                    print(lastCond1)
                addnewCond2= "condition=" + " & ".join(lastCond1)
            else:
                lastCond = addnewCond2.split("condition=")
                # print(lastCond[1])
                if lastCond[1]:
                    if "!=" not in lastCond[1] and ">=" not in lastCond[1] and "<=" not in lastCond[1] and "=" in \
                            lastCond[1]:
                        lastCond[1] = lastCond[1].replace("=", "==")
                    if "<=" in lastCond[1]:
                        re = lastCond[1].split("<=")
                        # print(re)
                        if len(re) > 2:
                            lastCond[1] = "(" + re[1] + ">=" + re[0] + ") & (" + re[1] + "<=" + re[2] + ")"
                        else:
                            lastCond[1] ="("+re[0] + "<=" + re[1]+")"
                    if ">=" in lastCond[1]:
                        re = lastCond[1].split(">=")
                        # print(re)
                        lastCond[1] = "(" + re[0] + ">=" + re[1] + ")"
                    if ">" in lastCond[1]:
                        re = lastCond[1].split(">")
                        # print(re)
                        lastCond[1] = "(" + re[0] + ">" + re[1] + ")"
                addnewCond2= "condition=" + lastCond[1]
            addT.append(addnewCond2)
            addT.append(addaction)
            forCompleteT.append(addT)
            countValue+=1
        print(forCompleteT)
        savedStdout = sys.stdout  # 保存标准输出流
        with open(filepath+'target2.txt', 'w+') as file:
            sys.stdout = file  # 标准输出重定向至文件
            for i in range(0,len(forCompleteT)):
                label=forCompleteT[i][0]
                src=forCompleteT[i][1]
                target=forCompleteT[i][2]
                event=forCompleteT[i][3].split("event=")[1]
                condition=forCompleteT[i][4].split("condition=")[1]
                action = forCompleteT[i][5].split("action=")[1]
                if event=="null":
                    event=""
                if condition=="null":
                    condition=""
                if action=="null":
                    action=""
                print(label+", "+src+ ", " +target+ ", " + event + ", " + condition + ", " +action+",")
        sys.stdout = savedStdout  # 恢复标准输出流
    print(forCompleteT)
    if len(forCompleteT)>0:
        # 可行的迁移
        feasibleT=[]
        result = judgeFeasibility(filepath+"target2.txt",filepath+"resultModel2.txt")
        print(result)
        for i in range(0,len(result)):
            if result[i][0]==1 and result[i][1]==1:#如果可行：
                feasibleT.append(forCompleteT[i])
        print(feasibleT)
        if (len(feasibleT)>0):
            savedStdout = sys.stdout  # 保存标准输出流
            with open(filepath+'outNew.txt', 'w+', encoding='utf-8') as file:
                sys.stdout = file  # 标准输出重定向至文件
                print("N")
                # for key, value in State2.items():
                #     print(key + "->" + value)
                # print("推荐补全的迁移为:")
                for i in range(len(feasibleT)):
                    # print("需要修改的条件所在的迁移为：")
                    # print(completeT)
                    # print("需要修改为其对立条件的条件分支:" + needChangeCond)
                    print(feasibleT[i][0] + ", " + feasibleT[i][1] + ", " + feasibleT[i][2] + ", " + feasibleT[i][
                        3] + ", " + feasibleT[i][4] + ", " + feasibleT[i][5])
            sys.stdout = savedStdout  # 恢复标准输出流
            counterCondSet.clear()

        else:
            print("模型完整")
            savedStdout = sys.stdout  # 保存标准输出流
            with open(filepath+'outNew.txt', 'w+') as file1:
                sys.stdout = file1  # 标准输出重定向至文件
                print("Y")
                # for key, value in State2.items():
                #     print(key + "->" + value)
            sys.stdout = savedStdout  # 恢复标准输出流
    else:
        print("模型完整")
        savedStdout = sys.stdout  # 保存标准输出流
        with open(filepath+'outNew.txt', 'w+') as file1:
            sys.stdout = file1  # 标准输出重定向至文件
            print("Y")
            # for key, value in State2.items():
            #     print(key + "->" + value)
        sys.stdout = savedStdout  # 恢复标准输出流
    return counterCondSet
if __name__ == '__main__':
    judgeModelComplete1()








