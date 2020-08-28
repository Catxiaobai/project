# incoding:utf-8
#State,初始状态集
# Trans,初始迁移集
# State2,合并后的状态集
# T，生成的模型
import os
import sys

from Model3.ConstructModel1 import ConstructModel1

sys.path.append("")
writepath = r''
filepath = r''
import fp as fp
def completeModel1(State2,counterCondSet):
    # print(counterCondSet)
    if len(counterCondSet) > 0:
        if not os.path.isfile("addTrace.txt"):
            # 从键盘输入trace并保存到数组中
            print("模型不完整，请补全：")
            # 从键盘输入并存入addTrace.txt
            newTrace = []
            for line in iter(input, ''):
                newTrace.append(line)
            output = open('addTrace.txt', 'w+')
            for item in newTrace:
                output.write(item)
                output.write('\n')
            output.close()
            # 从用户添加的文件中读取trace
            filename1 = "addTrace.txt"
            lines = open(filename1, 'r', encoding="utf-8").readlines()
            newTrace2 = []
            for line in lines:
                if line.strip() == "Trace:":  # ignore
                    newTrace2.append("Trace:")
                    continue
                line = line.strip()
                fileds = line.split(':', 1)
                if fileds[0] == "source":
                    newTrace2.append(line)
                elif fileds[0] == 'event':
                    newTrace2.append(line)
                elif fileds[0] == 'condition':
                    newTrace2.append(line)
                elif fileds[0] == 'action':
                    newTrace2.append(line)
                elif fileds[0] == 'target':
                    newTrace2.append(line)
            with open('Trace1.txt', 'a', encoding='utf-8') as f:
                f.write('\n')
                for item in newTrace2:
                    f.write(item + " " + "\n")
            f.close()
            TraceSet, State, Trans, State2, T = ConstructModel1()
        elif os.path.isfile("addTrace.txt") and not os.path.getsize('addTrace.txt'):
            print("请向文件添加入Trace：")
            # 从键盘输入并存入addTrace.txt
            newTrace = []
            for line in iter(input, ''):
                newTrace.append(line)
            print(newTrace)
            output = open('addTrace.txt', 'a+')
            for item in newTrace:
                output.write(item)
                output.write('\n')
            output.close()
            # 从用户添加的文件中读取trace
            filename1 = "addTrace.txt"
            lines = open(filename1, 'r', encoding="utf-8").readlines()
            newTrace2 = []
            for line in lines:
                if line.strip() == "Trace:":  # ignore
                    newTrace2.append("Trace:")
                    continue
                line = line.strip()
                fileds = line.split(':', 1)
                if fileds[0] == "source":
                    newTrace2.append(line)
                elif fileds[0] == 'event':
                    newTrace2.append(line)
                elif fileds[0] == 'condition':
                    newTrace2.append(line)
                elif fileds[0] == 'action':
                    newTrace2.append(line)
                elif fileds[0] == 'target':
                    newTrace2.append(line)
            with open('Trace1.txt', 'a', encoding='utf-8') as f:
                f.write('\n')
                for item in newTrace2:
                    f.write(item + " " + "\n")
            f.close()
            TraceSet, State, Trans, State2, T = ConstructModel1()
        elif os.path.isfile("addTrace.txt") and os.path.getsize('addTrace.txt'):
            # 从用户添加的文件中读取trace
            sys.path.append("")
            writepath = r''
            filepath = r''
            filename1 = "addTrace.txt"
            lines = open(filename1, 'r', encoding="gbk").readlines()
            newTrace2 = []
            for line in lines:
                if line.strip() == "Trace:":  # ignore
                    newTrace2.append("Trace:")
                    continue
                line = line.strip()
                fileds = line.split(':', 1)
                if fileds[0] == "source":
                    newTrace2.append(line)
                elif fileds[0] == 'event':
                    newTrace2.append(line)
                elif fileds[0] == 'condition':
                    newTrace2.append(line)
                elif fileds[0] == 'action':
                    newTrace2.append(line)
                elif fileds[0] == 'target':
                    newTrace2.append(line)
            with open('Trace1.txt', 'a', encoding='utf-8') as f:
                f.write('\n')
                for item in newTrace2:
                    f.write(item + " " + "\n")
                    # f.write('\n')
            f.close()
            TraceSet, StateSet, TransSet, State2, T = ConstructModel1()
