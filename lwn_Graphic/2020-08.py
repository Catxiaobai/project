# -*- coding: utf-8 -*-
import json
import codecs

filepath = r'E:/Code/project301/file/'

wf = codecs.open(filepath+"2020-result.txt", 'w', encoding="utf-8")
state = dict(json.load(open(filepath+"S2.txt", 'r')))

for key in sorted(state.keys(), key=lambda x: int(x[1:])):
    wf.write("State:\n\tlabel="+key+'\n\t'+"name="+state[key]+'\n')

details = codecs.open(filepath+"T8.txt", 'r', encoding="utf-8").readlines()
for line in details:
    fields = line.split(" ", 5)
    wf.write("Transition:\n\t\tname="+fields[0]+'\n\t\tsrc='+fields[1]+'\n\t\ttgt='+fields[2]+'\n\t\t'+fields[3]+'\n\t\t'+fields[4]+'\n\t\t'+fields[5])
wf.close()