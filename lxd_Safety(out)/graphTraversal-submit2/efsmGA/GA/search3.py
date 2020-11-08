# encoding:UTF-8
import datetime
import gc
import random
import time

from typing import List

import EFSM
import obtain_efsm_info
import re
import config
import random
import target


class TranWithInfo:
    conflictTran = {}

    def __repr__(self):
        return "<Transition %s>" % (self.tran.name)

    def __init__(self, tran):
        self.tran = tran
        self.vDUDict = obtain_efsm_info.getSimplevDefUseList(self.tran)
        self.Candidatelist = []  # 初始化时并未直接初始化，getCandidatelist时初始化
        self.candidateinitflag = 0
        self.sortedflag = 0
        self.quality = None

    def getvUseList(self):
        return list(set(self.vDUDict['condVuse']) | set(self.vDUDict['actionVuse']))

    def getvDefList(self):
        return list(set(self.vDUDict['eventVdef']) | set(self.vDUDict['actionVdef']))

    def getvcondVuse(self):
        return self.vDUDict['condVuse']

    def getvactionVuse(self):
        return self.vDUDict['actionVuse']

    def getveventVdef(self):
        return self.vDUDict['eventVdef']

    def getvactionVdef(self):
        return self.vDUDict['actionVdef']

    def getCandidatelist(self):
        if len(self.Candidatelist) == 0 and self.candidateinitflag == 0:
            self.Candidatelist = [TranWithInfo(item) for item in obtain_efsm_info.obtain_succ(self.tran)]
            self.candidateinitflag = 1
        else:
            if self.getName() in TranWithInfo.conflictTran.keys():
                self.Candidatelist = list(set(self.Candidatelist) - {TranWithInfo.conflictTran[self.getName()]})
        return self.Candidatelist

    def removeCandidate(self, CandidateTran):
        self.Candidatelist.remove(CandidateTran)

    def replaceCandidatelist(self, newCandidatelist):
        self.Candidatelist = newCandidatelist

    def getName(self):
        return self.tran.name


