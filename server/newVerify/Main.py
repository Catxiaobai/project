# -*- coding: UTF-8 -*-

#主文件
import os
from newVerify import forwardSearch1 as sequeueGenerate
from newVerify import forwardSearch as sequeueGeneratemulti
import fileinput
from newVerify import obtain_efsm_info as obtain_efsm_info
from newVerify import EFSM
from newVerify import config

# def main():
#     time1 = 0
#     count = 0
#     time2 = 0
#     number = 0
#     length = 0
#     select = 0
#     flag = 0
#     iteration = 0
#     obtain_efsm_info.getSM()
#     obtain_efsm_info.getfailureList()
#     while obtain_efsm_info.targetbranchlist and flag <= len(obtain_efsm_info.targetbranchlist):
#         # 序列生成
#         pathT = sequeueGenerate.search()
#         time1 += sequeueGenerate.generationtime
#         count += sequeueGenerate.successnumber
#         number += sequeueGenerate.sequencenumber
#         time2 += sequeueGenerate.generationsorttime
#         length += sequeueGenerate.sequencelength
#         select += sequeueGenerate.selecenumber
#         iteration += 1
#
#         if sequeueGenerate.sequencenumber == 0:
#             flag += 1
#             obtain_efsm_info.sort()
#         else:
#             flag = 0
#             obtain_efsm_info.change()
#         if number != 0:
#             # filename = 'path.txt'
#             # with open(filename, 'w') as file_object:
#             #     path_num = []
#             #     for path in pathT:
#             #         path_num.append(int(path[1:]))
#             #     file_object.write(str(path_num))
#             SM = obtain_efsm_info.returnSM()
#             flag = SM.testGen(pathT)
#             if flag == 1:
#                 print ('生成迁移路径')
#             # path = SM.allPathNum()
#             print (pathT)
#
# if __name__ == '__main__':
#     main()


# 单条故障迁移
def onefailure():
    time1=0
    count=0
    time2=0
    number=0
    length=0
    select=0
    flag=0
    iteration=0
    # obtain_efsm_info.getSM()
    #obtain_efsm_info.getfailureList()
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
        print (pathT)

        if sequeueGenerate.sequencenumber == 0:
            flag += 1
            obtain_efsm_info.sort()
        else:
            flag = 0
            obtain_efsm_info.change()
        print ("生成序列条数为",number)
        if number!=0:
            SM = obtain_efsm_info.returnSM()
    if number == 0:
        return -1
    return pathT


# 多条故障迁移
def multifailure():
    time1=0
    count=0
    time2=0
    number=0
    length=0
    select=0
    flag=0
    iteration=0
    targetPath = list()
    uselist = []
    # obtain_efsm_info.getSM()
    #obtain_efsm_info.getfailureList()
    while obtain_efsm_info.targetbranchlist and flag <= len(obtain_efsm_info.targetbranchlist):
        # 序列生成
        pathT = sequeueGeneratemulti.search(uselist)
        time1 += sequeueGeneratemulti.generationtime
        count += sequeueGeneratemulti.successnumber
        number += sequeueGeneratemulti.sequencenumber
        time2 += sequeueGeneratemulti.generationsorttime
        length += sequeueGeneratemulti.sequencelength
        select += sequeueGeneratemulti.selecenumber
        iteration+=1

        if sequeueGeneratemulti.sequencenumber == 0:
            flag += 1
            obtain_efsm_info.sort()
        else:
            flag = 0
            obtain_efsm_info.change()
            path = pathT[0]
            path.extend(targetPath)
            targetPath = path
            uselist = pathT[1]

        if number != 0:
            SM = obtain_efsm_info.returnSM()

    if flag != 0:
        return -1
    return targetPath

def main():
    obtain_efsm_info.getSM()
    obtain_efsm_info.getfailureList()
    print(obtain_efsm_info.targetbranchlist)
    if (len(obtain_efsm_info.targetbranchlist) == 1):
        print("执行1")
        path = onefailure()
    elif (len(obtain_efsm_info.targetbranchlist) > 1):
        print("执行2")
        path = multifailure()

    if path != -1:
        filepath = './file/'
        filename = 'path.txt'
        with open(filepath+filename, 'w') as file_object:
            path_num = []
            for pathT in path:
                path_num.append(int(pathT[1:]))
            file_object.write(str(path_num))
        SM = obtain_efsm_info.returnSM()
        flag = SM.testGen(path)

















