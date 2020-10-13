import os
import shutil
import sys
from numpy import double
from judgeFeasibility.Main import judgeFeasibility, judgeInDegreeisZero
from judgeFeasibility.obtain_efsm_info import returnSM
from judgeFeasibility.EFSM import efsmFromFile
def judegeAdd():
    judgeLabel=""
    inDegreeisZeroState = judgeInDegreeisZero("resultModel3.txt")#判断修改后的模型的度数
    # print(inDegreeisZeroState)
    result2=[]
    print(inDegreeisZeroState)
    if inDegreeisZeroState == 1:  # 如果加入之后是有入度为0的迁移（加入一条孤立的迁移或节点）
        judgeLabel = "No!"
        result2.append(judgeLabel)
        # print("No!")
    if inDegreeisZeroState == 0:
        result=judgeFeasibility("failureTran/target1.txt","model/resultModel.txt")
        # print(result)
        for i in range(0,len(result)):
            if result[i][0]==0: #没有有测试序列生成
                judgeLabel = "No!"
                result2.append(judgeLabel)
            elif result[i][0]==1 and result[i][1]==0:  # 有测试序列生成 没有测试数据生成
                judgeLabel = "Warning!"
                result2.append(judgeLabel)
            elif result[i][0]==1 and result[i][1]==1:  # 有测试数据生成
                judgeLabel = "Yes!"
                result2.append(judgeLabel)
    return result2
 # shutil.copy('model/resultModel2.txt',filename)#将前端删除的结果模型写入'model/resultModel2.txt'中时，先将原模型复制到resultModel2.txt中
def judegeDelete():
    judgeLabel=""
    oriModel= efsmFromFile('model/resultModel.txt')#存储原模型，没删除的上一次的模型
    TransNum=len(oriModel.transitionList) #计算修改后的模型的迁移数
    oriModel = efsmFromFile('resultModel3.txt')  # 存储删除边后的模型
    currentTransNumber= len(oriModel.transitionList)  # 计算删除后的模型的迁移数
    transRatio = double(1 - (currentTransNumber / TransNum))
    inDegreeisZeroState = judgeInDegreeisZero('resultModel3.txt')  # 表示入度为0的状态数
    print(inDegreeisZeroState)
    # print(TransNum)
    # print(currentTransNumber)
    # print(transRatio)
    if inDegreeisZeroState == 1:  # 删完有入度为0的状态节点，不能删
        judgeLabel= "No！"
        # print("No!")
    if inDegreeisZeroState == 0:
        if transRatio >= 0.2:   #删除的迁移太多 警告
            judgeLabel = "Warning"
            # print('Warning!')
        else:
            judgeLabel = "Yes！"
            # print("Yes!")
    return judgeLabel
if __name__ == '__main__':
    print(judegeAdd())
    # judgeLabel=judegeDelete()
    # print(judgeLabel)