class PartialList:
    usePercent = None  # type: List[int]

    def __init__(self, targetBranch, starttime):
        # traninforlist = obtain_efsm_info.obtain_tran_info()
        self.targetBranch = targetBranch

        while '.' in self.targetBranch.event:
            self.targetBranch.event = self.targetBranch.event.replace('.', '')
        while '.' in self.targetBranch.cond:
            self.targetBranch.cond = self.targetBranch.cond.replace('.', '')
        while '.' in self.targetBranch.action:
            self.targetBranch.action = self.targetBranch.action.replace('.', '')

        self.targetBranchSrcList = obtain_efsm_info.getOppositeBranch(self.targetBranch)
        # self.targetBranchSrcList = obtain_efsm_info.getSecondOppositeBranch(self.targetBranch) #2020/10/14 11/35
        self.useList = []
        self.tranlist = []
        self.eventDefList = set
        self.sortKaiGuan = 1
        self.defPercent = config.defPercent  # event action
        self.usePercent = config.usePercent  # cond action
        self.sorttime = 0
        self.sortnum = 0
        #print self.targetBranchSrcList
        if self.targetBranchSrcList is not None:
            # print ("插入点列表：%s %s") % (self.targetBranchSrcList, time.time() - starttime)

            # STATE = EFSM.State("State S6")
            # targetBranch.src = STATE
            self.targetBranch.src = self.targetBranchSrcList[0]

            self.targetBranchSrcList.pop(0)
            originTran = TranWithInfo(self.targetBranch)
            originTran.quality = 'relate'
            self.useList = list(set(originTran.getvUseList()) - set(originTran.getveventVdef()))
            self.tranlist.append(originTran)
            self.eventDefList = set(originTran.getveventVdef())

        else:
            pass
            # print "目标分支无对立分支"

        # 一些后面需要用到的东西

    def __repr__(self):
        # return "<PartialList %s %s %s %s>" % (self.currentPartialList, self.nameList,self.vUseList,self.Candidatelist)
        return "<PartialList %s>" % ([item.getName() for item in reversed(self.tranlist)])

    def newTargetSrc(self):
        if len(self.targetBranchSrcList) > 0:
            self.targetBranch.src = self.targetBranchSrcList[0]
            self.targetBranchSrcList.pop(0)
            originTran = TranWithInfo(self.targetBranch)
            originTran.quality = 'relate'
            self.useList = list(set(originTran.getvUseList()) - set(originTran.getveventVdef()))
            self.tranlist = []
            self.tranlist.append(originTran)
            self.eventDefList = set(originTran.getveventVdef())

    def push(self, tranWithInfo):
        self.tranlist.append(tranWithInfo)

    def pop(self):
        if len(self.tranlist) > 0:
            self.eventDefList = set(self.eventDefList) - set(self.top().getveventVdef())
            self.tranlist.pop()
        else:
            print "部分迁移序列为空！"

    def top(self):
        return self.tranlist[-1]

    def flushUseList(self):
        self.useList = []
        for item in self.tranlist:
            self.useList = [tmp for tmp in self.useList if tmp not in item.getvDefList()]
            self.useList.extend(item.getvUseList())
            self.useList = list(set(self.useList) - set(item.getveventVdef()))
            # print self.useList

    def removeCandidate(self, CandidateTran):
        self.tranlist[-1].removeCandidate(CandidateTran)

    @property
    def getCandidatelist(self):
        # firsttime = time.time()
        tmplist = self.tranlist[-1].getCandidatelist()  # 获取栈顶迁移的前序迁移
        random.shuffle(tmplist)
        firsttime = time.time()
        if self.tranlist[-1].sortedflag == 0:
            if self.sortKaiGuan > 0:
                '''
                for item in tmplist:
                    print "vDEF%s"%(item.getvDefList())
                    print "useList%s"%(self.useList)
                    if len(set(item.getvDefList()) & set(self.useList)) >= 1:
                        atmplist.append(item)
                '''
                atmplist = [item for item in tmplist if len(set(item.getvDefList()) & set(self.useList)) >= 1]  # 筛选相关迁移
                if (self.sortKaiGuan == 1 or self.sortKaiGuan == 2) and len(atmplist) >= 1:  # 如果存在相关迁移，且原迁移未筛选过
                    tmplist = atmplist
                    for tran in tmplist:
                        tran.quality = 'relate'
                    if config.yrzswgbl == 1:
                        tmplist = sorted(tmplist,
                                         key=lambda x: len(x.getvcondVuse()) * self.usePercent[0] + len(
                                             x.getvactionVuse()) * self.usePercent[1])  # 按引入变量的多少排序，少的优先
                    if config.achcdpx == 1:
                        tmplist = sorted(tmplist, key=self.achcdpx, reverse=True)  # 按重合程度排序
                    if config.achxhpx == 1:
                        tmplist = sorted(tmplist, key=self.achxhpx)  # 按重合先后排序
                    if config.hhpx == 1 and len(tmplist) > 1:
                        if self.achcdpx(tmplist[0]) == self.achcdpx(tmplist[1]):
                            tmplist = sorted(tmplist, key=self.hhpx, reverse=True)  # 混合排序
                    # self.sortnum += 1;
                if (self.sortKaiGuan == 1 or self.sortKaiGuan == 3) and len(atmplist) < 1:
                    tmplist = sorted(tmplist, key=lambda x: len(set(x.getvUseList()) - set(x.getveventVdef())))
                    for tran in tmplist:
                        tran.quality = 'noRelate'
                    # self.sortnum += 1;
                if config.newtransort == 1:
                    tmplist = sorted(tmplist, key=self.isNewTran, reverse=True)
                # self.sorttime += time.time() - firsttime
                if (self.sortKaiGuan == 3 and len(atmplist) >= 1) or (self.sortKaiGuan == 2 and len(atmplist) < 1):
                    tmplist = tmplist
                self.sorttime += time.time() - firsttime
            else:
                # random.shuffle(tmplist)
                if config.newtransort == 1:
                    tmplist = sorted(tmplist, key=self.isNewTran, reverse=True)
                # tmplist=tmplist
        self.tranlist[-1].sortedflag = 1
        self.tranlist[-1].replaceCandidatelist(tmplist)
        self.sortnum += 1
        # self.sorttime += time.time() - firsttime
        # self.sorttime += time.time() - firsttime
        return tmplist

    def achcdpx(self, tran):  # 按重合程度排序

        eventDefSet = set(tran.getveventVdef())
        actionDefSet = set(tran.getvactionVdef())
        defSet = set(tran.getvDefList())

        for item in reversed(self.tranlist):
            eventDefSet = eventDefSet - set(item.getvDefList())  # 消去迁移中已有的定义变量（针对自己定义自己使用的情况）
            actionDefSet = actionDefSet - set(item.getvDefList())
            defSet = defSet - set(item.getvDefList())
            if len(eventDefSet) == 0 or len(actionDefSet) == 0 or len(defSet) == 0:  # 不存在 没在序列中找到定义的 def集合 时，break
                break

        res = (len(set(eventDefSet) & set(self.useList)) * self.defPercent[0]
               + len(set(actionDefSet) & set(self.useList)) * self.defPercent[1] + 1) / (
                      len(self.useList) + 1)
        # res = config.distMap(dist) * config.numMap(res)  # 距离的映射函数 * 数量的映射函数
        return res

    def hhpx(self, tran):  # 混合排序#不是看最近距离，看每个重合变量的距离
        dist = 0
        defSet = set(tran.getvDefList())

        for item in reversed(self.tranlist):
            defSet = defSet - set(item.getvDefList())
            if len(defSet) == 0:  # 不存在 没在序列中找到定义的 def集合 时，break
                break
        for item in reversed(self.tranlist):
            dist += 1
            if len(set(defSet) & set(item.getvUseList())) != 0:
                break

        res = config.distMap(dist) * config.numMap(self.achcdpx(tran))  # 距离的映射函数 * 数量的映射函数
        return res

    def achxhpx(self, tran):  # 按重合先后排序（只看最近距离）
        dist = 0
        for item in reversed(self.tranlist):
            dist += 1
            if len(set(tran.getvDefList()) & set(item.getvUseList())) != 0:
                break
        return dist

    def isNewTran(self, tran):
        for item in self.tranlist:
            if item.getName() == tran.getName():
                return 0
        return 1

    def isComplete(self):
        if len(self.tranlist) == 0:  # 目标分支出发的所有路径全无法达成
            return 0
        if self.tranlist[-1].tran.src.name == "START" and len(self.useList) == 0:  # 成功的情况
            return 1
        else:
            return 2  # 其余情况


