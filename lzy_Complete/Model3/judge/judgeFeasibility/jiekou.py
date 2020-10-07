import re
import json
from judgeResult import judegeDelete,judegeAdd
def json_node():
    data = []
    with open('1.json') as f:
        for line in f:
            data.append(json.loads(line))
    #数据格式修改
    string = str(data)
    string = string.replace('[','').replace(']','').replace('},','}\n').replace('{','').replace('}','').replace(',','\n')
    #print(string)
    data_nodename = []
    with open('test.txt', 'w') as fp:
        fp.write(string)

    lines = open('test.txt', 'r', encoding='gbk').readlines()
    index_line = 0
    node_sum = 0
    while index_line < len(lines):
        if lines[index_line].strip() .split(':')[0]== "'id'":
            node_num = lines[index_line].strip().split(':')[1]
            data_nodename.append(node_num)
            node_sum +=1
        index_line += 1
    #print(node_sum)
    with open('test1.txt','w') as fp:
        i=0
        while i<node_sum:
            fp.write("State:"+"\n")
            data_nodename[i].strip()
            t = "name=S"+data_nodename[i]
            t="".join(t.split())
            #print(t)
            fp.write("\t"+t+"\n")
            i +=1


data = []
with open('2.json') as f:
    for line in f:
        data.append(json.loads(line))
# 数据格式修改
string = str(data)
#print(data)
string = string.replace('[', '').replace(']', '').replace('},', '}\n').replace('{', '').replace('}', '').replace("',","'\n")

print(string)
# data_nodename = []
# with open('test.txt', 'w') as fp:
#     fp.write(string)
#
# lines = open('test.txt', 'r', encoding='gbk').readlines()
# index_line = 0
# node_sum = 0
# while index_line < len(lines):
#     if lines[index_line].strip().split(':')[0] == "'id'":
#         node_num = lines[index_line].strip().split(':')[1]
#         data_nodename.append(node_num)
#         node_sum += 1
#     index_line += 1
# # print(node_sum)
# with open('test1.txt', 'w') as fp:
#     i = 0
#     while i < node_sum:
#         fp.write("State:" + "\n")
#         data_nodename[i].strip()
#         t = "name=S" + data_nodename[i]
#         t = "".join(t.split())
#         # print(t)
#         fp.write("\t" + t + "\n")
#         i += 1
