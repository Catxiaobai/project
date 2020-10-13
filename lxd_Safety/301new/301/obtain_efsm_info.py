# encoding:UTF-8

import sys
import types
import re
import EFSM
import config

SM = EFSM.efsmFromFile(config.getGenerateModule())  # 对efsm类实例化
#----------------rinsmq
# print ('rinsmq')
print('执行 obtain_efsm_info 文件')
#----------------rinsmq

def obtain_tran_info():  # 得到某efsm的全部迁移信息（name, src, tgt, event, cond, action）
    # print "%s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))
    return SM.transitionList

def tran_number():
    return len(SM.transitionList)


def obtain_end_tranlist():  # 得到end transition list
    SM.findEndTransition()
    return SM.endTransitionList

def obtain_start_tranlist():
    SM.findStartTransition()
    return SM.startTransitionList

#返回当前迁移的前向迁移（前向迁移的结束节点指向当前迁移的开始节点）
def obtain_succ(currTransition):
    res = SM.transitionSuccessor(currTransition)
    return res  # 里面被我改成向上找迁移了，原本是向下找迁移

    pathlist = SM.findPath(start)
    return pathlist

def getAllEventDef():
    res = set
    for currTransition in SM.transitionList:
        res = res & set(SM.vDefUseList(currTransition)['eventVdef'])
    return list(res)
    pathlist = SM.findAllPath()
    return pathlist

def getTran(target):
    return SM.transitionList[target - 1]

# 返回当前迁移变量
def getSimplevDefUseList(currTransition):
    if currTransition.name not in SM.tranVarDict:  #??????????
        SM.vDefUseList(currTransition)
    return SM.tranVarDict[currTransition.name]


def getALLvDefUseList(currList):
    res = []
    for transition in currList:
        res.append(getSimplevDefUseList(transition))
    return res


def getUseList(currList):
    vDUDict = getSimplevDefUseList(currList)
    return list(set(vDUDict['condVuse'] + vDUDict['actionVuse']))
#返回有相同event事件的迁移
def findTranWithSameEvent(targetedTran):
    print "执行返回有相同event事件的迁移函数"
    return [item for item in SM.transitionList if item.event == targetedTran.event]

# 根据数据依赖关系排序
# 只考虑前序迁移操作定义变量与目标迁移的谓词条件变量的交集！！！！ rinsmq改为与操作变量和谓词条件变量的交集
def gjsjylgxpx(targetedTran, CandidateOppositeBranchList):
    print "执行根据数据依赖关系排序函数"
    vDUDict = getSimplevDefUseList(targetedTran)
    # print 'vDUDict=',vDUDict
    targetuselist = list(set(vDUDict['condVuse']) | set(vDUDict['actionVuse']))
    print targetuselist
    CandidateOppositeBranchDict = dict()
    for CandidateOppositeBranch in CandidateOppositeBranchList:
        Candidatelist = obtain_succ(CandidateOppositeBranch)
        for candidate in Candidatelist:
            vDUDict = getSimplevDefUseList(candidate)
            tmpdeflist = vDUDict['actionVdef'][:]
            # 可能后续需要加可行性判断
            num = len(set(tmpdeflist) & set(targetuselist))
            # print 'num=',num
            if not (CandidateOppositeBranch in CandidateOppositeBranchDict
                    and num < CandidateOppositeBranchDict[CandidateOppositeBranch]):
                CandidateOppositeBranchDict[CandidateOppositeBranch] = num
    # print 'CandidateOppositeBranchDict=',CandidateOppositeBranchDict
    res = CandidateOppositeBranchDict.items()
    # 目标分支排序
    if config.mbfzpax == 1:
        res = sorted(CandidateOppositeBranchDict.items(), key=lambda x: x[1], reverse=True)
    ans = []
    for key,values in res:
        if key.src not in ans:
            ans.append(key.src)
    print "执行根据数据依赖关系排序结束"
    return ans

# 第一种情况，event相同，con相反
# 查找对立分支返回目标分支起始节点
def getOppositeBranch(targetedTran):
    TranWithSameEvent = findTranWithSameEvent(targetedTran)
    #print "相同EVENT迁移为%s"%([item.name for item in TranWithSameEvent])
    cond = "!(" + targetedTran.cond[:] + ")"
    CandidateOppositeBranchList = [item for item in TranWithSameEvent if item.cond.find(cond) != -1]
    cond = targetedTran.cond[:]
    if len(cond) > 2 and cond[0] == '!' and cond[1] == '(' and cond[-1] == ')':
        cond = cond[2:-1]
        CandidateOppositeBranchList = [item for item in TranWithSameEvent if item.cond.find(cond) != -1]
    if len(CandidateOppositeBranchList) == 0:
        return None
    if len(CandidateOppositeBranchList) == 1:
        return [CandidateOppositeBranchList[0].src]
    # print 'Candidate=',CandidateOppositeBranchList
    # print ''
    return gjsjylgxpx(targetedTran, CandidateOppositeBranchList)  # 根据数据依赖关系排序并返回


# 第二种情况，event相同，con不同
def getSecondOppositeBranch(targetedTran):
    TranWithSameEvent = findTranWithSameEvent(targetedTran)
    # print 'TranWithSameEvent=',TranWithSameEvent
    return gjsjylgxpx(targetedTran, TranWithSameEvent)


f = open("failureTran/target.txt", 'r')
targetList=[]
targetList = f.readlines()
f.close()
s = []
k=0
targetbranchlist=[]

for item in targetList:
    s.append(item.split(', '))
    print s
    #需要修改成<name, src，tgt，event，cond，action>
    src = SM.state(s[k][1])
    tgt = SM.state(s[k][2])
    targetbranchlist.append(EFSM.Transition(s[k][0], src, tgt, s[k][3], s[k][4], s[k][5]))
    k+=1

def targetBranch():
    return targetbranchlist[0]

def change():
    targetbranchlist.pop(0)
def sort():
    targetbranchlist.append(targetbranchlist[0])
    targetbranchlist.remove(targetbranchlist[0])

def tragetState():
    s.append(item.split(', '))
    return SM.state(s[k][1])

def returnSM():
    return SM




if __name__ == '__main__':  # not execute when import as a module

    ''''''
    print getOppositeBranch(getTran(7))
    print getOppositeBranch(getTran(16))
    print getOppositeBranch(getTran(4))
    ''''''
    # print obtain_succ(getTran(16))
    print getSimplevDefUseList(getTran(1))


    strings = ""
    print range(1,2)

    a = 1
    exec "a = 2"
    print a

    str = re.search("!{0,1}\([^(]*?cb" + '[^)]*?\)', "(!!(cb= cb - w)))));aaaa").group()
    print str[:-1]
    pos = str.find('=')
    print str[pos+1:]

    dic = {'s': "1", 'd': "s"}
    print dic
    s = 2
    exec ("print s=='1'", dic)
    exec ("c=1", dic)
    print "c=%s"%(dic['c'])
    exec "print a==2"

    if not(a == 1):
        print 0
    flag = True
    documentedituserpasswordvalue = 'a'
    documentedituserpassword2value = 'a'
    string = "(not (documentedituserpasswordvalue == '' and documentedituserpassword2value == ''))  and  (documentedituserpasswordvalue == documentedituserpassword2value)"
    exec "if not " + string+":\n\tflag = False"
    print flag

    l='e'
    if not l=='s':
        print "wawawa"


