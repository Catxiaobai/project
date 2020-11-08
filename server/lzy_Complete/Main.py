# -*- coding: UTF-8 -*-

#主文件
# from Model5.judgeFeasibility.forwardSearch import search
from lzy_Complete.EFSM import efsmFromFile
from lzy_Complete.obtain_efsm_info import targetbranchlist, returnSM, change, targetDeal
import lzy_Complete.forwardSearch as sequeueGenerate
def judgeFeasibility(inputfile1,inputfile2):
    result=[]
    time1=0
    count=0
    time2=0
    number=0
    length=0
    select=0
    flag=0
    iteration=0
    targetDeal(inputfile1)
    while targetbranchlist and flag <= len(targetbranchlist):
        # 序列生成
        pathT = sequeueGenerate.search()
        time1 += sequeueGenerate.generationtime
        count += sequeueGenerate.successnumber
        number += sequeueGenerate.sequencenumber
        time2 += sequeueGenerate.generationsorttime
        iteration+=1
        print ('path=',pathT)
        if sequeueGenerate.sequencenumber == 0:
            flag += 1
            # sort()
            change()
            result.append([0,0])
        else:
            flag = 0
            change()
            # SM=returnSM()
            # judge = SM.testGen(pathT)
            oriModel = efsmFromFile(inputfile2)
            # print(oriModel.allPathNum())
            # print(oriModel.testGen(pathT))
            judge = oriModel.testGen(pathT)
            # judge=SM.testGen(pathT)
            if judge==1:
                result.append([1, 1])
            else:
                result.append([1, 0])

    print ("生成序列条数为%s" % number)
    # # judge=0
    # # if number!=0:
    # #     SM = returnSM()
    # #     judge = SM.testGen(pathT)
    # #     path = SM.allPathNum()
    # #     print(judge)
    # print(result)
    return result
#判断是否有入度为0的节点 有返回0，没有返回1
def judgeInDegreeisZero(inputefile):
    oriModel = efsmFromFile(inputefile)
    #入度为零的状态数
    inDegreeisZeroState = 0
    # print (SM.stateList)
    # print SM.transitionList
    for state in oriModel.stateList:
        flag = 0
        for trans in oriModel.transitionList:
            if trans.tgt == state:
                flag = 1
                break
        if flag == 0:
            inDegreeisZeroState = 1
    return inDegreeisZeroState
if __name__ == '__main__':
    # judgeFeasibility()
    print('11111')
    print(judgeFeasibility("failureTran/target1.txt","model/resultModel.txt"))
    # SM = returnSM()
    #  print(judgeInDegreeisZero("resultModel3.txt"))

