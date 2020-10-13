# -*- coding: UTF-8 -*-

#主文件
import os
import forwardSearch as sequeueGenerate
import fileinput
import obtain_efsm_info as obtain_efsm_info
import EFSM
import config
time1=0
count=0
time2=0
number=0
length=0
select=0
flag=0
iteration=0
while obtain_efsm_info.targetbranchlist and flag <= len(obtain_efsm_info.targetbranchlist):
    # 序列生成
    pathT = sequeueGenerate.search()
    time1 += sequeueGenerate.generationtime
    count += sequeueGenerate.successnumber
    number += sequeueGenerate.sequencenumber
    time2 += sequeueGenerate.generationsorttime
    length += sequeueGenerate.sequencelength
    select += sequeueGenerate.selecenumber
    iteration+=1
    print pathT

    if sequeueGenerate.sequencenumber == 0:
        flag += 1
        obtain_efsm_info.sort()
    else:
        flag = 0
        obtain_efsm_info.change()



print "生成序列条数为%s" % number
if number!=0:

    SM = obtain_efsm_info.returnSM()
    SM.testGen(pathT)
    # path = SM.allPathNum()
    # print path









