# encoding:UTF-8
import os
import shutil
import sys

from numpy import double

from Main import judgeFeasibility, judgeInDegreeisZero
from obtain_efsm_info import returnSM
from EFSM import efsmFromFile
filepath = 'E:/Code/project301/file/'
filename=filepath+"resultModel2.txt"
# def judegeAdd():
#     number, judge = judgeFeasibility()  # number,judge分别表示测试序列的数量和测试数据是否生成
#     SM = returnSM()
#     inDegreeisZeroState = judgeInDegreeisZero(SM)  # 表示入度为0的状态数
#     #savedStdout = sys.stdout  # 保存标准输出流
#     #with open('judgeResult.txt', 'w+') as file:
#         #sys.stdout = file  # 标准输出重定向至文件
#     if inDegreeisZeroState==1: #如果加入之后是有入度为0的迁移（加入一条孤立的迁移或节点）
#         #print("No!")
#         return 0
#     elif number==0:   #没有测试序列生成
#         #print("No!")
#         return 0
#     elif number!=0 and judge==0:#有测试序列生成 没有测试数据生成
#         #print("Warning!")
#         return 1
#     elif number!=0 and judge!=0:#有测试数据生成
#         #print("Yes!")
#         return 2
#     #sys.stdout = savedStdout  # 恢复标准输出流
#  # shutil.copy('model/resultModel.txt',filename)#将前端删除的结果模型写入'model/resultModel.txt'中时，先将原模型复制到resultModel2.txt中
#                                                  #这件事要在用户删除边或节点触发模型修改事件后，就要先做，然后再调用judegeDelete判断能不能删
#
# def judegeDelete():
#
#     # lines = open(filename, 'r', encoding="utf-8").readlines()
#     #记录原模型的迁移数量
#     # oldTransNumber=0
#     # for line in lines:
#     #     if line.strip() == "Transition:":
#     #         oldTransNumber+=1
#     # print(TransNumber)
#     #记录删除状态或迁移后的模型的迁移数
#     SM = returnSM()
#     currentTransNumber=len(SM.transitionList)#表示迁移的数量
#     # transRatio=double(currentTransNumber/oldTransNumber)#获得现在模型和原模型的迁移比例
#     # print(transRatio)
#     #savedStdout = sys.stdout  # 保存标准输出流
#     #with open('judgeResult.txt', 'w+') as file:
#         #sys.stdout = file  # 标准输出重定向至文件
#     import os
#     filename1 = "failureTran/target3.txt"
#     if not os.path.getsize(filename1):
#         # print('****',os.path.getsize(filename1))
#         SM = returnSM()
#         inDegreeisZeroState = judgeInDegreeisZero(SM)  # 表示入度为0的状态数
#         if inDegreeisZeroState == 1: #删完有入度为0的状态节点，不能删
#             #print("No!")
#             #shutil.copy(filename,'model/resultModel.txt')#返回原模型
#             return 0
#         elif inDegreeisZeroState == 0:
#             #print('Yes!')
#             #shutil.copy('model/resultModel.txt',filename)
#             return 2
#     else:
#         # print('执行这里')
#         oriModel = efsmFromFile('resultModel2.txt')
#         # print(oriModel.transitionList)
#         TransNum = len(oriModel.transitionList)
#         # print(TransNum)
#         inDegreeisZeroState = judgeInDegreeisZero(oriModel)  # 表示入度为0的状态数
#         # print(inDegreeisZeroState)
#         if inDegreeisZeroState == 1: #删完有入度为0的状态节点，不能删
#             #print("No!")
#             #shutil.copy(filename,'model/resultModel.txt')#返回原模型
#             return 0
#         else:
#             lines = open(filename1, 'r', encoding="utf-8").readlines()
#             for line in lines:
#                 state = line
#             state = oriModel.state(state)
#             relateTrans = len(oriModel.delState(state))
#             transRatio = double(relateTrans/TransNum)
#             if transRatio >= 0.2:
#                 #print('Warning!')
#                 return 1
#             else:
#                 #print('Yes!')
#                 #shutil.copy('model/resultModel.txt', filename)
#                 with open(filename1, 'r+') as file:
#                     file.truncate(0)
#                 return 2
def judegeAdd():
    judgeLabel=""
    SM = returnSM()
    inDegreeisZeroState = judgeInDegreeisZero(SM)  # 表示入度为0的状态数
    # print(inDegreeisZeroState)
    if inDegreeisZeroState == 1:  # 如果加入之后是有入度为0的迁移（加入一条孤立的迁移或节点）
        judgeLabel = 0
        # print("No!")
    if inDegreeisZeroState == 0:
        number, judge = judgeFeasibility()
        if number == 0:  # 没有测试序列生成
            judgeLabel = 0
            # print("No!")
        elif number != 0 and judge == 0:  # 有测试序列生成 没有测试数据生成
            judgeLabel = 1
            # print("Warning!")
        elif number != 0 and judge != 0:  # 有测试数据生成
            judgeLabel = 2
            # print("Yes!")
    return judgeLabel
 # shutil.copy('model/resultModel2.txt',filename)#将前端删除的结果模型写入'model/resultModel2.txt'中时，先将原模型复制到resultModel2.txt中
def judegeDelete():
    judgeLabel = ""
    oriModel = efsmFromFile(filepath+'resultModel2.txt')#存储原模型，没删除的上一次的模型
    TransNum = len(oriModel.transitionList) #计算原模型的迁移数
    # print(TransNum)
    SM = returnSM()
    currentTransNumber = len(SM.transitionList)  # 表示删除迁移后的模型Model/resultModel1.txt迁移数量
    # print(currentTransNumber)
    print (SM.transitionList)
    transRatio = double(1 - (currentTransNumber / TransNum))
    # print('SM=',type(SM))
    inDegreeisZeroState = judgeInDegreeisZero(SM)  # 表示入度为0的状态数
    if inDegreeisZeroState == 1:  # 删完有入度为0的状态节点，不能删
        judgeLabel= 0
        # print("No!")
    if inDegreeisZeroState == 0:
        if transRatio >= 0.2:   #删除的迁移太多 警告
            judgeLabel = 1
            # print('Warning!')
        else:
            judgeLabel = 2
            # print("Yes!")
    return judgeLabel
if __name__ == '__main__':
    print('test:'+judgeLabel)
    judgeLabel=judegeAdd()

#sys.stdout = savedStdout  恢复标准输出流


