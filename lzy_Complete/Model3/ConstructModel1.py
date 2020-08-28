#incoding:UTF-8
import copy
import json
import copy
import sys
import json
import numpy as np
from graphviz import Digraph
#获取状态集跟迁移集
sys.path.append("")
writepath = r''
filepath = r''
filename1 = "Trace1.txt"
filename2 = r'result1'
def getTransState1():
    lines = open(filename1, 'r', encoding="utf-8").readlines()
    states_label = []
    source, event, condition, action, target = "", "", "", "", ""
    # 迁移列表
    TransSet = []
    count = 0
    k = 0
    # 状态列表
    StateSet = {}
    #Trace集合
    TraceSet=[]
    for line in lines:
        if line.strip() == "Trace:":# ignore
            Trace=[]
            Trace.append("Trace:")
            continue
        line = line.strip()
        fileds = line.split(':', 1)
        if fileds[0] == "source":
            Trace.append(line)
            source = fileds[1].split(":")[1]
            label = fileds[1].split(":")[0]
            if label not in states_label:
                states_label.append(label)
                StateSet[label] = source
                k += 1
        elif fileds[0] == 'event':
            Trace.append(line)
            event = "event=" + fileds[1]
        elif fileds[0] == 'condition':
            Trace.append(line)
            condition = "condition=" + fileds[1]
        elif fileds[0] == 'action':
            Trace.append(line)
            action = "action=" + fileds[1]
        elif fileds[0] == 'target':
            Trace.append(line)
            target = fileds[1].split(":")[1]
            label = fileds[1].split(":")[0]
            if label not in states_label:
                states_label.append(label)
                StateSet[label] = target
                k = k + 1
            count += 1
            TransLable = "T" + str(count)
            TransSet.append([TransLable, states_label[k - 2], states_label[k - 1], event, condition, action])
            source, event, condition, action, target = "", "", "", "", ""
            if Trace not in TransSet:
                TraceSet.append(Trace)
    output = open('TraceSet.txt', 'w+')
    for i in range(len(TraceSet)):
        for j in range(len(TraceSet[i])):
            output.write(str(TraceSet[i][j]))
            output.write(' ')
        output.write('\n')
    output.close()
    with open('StateSet.txt', 'w') as f:
        json_str = json.dumps(StateSet, ensure_ascii=False, indent=0)
        f.write(json_str)
        f.write('\n')
    output = open('TransSet.txt', 'w+')
    for i in range(len(TransSet)):
        for j in range(len(TransSet[i])):
            output.write(str(TransSet[i][j]))
            output.write(' ')
        output.write('\n')
    output.close()
    return TraceSet,StateSet,TransSet