def insert_value_dict(value_dict, action_def, selected_tran):
    if action_def not in value_dict:
        tmp_list = [selected_tran]
        value_dict[action_def] = tmp_list
    else:
        value_dict[action_def].append(selected_tran)


def get_infeasible_order_number(selected_tran, tran_list, partialListEventDefList):
    operator = ['+', '-', '*', '/']
    actionDefList = selected_tran.getvactionVdef()
    actionUseList = selected_tran.getvcondVuse()
    eventDefList = selected_tran.getveventVdef()
    # 外部输入的变量不会引发冲突
    actionDefList = list(set(actionDefList) - set(eventDefList))  # 针对输入a，a = a + c的情况
    # 针对输入a，v = a的情况
    selectedTranAction = selected_tran.tran.action
    eventDefList = set(eventDefList) | set(partialListEventDefList)

    # 分析action
    tmpDic = {}
    for actionDef in actionDefList:
        judge = re.search(actionDef + '[^;]*(?=;{0,1})', selectedTranAction)  # 这里实际上是假设了都是形如a=xxx的形式
        if judge is not None:  # 分四种情况讨论
            judge = judge.group()
            if '=' in judge:
                pos = judge.find('=')
                strDef = judge[pos + 1:].strip()

                # 包含外部变量的直接跳
                if strDef in eventDefList:
                    eventDefList.add(strDef)  # 拓展，次级外部输入
                    continue
                flag = 0
                for eventDef in eventDefList:
                    if eventDef in strDef:
                        flag = 1
                        continue
                if flag == 1:
                    continue

                if strDef in selected_tran.getvactionVuse():  # v = v'
                    if strDef in tmpDic:
                        tmpDic[actionDef] = tmpDic[strDef]
                else:
                    flag = 'c'
                    for op in operator:
                        if op in strDef:
                            flag = 'voc'
                            for actionUse in selected_tran.getvactionVuse():
                                if actionUse != actionDef and actionUse in strDef:  # v = v op v'
                                    flag = 'vov'
                                    if actionDef in tmpDic and actionUse in tmpDic:
                                        exec (judge, tmpDic)
                                    break
                            if flag == 'voc':  # v = v op c
                                if actionDef in tmpDic:
                                    exec (judge, tmpDic)
                                break
                    if flag == 'c':  # v = c
                        exec (judge, tmpDic)
    if len(tmpDic) > 0:  # 只有action存在定义的时候才有可能不可行
        for i in range(len(tran_list) - 1, -1, -1):
            item = tran_list[i]

            if len(item.getvcondVuse()) > 0:
                flag = True
                for cond in item.getvcondVuse():  # 全都要已存在定义
                    if cond not in tmpDic and cond not in eventDefList:
                        flag = False
                        break
                if flag:
                    cond = item.tran.cond[:]
                    for condUse in item.getvcondVuse():
                        if condUse in eventDefList:
                            stra = re.search("!{0,1}\([^(]*" + condUse + '[^)]*\)', cond)
                            if stra:
                                stra = stra.group()
                                cond = cond.replace(stra, 'True')
                            strb = re.search("[^&|(]*" + condUse + '[^&|)]*', cond)
                            if strb:
                                strb = strb.group()
                                cond = cond.replace(strb, 'True')
                    cond = cond.replace('!(', ' not (')
                    cond = cond.replace('&&', ' and ')
                    cond = cond.replace('&', ' and ')
                    cond = cond.replace('|', ' or ')
                    while '(True)' in cond or 'True and True' in cond:
                        cond = cond.replace('not (True)', 'True')
                        cond = cond.replace('(True)', 'True')
                        cond = cond.replace('True and True', 'True')
                    # print item.tran.name
                    # print "判断条件：%s" % (cond)
                    tmpDic['isFeasibilityBeforeCorrect'] = True
                    exec ("if not (" + cond + "):\n\tisFeasibilityBeforeCorrect = False", tmpDic)
                    if not tmpDic['isFeasibilityBeforeCorrect']:
                        return i

            for actionDef in item.getvactionVdef():
                judge = re.search(actionDef + '[^;]*(?=;{0,1})', item.tran.action)  # 这里实际上是假设了都是形如a=xxx的形式
                if judge is not None:  # 分四种情况讨论
                    judge = judge.group()
                    if '=' in judge:
                        pos = judge.find('=')
                        strDef = judge[pos + 1:].strip()

                        # 包含外部变量的直接跳
                        if strDef in eventDefList:
                            eventDefList.add(strDef)  # 拓展，次级外部输入
                            continue
                        flag = 0
                        strDefList = strDef.split(" ")
                        for eventDef in eventDefList:
                            for sd in strDef:
                                if eventDef == sd:
                                    flag = 1
                                    break
                        if flag == 1:
                            continue

                        if strDef in item.getvactionVuse():  # v = v'
                            if strDef in tmpDic:
                                tmpDic[actionDef] = tmpDic[strDef]
                        else:
                            flag = 'c'
                            for op in operator:
                                if op in strDef:
                                    flag = 'voc'
                                    for actionUse in item.getvactionVuse():
                                        if actionUse != actionDef and actionUse in strDef:  # v = v op v'
                                            flag = 'vov'
                                            if actionDef in tmpDic and actionUse in tmpDic:
                                                exec (judge, tmpDic)
                                            break
                                    if flag == 'voc':  # v = v op c
                                        if actionDef in tmpDic:
                                            exec (judge, tmpDic)
                                        break
                            if flag == 'c':  # v = c
                                exec (judge, tmpDic)
    return -1


