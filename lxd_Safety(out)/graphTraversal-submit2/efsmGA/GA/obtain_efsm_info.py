# encoding:UTF-8

import sys
import types
import re

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../subjects")
import os
import sys
import EFSM
import config
import lusst
import lusst.SM as LSM
import lusst.Skip as SKIP
import execution.format as format

format.formatfile()


SM = EFSM.efsmFromFile(config.getGenerateModule())  # 对efsm类实例化

#获取模型
def obtain_tran_info():  # 得到某efsm的全部迁移信息（name, src, tgt, event, cond, action）

    #    modelfile="ntscd_example.txt"
    #    modelfile="sm3.txt"
    #    modelfile="fairnessEG.txt"
    #    modelfile="kellysample.txt"

    #    modelfile="EFSM_ATM_noexit.txt"
    #    modelfile="efsm_atm_noexit_temp.txt"
    #    modelfile="EFSM_ATM_noexit_new.txt"
    #    modelfile="EFSM_Cashier.txt"
    #   modelfile="EFSM_Cashier_shortPin.txt"
    #    modelfile="EFSM_Cashier_noexit.txt"
    #    modelfile="EFSM_CruiseControl-new.txt"
    #    modelfile="EFSM_FuelPump.txt"
    #    modelfile="EFSM_FuelPump_noexit.txt"
    #    modelfile="EFSM_INRES.txt"
    #    modelfile="EFSM_INRES_noexit.txt"
    #    modelfile="EFSM_Lift.txt"
    #    modelfile="EFSM_SimplifiedPhone.txt"
    #    modelfile="EFSM_SimplifiedPhone_noexit.txt"
    #    modelfile="EFSM_TCP.txt"
    #    modelfile="EFSM_PrinTok.txt"
    #    modelfile="EFSM_TCSbin.txt"
    #    modelfile="EFSM_TCSbin_EXIT.txt"
    #    modelfile="EFSM_VendingMachine.txt"
    #    modelfile="EFSM_VendingMachine_noexit.txt"
    ##################################################

    # print "%s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))

    return SM.transitionList
    #print SM.transitionList[1].src.name


def tran_number():
    return len(SM.transitionList)


def obtain_end_tranlist():  # 得到end transition list
    SM.findEndTransition()
    return SM.endTransitionList


def obtain_start_tranlist():
    SM.findStartTransition()
    return SM.startTransitionList


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


def getSimplevDefUseList(currTransition):
    if currTransition.name not in SM.tranVarDict:
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

def findTranWithSameEvent(targetedTran):
    #return [item for item in SM.transitionList if item.event.split(';')[0] == targetedTran.event.split(';')[0]]
    return [item for item in SM.transitionList if item.event == targetedTran.event]

# 根据数据依赖关系排序
def gjsjylgxpx(targetedTran, CandidateOppositeBranchList):
    vDUDict = getSimplevDefUseList(targetedTran)
    targetuselist = list(set(vDUDict['condVuse']))
    CandidateOppositeBranchDict = dict()
    for CandidateOppositeBranch in CandidateOppositeBranchList:
        Candidatelist = obtain_succ(CandidateOppositeBranch)
        for candidate in Candidatelist:
            vDUDict = getSimplevDefUseList(candidate)
            tmpdeflist = vDUDict['actionVdef'][:]
            # 可能后续需要加可行性判断
            num = len(set(tmpdeflist) & set(targetuselist))
            if not (CandidateOppositeBranch in CandidateOppositeBranchDict
                    and num < CandidateOppositeBranchDict[CandidateOppositeBranch]):
                CandidateOppositeBranchDict[CandidateOppositeBranch] = num
    res = CandidateOppositeBranchDict.items()
    if config.mbfzpax == 1:
        res = sorted(CandidateOppositeBranchDict.items(), key=lambda x: x[1], reverse=True)
    return [key.src for key, values in res]

# 第一种情况，event相同，con相反
def getOppositeBranch(targetedTran):
    TranWithSameEvent = findTranWithSameEvent(targetedTran)
    #print "相同EVENT迁移为%s"%([item.name for item in TranWithSameEvent])
    cond = "!(" + targetedTran.cond[:] + ")"
    # print cond
    CandidateOppositeBranchList = [item for item in TranWithSameEvent if item.cond.find(cond) != -1]
    cond = targetedTran.cond[:]

    if len(cond) > 2 and cond[0] == '!' and cond[1] == '(' and cond[-1] == ')':

        cond = cond[2:-1]
        CandidateOppositeBranchList = [item for item in TranWithSameEvent if item.cond.find(cond) != -1]

    if len(CandidateOppositeBranchList) == 0:

        return None
    if len(CandidateOppositeBranchList) == 1:

        return [CandidateOppositeBranchList[0].src]

    return gjsjylgxpx(targetedTran, CandidateOppositeBranchList)  # 根据数据依赖关系排序并返回


# 第二种情况，event相同，con不同
def getSecondOppositeBranch(targetedTran):
    TranWithSameEvent = findTranWithSameEvent(targetedTran)
    return gjsjylgxpx(targetedTran, TranWithSameEvent)


if __name__ == '__main__':  # not execute when import as a module
    '''
    print "%s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))
    traninfolist = obtain_tran_info()
    print traninfolist
    endtran = obtain_end_tranlist()
    print endtran
    print tran_number()

    print ''
    print 'newtest'
    src = SM.state('S1')
    tgt = SM.state('S2')
    test_target = EFSM.Transition('target', src, tgt, 'Card(ab, sb, cb)', 'write("Enter PIN");', 'attempts = 0')
    print getUseList(getTran(16))
    print getUseList(getTran(14))
    print getUseList(getTran(7))
    print getUseList(getTran(5))
    print getTran(4)
    print getUseList(getTran(4))
    print getSimplevDefUseList(test_target)
    '''
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



    # print getSimplevDefUseList(getTran(14))
    # print getSimplevDefUseList(getTran(13))
    # print getTran(13).name[1:]
    # print obtain_succ(getTran(13))
    # obtain_end_tranlist()
    # obtain_succ()
    # p=find_subpath('T8')
    # print p
    # allpath=find_allpath()
    # print allpath
