# -*- coding: utf-8 -*-
import json
import codecs
import re

filepath = r'E:/Code/project301/file/'
wf = codecs.open(filepath+"result.txt", 'w', encoding ="utf-8")
state = dict(json.load(open(filepath+"S2.txt", 'r', encoding ="gbk")))

for key in sorted(state.keys(), key=lambda x: int(x[1:])):
    wf.write("State:\n\tlabel="+key+'\n\t'+"name="+state[key]+'\n')

details = codecs.open(filepath+"T6.txt", 'r', encoding ="utf-8").readlines()
for line in details:
    fields = line.split(";", 5)
    if fields[4].strip().split('=')[1] == "null":
        fields[4] ="condition="
    else:
        lastCond = fields[4].strip().split('=',1)[1]
        lastCond1 = lastCond.strip().split(',')
        #num_con = len(con)
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
            #print(lastCond1)
        fields[4]= "condition=" + " & ".join(lastCond1)
    fields[5] = fields[5].replace(',',';')
    wf.write("Transition:\n\tname="+fields[0]+'\n\tsrc='+fields[1]+'\n\ttgt='+fields[2]+'\n\t'+fields[3]+'\n\t'+fields[4]+'\n\t'+fields[5])
wf.close()