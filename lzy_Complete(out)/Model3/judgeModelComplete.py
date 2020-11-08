# incoding:utf-8
#State,初始状态集
# Trans,初始迁移集
# State2,合并后的状态集
# T，生成的模型
import os
import sys

from ConstructModel1 import ConstructModel1

sys.path.append("")
writepath = r'E:/Code/project301/file/'
filepath = r'E:/Code/project301/file/'
import fp as fp
def judgeModelComplete1():
        # print(T)
        # print(TraceSet[0])
        # 存储没有找到条件对立分支的条件及其所在迁移
    TraceSet, StateSet, TransSet, State2, T = ConstructModel1()
    counterCondSet = {}
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
            for k in range(0, len(cond1)):
                flag = 1
                # 寻找每一个条件的对立分支
                for j in range(0, len(T)):
                    t2 = T[j][0]
                    src2 = T[j][1]
                    tgt2 = T[j][2]
                    event2 = T[j][3]
                    cond2 = T[j][4].split("condition=")[1]
                    if t2 != t1:
                        if src2 == src1 and tgt2 != tgt1 and event2 == event1 and cond2 != "null":
                            cond2 = cond2.split(",")
                            # print(t1)
                            # print(t2)
                            # print(cond1)
                            # print(cond2)
                            count = 0
                            if k == 0:
                                count = 0
                            else:
                                for n in range(0, k):
                                    if cond1[n] == cond2[n]:
                                        count += 1
                            if count == k:
                                if "!=" in cond1[k] and "=" in cond2[k]:
                                    variable1 = cond1[k].split("!=")
                                    variable2 = cond2[k].split("=")
                                    # print(variable1)
                                    # print(variable1)
                                    if variable1 == variable2:
                                        flag = 0
                                elif "!=" in cond2[k] and "=" in cond1[k]:
                                    variable1 = cond1[k].split("=")
                                    variable2 = cond2[k].split("!=")
                                    # print(variable1)
                                    # print(variable1)
                                    if variable1 == variable2:
                                        flag = 0
                                elif "<=" in cond1[k] and ">" in cond2[k]:
                                    variable1 = cond1[k].split("<=")
                                    variable2 = cond2[k].split(">")
                                    # print(t1)
                                    # print(t2)
                                    # print(variable1)
                                    # print(variable1)
                                    if variable1 == variable2:
                                        flag = 0
                                elif "<=" in cond2[k] and ">" in cond1[k]:
                                    variable1 = cond1[k].split(">")
                                    variable2 = cond2[k].split("<=")
                                    # print(variable1)
                                    # print(variable1)
                                    if variable1 == variable2:
                                        flag = 0
                                elif "=" in cond1[k] and "<=" in cond2[k]:
                                    variable1 = cond1[k].split("=")[0]
                                    variable2 = cond2[k].split("<=")[1].split("<=")[0]
                                    # print(variable1)
                                    # print(variable1)
                                    if variable1 == variable2:
                                        flag = 0
                                    # print(flag)
                                elif "=" in cond2[k] and "<=" in cond1[k]:
                                    variable1 = cond1[k].split("<=")[1].split("<=")[0]
                                    variable2 = cond2[k].split("=")[0]
                                    # print(variable1)
                                    # print(variable2)
                                    if variable1 == variable2:
                                        flag = 0
                                    # print(flag)
                                elif ">" in cond1[k] and "<=" in cond2[k]:
                                    variable1 = cond1[k].split(">")[0]
                                    variable2 = cond2[k].split("<=")[1].split("<=")[0]
                                    # print(variable1)
                                    # print(variable2)
                                    if variable1 == variable2:
                                        flag = 0
                                elif "<=" in cond1[k] and ">" in cond2[k]:
                                    variable1 = cond1[k].split("<=")[1].split("<=")
                                    variable2 = cond2[k].split(">")[0]
                                    print(variable1)
                                    print(variable1)
                                    if variable1 == variable2:
                                        flag = 0
                    else:
                        continue
                # 如果没有找到该条件的分支
                if flag == 1:
                    counterCondSet[cond1[k]] = t1

                else:
                    break
    if len(counterCondSet) > 0:
        # print(counterCondSet)
        for key, value in counterCondSet.items():
            # 需要补全的迁移及后续迁移
            completeT = []
            for j in range(0, len(T)):
                t = T[j][0]
                src = T[j][1]
                event = T[j][3].split("event=")[1]
                cond = T[j][4].split("condition=")[1]
                if t == value:
                    src = "source:" + State2[src]
                    existKey = []
                    for index in StateSet.keys():
                        existKey.append(index)
                    maxStateLabe = existKey[-1]
                    # print(maxStateLabe)
                    event = "event:" + event
                    cond = "condition:" + cond
                    # print(event)
                    # print(cond)
                    traceSample = None
                    for k in range(0, len(TraceSet)):
                        if event in TraceSet[k] and cond in TraceSet[k]:
                            traceSample = TraceSet[k]
                            break
                    # print(traceSample)
                    completeT.append(src)
                    completeT.append(event)
                    print("模型不完整")
                    savedStdout = sys.stdout  # 保存标准输出流
                    with open(filepath+'out.txt', 'w+') as file:
                        sys.stdout = file  # 标准输出重定向至文件
                        print("N")
                        print("模型不完整，请补全：")
                        for key, value in State2.items():
                            print(key + "->" + value)
                        print(completeT)
                        print("原Trace集中最大的状态节点编号:" + str(maxStateLabe))
                        print("原来的condition:" + cond)
                        print("需要修改为其对立条件的条件分支:")
                        print("需要修改条件的迁移所在的Trace示例:")
                        for item in traceSample:
                            print(item)
                        print('')
                        print("请按照Trace示例从最大状态节点编号之后编号，并从需要修改为其对立条件的Condition处修改Trace示例，补全Trace：")
                    sys.stdout = savedStdout  # 恢复标准输出流
    else:
        print("模型完整")
        savedStdout = sys.stdout  # 保存标准输出流
        with open(filepath+'out.txt', 'w+') as file:
            sys.stdout = file  # 标准输出重定向至文件
            print("Y")
            print("模型完整")
            for key, value in State2.items():
                print(key + "->" + value)
        sys.stdout = savedStdout  # 恢复标准输出流
    return State2, counterCondSet

if __name__ == '__main__':
    judgeModelComplete1()