def search():
    # 初始化：name, src=None, tgt=None, event=None, cond=None, action=None
    operator = ['+', '-', '*', '/']  # 4种情况
    loopLimit = config.loopLimit   #修正次数上限
    numOfPSG = config.numOfPSG   #序列生成条数
    psDict = {}
    psDict1 = {}
    psDict2 = {}
    psDict3 = {}

    while numOfPSG > 0:

        print 'num=%s' % (numOfPSG)
        numOfPSG = numOfPSG - 1

        starttime = time.time()

        partialList = PartialList(target.targetBranch(), starttime)
        #print partialList.targetBranchSrcList
        partialList.sortKaiGuan = config.sort  # 排序开关 1是排序； 0是全随机，除了候选对立分支； 2是连接迁移随机
        # partialList = PartialList(obtain_efsm_info.getTran(70))r
        valueDict = {}
        # print partialList
        if partialList.targetBranchSrcList is not None:

            while partialList.isComplete() == 2 or (
                    partialList.isComplete() == 0 and len(partialList.targetBranchSrcList) > 0):
                if partialList.isComplete() == 0 and len(partialList.targetBranchSrcList) > 0:
                    partialList.newTargetSrc()
                # print "一次执行前的部分序列%s%s" % (partialList, time.time() - starttime)
                candidateList = partialList.getCandidatelist
                #print "前序候选迁移集合:%s" % (candidateList)
                if len(candidateList) == 0:
                    if config.back == 1:
                        partialList.pop()
                    # print time.time()-starttime
                    # 下面是回溯至上一数据相关迁移的代码
                    elif config.back == 0:
                        if len(partialList.tranlist) == 1:
                            partialList.pop()
                        else:
                            partialList.pop()
                            while partialList.top().quality != 'relate':
                                partialList.pop()
                    partialList.flushUseList()
                    # print time.time()-starttime
                    continue
                '''if partialList.sortKaiGuan == 1:
                    selectedTran = candidateList[0]
                else:
                    if partialList.sortKaiGuan == 0 or (partialList.sortKaiGuan == 2 and candidateList[0].quality != 'relate') or (partialList.sortKaiGuan == 3 and candidateList[0].quality != 'noRelate'):
                        # print partialList.sorttime
                        # othertime = time.time()
                        rand = random.randint(0, len(candidateList) - 1)
                        selectedTran = candidateList[rand]
                        # partialList.sorttime += time.time() - othertime
                        # print partialList.sorttime
                        # print "选取 %s" % (rand)
                    else:
                       selectedTran = candidateList[0]
                '''
                selectedTran = candidateList[0]
                partialList.removeCandidate(selectedTran)
                # print partialList.top().getCandidatelist()
                if selectedTran.tran == partialList.top().tran:  # 最优先候选迁移是序列首个迁移本身的情况
                    continue
                pb = 0
                for i in range(len(partialList.tranlist)):
                    # 候选迁移在部分序列中出现，且只有一个候选迁移
                    if partialList.tranlist[i].tran == selectedTran.tran and len(partialList.tranlist[-1].Candidatelist)==1:
                        pb = 1
                        break
                if pb == 1:
                    continue
                isFeasibility = True
                # 判断是否矛盾变量冲突
                selectedTranCond = selectedTran.tran.cond
                #print selectedTranCond
                for item in reversed(partialList.tranlist):
                    cond = item.tran.cond
                    opposeCond = "!(" + cond + ")"
                    #print opposeCond
                    # if len(set(selectedTran.getvcondVuse()) - set(item.getvDefList())) == 0:
                    #   break
                    if opposeCond == selectedTranCond:  # 矛盾迁移

                        isFeasibility = False
                        TranWithInfo.conflictTran[item.tran.name] = selectedTran.tran.name
                        TranWithInfo.conflictTran[selectedTran.tran.name] = item.tran.name
                        break
                    # print cond
                    if len(cond) > 2 and cond[0] == '!' and cond[1] == '(' and cond[-1] == ')':
                        opposeCond = cond[2:-1]
                        # if len(set(selectedTran.getvcondVuse()) - set(item.getvDefList())) == 0:
                        #    break
                        if opposeCond == selectedTranCond:  # 矛盾迁移

                            isFeasibility = False
                            TranWithInfo.conflictTran[item.tran.name] = selectedTran.tran.name
                            TranWithInfo.conflictTran[selectedTran.tran.name] = item.tran.name
                            break
                    # for actiondef in actionDefList:
                    #   pos = cond.find(actiondef)
                    # if pos != -1:
                if not isFeasibility:
                    # print "矛盾变量冲突"
                    continue
                # 判断是否选择变量冲突

                actionDefList = selectedTran.getvactionVdef()
                actionUseList = selectedTran.getvcondVuse()
                eventDefList = set(selectedTran.getveventVdef())
                # 外部输入的变量不会引发冲突
                actionDefList = list(set(actionDefList) - set(eventDefList))  # 针对输入a，a = a + c的情况
                selectedTranAction = selectedTran.tran.action
                eventDefList = eventDefList | set(partialList.eventDefList)
                # 分析action
                tmpDic = {}

                for actionDef in actionDefList:
                    judge = re.search(actionDef + '[^;]*(?=;{0,1})', selectedTranAction)  # 这里实际上是假设了都是形如a=xxx的形式
                    if judge is not None:  # 分四种情况讨论
                        judge = judge.group()
                        # print judge
                        if '=' in judge:
                            pos = judge.find('=')
                            strDef = judge[pos + 1:].strip()

                            # 包含外部变量的直接跳
                            if strDef in eventDefList:
                                eventDefList.add(strDef)  # 拓展，次级外部输入
                                continue
                            if strDef in actionUseList:  # v = v'
                                if actionDef in eventDefList:  # 重定义的话要才从eventdef里删除
                                    eventDefList.remove(actionDef)
                            else:
                                flag = 'c'
                                for item in operator:

                                    if item in strDef:
                                        flag = 'vo'  # v=v op c or v=v op v'
                                        break
                                if flag == 'c':  # v = c
                                    exec (judge, tmpDic)

                if len(tmpDic) > 0:
                    # print "开始二阶段可行性判断"
                    num = get_infeasible_order_number(selectedTran, partialList.tranlist, partialList.eventDefList)
                    # print num
                    flag = 0
                    if num >= 0:
                        tranList = partialList.tranlist
                        linShiDic = tmpDic.copy()
                        isCorrect = False
                        for k in range(len(tranList) - 1, num, -1):
                            if isCorrect:
                                break
                            item = tranList[k]
                            for actionDef in item.getvactionVdef():
                                judge = re.search(actionDef + '.*(?=;| \Z)', item.tran.action)  # 这里实际上是假设了都是形如a=xxx的形式
                                if judge is not None:  # 分四种情况讨论
                                    judge = judge.group()
                                    if '=' in judge:
                                        pos = judge.find('=')
                                        strDef = judge[pos + 1:].strip()

                                        if strDef in item.getvactionVuse():  # v = v'
                                            if strDef in tmpDic:
                                                linShiDic[actionDef] = linShiDic[strDef]
                                        else:
                                            flag = 'c'
                                            for op in operator:
                                                if op in strDef:
                                                    flag = 'voc'
                                                    for actionUse in item.getvactionVuse():
                                                        if actionUse != actionDef and actionUse in strDef:  # v = v op v'
                                                            flag = 'vov'
                                                            if actionDef in linShiDic and actionUse in linShiDic:
                                                                exec (judge, linShiDic)
                                                                if item.tran.src.name == item.tran.tgt.name:
                                                                    if len(set(item.getvactionVdef()) & set(
                                                                            tranList[num].getvcondVuse())) > 0:
                                                                        numOfLoop = 1
                                                                        newTranList = tranList[:]
                                                                        newTranList.insert(k, item)
                                                                        res = get_infeasible_order_number(selectedTran,
                                                                                                          newTranList,
                                                                                                          partialList.eventDefList)
                                                                        while res != -1 and numOfLoop < loopLimit:
                                                                            numOfLoop += 1
                                                                            newTranList.insert(k, item)
                                                                            res = get_infeasible_order_number(
                                                                                selectedTran,
                                                                                newTranList,
                                                                                partialList.eventDefList)
                                                                        if res == -1:  # 纠正完成
                                                                            isCorrect = True
                                                                            partialList.tranlist = newTranList
                                                            break
                                                    if flag == 'voc':  # v = v op c
                                                        if actionDef in tmpDic:
                                                            exec (judge, linShiDic)
                                                            if item.tran.src.name == item.tran.tgt.name:
                                                                if len(set(item.getvactionVdef()) & set(
                                                                        tranList[num].getvcondVuse())) > 0:
                                                                    numOfLoop = 1
                                                                    newTranList = tranList[:]
                                                                    newTranList.insert(k, item)
                                                                    res = get_infeasible_order_number(selectedTran,
                                                                                                      newTranList,
                                                                                                      partialList.eventDefList)
                                                                    while res != -1 and numOfLoop < loopLimit:
                                                                        numOfLoop += 1
                                                                        newTranList.insert(k, item)
                                                                        res = get_infeasible_order_number(selectedTran,
                                                                                                          newTranList,
                                                                                                          partialList.eventDefList)
                                                                    if res == -1:  # 纠正完成
                                                                        isCorrect = True
                                                                        partialList.tranlist = newTranList
                                                        break
                                            if flag == 'c':  # v = c
                                                try:
                                                    exec (judge, linShiDic)
                                                except NameError:
                                                    continue
                                                else:
                                                    pass

                        if not isCorrect:
                            # print "纠正失败"
                            isFeasibility = False
                        else:
                            # print "已纠正"
                            pass
                if not isFeasibility:
                    # print "可行性判断无法通过%s" % (time.time() - starttime)
                    if time.time() - starttime > 1:
                        break
                    continue
                # “纠正”的过程：重复对判断未通过的变量有影响的、对其他变量影响最小的、可重复的、恰当的子序列
                # 现在只处理自循环
                firstFind = []
                for i in range(len(partialList.tranlist)):
                    if partialList.tranlist[i].tran == selectedTran.tran:
                        firstFind.append(i)
                if len(firstFind) == 0:
                    flag = 1
                for item in firstFind:
                    length = len(partialList.tranlist) - item
                    flag = 0
                    for i in range(item + 1, len(partialList.tranlist)):
                        if i - length < 0:
                            flag = 1
                            break
                        elif partialList.tranlist[i].tran != partialList.tranlist[i - length].tran:
                            flag = 1
                            break
                    if flag == 0:
                        for i in range(2 * item - len(partialList.tranlist) + 1, len(partialList.tranlist)):
                            partialList.eventDefList = list(
                                set(partialList.eventDefList) - set(partialList.top().getveventVdef()))
                            partialList.pop()
                            partialList.flushUseList()
                        break
                if flag == 1:
                    partialList.push(selectedTran)
                    partialList.eventDefList = eventDefList
                    partialList.flushUseList()
                    partialList.getCandidatelist
                # print "一次执行后的部分序列%s" % (partialList)
                # print "执行后部分序列的变量依赖集:%s %s" % (partialList.useList, time.time() - starttime)
                # print '\n'
                if time.time() - starttime > 1:
                    break

        if partialList.isComplete() == 0:
            # print "无任何可行序列"
            pass
        else:
            if time.time() - starttime < 1:
                psDict[partialList] = (time.time() - starttime)
                psDict1[partialList] = partialList.sorttime
                psDict2[partialList] = partialList.sortnum
            # print psDict1[partialList]
            # print "已生成序列%s 用时%s" % (partialList, time.time() - starttime)
            # for item in partialList.tranlist:
            #    print ("%s : %s") % (item.getName(), item.quality)
            # pass
    # print '\n'
    res3 = 0
    for item in psDict.keys():
        #print item
        # print len(item.tranlist)
        res3 += len(item.tranlist)
        # print psDict[item]

    res = 0
    res1 = 0
    res2 = 0

    for item in psDict.values():
        res += item
    for item in psDict1.values():
        res1 += item
    for item in psDict2.values():
        res2 += item
    global sequencenumber
    global generationtime
    global generationsorttime
    global sequencelength
    global selecenumber
    global successnumber

    sequencenumber = len(psDict)
    #print "生成序列条数为%s" % sequencenumber
    if sequencenumber == 0:
        generationtime = 0
        generationsorttime = 0
        sequencelength = 0
        selecenumber = 0
        successnumber = 0
    else:
        successnumber = 1
        generationtime = res / len(psDict)
        #print "序列生成平均时间为%s" % (generationtime)

        generationsorttime = res1 / len(psDict1)
        # print "优先级排序时间: %s"%(partialList.sorttime)
        #print "优先级排序平均时间: %s" % (generationsorttime)

        sequencelength = float(res3) / float(len(psDict1))
        #print "平均序列长度:"
        #print(format(sequencelength, '.2f'))

        selecenumber = float(res2) / float(len(psDict2))
        #print "平均选择次数1:"
        #print(format(selecenumber, '.2f'))

        # for item in psDict.keys():
        #    for k in item.tranlist:
        #       psDict3[k]=k.getName()
        #   break

    return [item.getName() for item in reversed(partialList.tranlist)]
    # return psDict3.values()


if __name__ == '__main__':
    search()