def ConstructModel1():
    TraceSet,StateSet,TransSet=getTransState1()
    Tr = copy.deepcopy(TransSet)
    # 去除state字典中的值重复项
    func = lambda State: dict([(x, y) for y, x in State.items()])
    State2 = func(func(StateSet))
    # 修改状态编号使状态编号较小
    State3 = {}
    i = 0
    s = ""
    for value in State2.values():
        s = "S" + str(i)
        State3[value] = s
        i += 1
    with open('S1.txt', 'w') as f:
        json_str = json.dumps(State3, ensure_ascii=False, indent=0)
        f.write(json_str)
        f.write('\n')
    # 获得标号-》名称一一对应
    State4 = {}
    for key, value in State3.items():
        State4[value] = key
    with open('S2.txt', 'w') as f:
        json_str = json.dumps(State4, ensure_ascii=False, indent=0)
        f.write(json_str)
        f.write('\n')
    # 合并迁移中状态相等的
    for k in range(0, len(Tr) - 1):
        m = Tr[k][1]
        n = Tr[k][2]
        for i in range(k + 1, len(Tr)):
            if StateSet[m] == StateSet[Tr[i][1]]:
                Tr[i][1] = m
            if StateSet[m] == StateSet[Tr[i][2]]:
                Tr[i][2] = m
            if StateSet[n] == StateSet[Tr[i][1]]:
                Tr[i][1] = n
            if StateSet[n] == StateSet[Tr[i][2]]:
                Tr[i][2] = n
    # output = open('T2.txt', 'w+')
    # for i in range(len(Tr)):
    #     for j in range(len(Tr[i])):
    #         output.write(str(Tr[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    # 修改迁移中的状态标号使其标号为小标号
    for k in range(0, len(Tr)):
        m = Tr[k][1]
        n = Tr[k][2]
        Tr[k][1] = State3[StateSet[m]]
        Tr[k][2] = State3[StateSet[n]]
    # output = open('T3.txt', 'w+')
    # for i in range(len(Tr)):
    #     for j in range(len(Tr[i])):
    #         output.write(str(Tr[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    # # 识别各个元素相同的迁移并标识为相同的编号
    for i in range(0, len(Tr) - 1):
        t = Tr[i][0]
        src1 = Tr[i][1]
        tgt1 = Tr[i][2]
        event1 = Tr[i][3]
        cond1 = Tr[i][4]
        action1 = Tr[i][5]
        for j in range(i + 1, len(Tr)):
            if src1 == Tr[j][1] and tgt1 == Tr[j][2] and event1 == Tr[j][3] and cond1==Tr[j][4] and action1 == Tr[j][5]:
                    Tr[j][0] = t
    # output = open('T4.txt', 'w+')
    # for i in range(len(Tr)):
    #     for j in range(len(Tr[i])):
    #         output.write(str(Tr[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    # 去除迁移列表中的重复迁移
    T2 = np.array(Tr)
    list3 = np.array(list(set([tuple(t) for t in T2])))
    k = 1
    Trans2 = []
    for i in list3:
        list3 = list(i)
        k += 1
        Trans2.append(list3)
    # output = open('T5.txt', 'w+')
    # for i in range(len(Trans2)):
    #     for j in range(len(Trans2[i])):
    #         output.write(str(Trans2[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    Trans2.sort()
    # output = open('T6.txt', 'w+')
    # for i in range(len(Trans2)):
    #     for j in range(len(Trans2[i])):
    #         output.write(str(Trans2[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    # 将输入密码次数不同，其余均相同的标为同一条迁移，以便合并
    sameTLabel = []
    sameT = []
    for i in range(0, len(Trans2) - 1):
        t = Trans2[i][0]
        src1 = Trans2[i][1]
        tgt1 = Trans2[i][2]
        event1 = Trans2[i][3]
        cond1 = Trans2[i][4]
        action1 = Trans2[i][5]
        for j in range(i + 1, len(Trans2)):
            if src1 == Trans2[j][1] and tgt1 == Trans2[j][2] and event1 == Trans2[j][3] and action1 == Trans2[j][5]:
                Trans2[j][0] = t
                sameTLabel.append(t)
                if Trans2[i] not in sameT:
                    sameT.append(Trans2[i])
                if Trans2[j] not in sameT:
                    sameT.append(Trans2[j])
    sameTLabel = list(set(sameTLabel))
    # print(sameTLabel)
    # print(sameT)
    # 将标号不同的迁移从1标号并加入到1
    T1 = []
    j = 1
    for i in range(0, len(Trans2)):
        t = Trans2[i][0]
        if t not in sameTLabel:
            Trans2[i][0] = "t" + str(j)
            T1.append(Trans2[i])
            j += 1
    # output = open('T7.txt', 'w+')
    # for i in range(len(T1)):
    #     for j in range(len(T1[i])):
    #         output.write(str(T1[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    # 合并相同标号的迁移 ，合并尝试密码的次数
    i = 0
    mergeCond = []
    mergeT = []
    while i < len(sameT) - 1:
        t = sameT[i][0]
        cond1 = sameT[i][4]
        mergeT.append(sameT[i])
        if "attempts=" in cond1:
            numAttempts1 = int(cond1.split("attempts=")[1])
            minN = maxN = numAttempts1
            j = i + 1
            while j < len(sameT):
                if sameT[j][0] == t:
                    cond2 = sameT[j][4]
                    # condition = p != pin, attempts=0
                    # condition = p != pin, attempts=1
                    if "attempts=" in cond2:
                        numAttempts2 = int(cond2.split("attempts=")[1])
                        if minN > numAttempts2:
                            minN = numAttempts2
                        if maxN < numAttempts2:
                            maxN = numAttempts2
                    j += 1
                else:
                    break
            mergeCondition = cond1.split("attempts=")[0] + str(minN) + "<=attempts<=" + str(maxN)
            # print(mergeCondition)
            mergeCond.append(mergeCondition)
        i = j
    # print(mergeCond)
    # print(mergeT)
    # 合并尝试密码次数,并加入模型迁移集：
    k = len(T1)
    for i in range(0, len(mergeT)):
           mergeSame = []
           src1 = mergeT[i][1]
           tgt1 = mergeT[i][2]
           event1 = mergeT[i][3]
           action1 = mergeT[i][5]
           t = "t" + str(k + 1)
           mergeSame.append(t)
           mergeSame.append(src1)
           mergeSame.append(tgt1)
           mergeSame.append(event1)
           mergeSame.append(mergeCond[i])
           mergeSame.append(action1)
           # print(mergeSame)
           T1.append(mergeSame)
           k += 1
    output = open('T8.txt', 'w+')
    for i in range(len(T1)):
        for j in range(len(T1[i])):
            output.write(str(T1[i][j]))
            output.write(' ')
        output.write('\n')
    output.close()
    # 画图
    # with open(r"" + writepath + filename2 + '.dot', 'w+') as fout:
    #     fout.writelines("digraph g {\n")
    #     st = list()
    #     for i in range(0, len(T1)):
    #         name = T1[i][0]
    #         src = T1[i][1]
    #         tgt = T1[i][2]
    #         event = T1[i][3]
    #         cond = T1[i][4]
    #         action = T1[i][5]
    #         fout.writelines(" " + src + " -> " + tgt + ' [ label="' + name)
    #         if event != None:
    #             fout.writelines('\n' + event)
    #         if cond != None:
    #             fout.writelines('\n' + cond)
    #         # if action!= None:
    #         #     fout.writelines('\n' + action)
    #         fout.writelines('" ];\n')
    #         if src not in st:
    #             st.append(src)
    #             print(src + "->" + State4[src])
    #     fout.writelines("}\n")
    # os.popen("dot -Tpng {}.dot -o {}.png".format(filename2, filename2))
    f = Digraph('digraph g', filename="efsm1.gv")
    s=""
    for i in range(0, len(T1)):
        src = T1[i][1]
        if src== "S0":
            s=src
    f.attr('node', shape='doublecircle')
    f.node(s)
    f.attr('node', shape='circle')
    st=list()
    for i in range(0, len(T1)):
        name = T1[i][0]
        src = T1[i][1]
        tgt = T1[i][2]
        event = T1[i][3]
        cond = T1[i][4]
        action = T1[i][5]
        if src not in st:
            st.append(src)
            print(src + "->" + State4[src])
        f.edge(src, tgt, label=event + '\n' + cond + '\n' + action)
    f.view()
    return TraceSet,StateSet,TransSet,State4,T1