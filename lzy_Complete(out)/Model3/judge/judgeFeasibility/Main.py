# -*- coding: UTF-8 -*-

#主文件

import obtain_efsm_info
# from Model3.judgeFeasibility.forwardSearch import search
from obtain_efsm_info import sort, change, targetbranchlist,returnSM
import forwardSearch as sequeueGenerate
def judgeFeasibility():
    time1=0
    count=0
    time2=0
    number=0
    length=0
    select=0
    flag=0
    iteration=0
    while targetbranchlist and flag <= len(targetbranchlist):
        # 序列生成
        pathT = sequeueGenerate.search()
        time1 += sequeueGenerate.generationtime
        count += sequeueGenerate.successnumber
        number += sequeueGenerate.sequencenumber
        time2 += sequeueGenerate.generationsorttime
        iteration+=1
        print (pathT)
        if sequeueGenerate.sequencenumber == 0:
            flag += 1
            sort()
        else:
            flag = 0
            change()
    #print ("生成序列条数为%s" % number)
    judge=0
    if number!=0:
        SM = returnSM()
        judge = SM.testGen(pathT)
        path = SM.allPathNum()
        print(path)
    return number,judge
#判断是否有入度为0的节点
def judgeInDegreeisZero(SM):
    print(len(SM.transitionList))
    #入度为零的状态数
    inDegreeisZeroState = 0
    #print (SM.stateList)
    print('SM>')
    print(type(SM))
    
    for state in SM.stateList:
        flag = 0
        for trans in SM.transitionList:
            print ('trans',trans)
            if trans.tgt == state:
                flag = 1
                break
        if flag == 0:
            inDegreeisZeroState = 1
    return inDegreeisZeroState
if __name__ == '__main__':
    # judgeFeasibility()
    # print('11111')
    print(judgeInDegreeisZero())

