# encoding:UTF-8
#前向搜索
import datetime
import gc
import random
import time
import re
from typing import List
#调用自己配置文件，EFSM和obtain_efsm_info文件为实验室早期研究
from lxd_verify import EFSM
from lxd_verify import obtain_efsm_info
from lxd_verify import config
from lxd_verify import sclexer

#迁移信息
class TranWithInfo:
    conflictTran = {}

    def __repr__(self):
        return "<Transition %s>" % (self.tran.name)

    def __init__(self, tran):
        self.tran = tran
        self.vDUDict = obtain_efsm_info.getSimplevDefUseList(self.tran) #获取当前迁移的变量
        self.Candidatelist = []  # 初始化时并未直接初始化，getCandidatelist时初始化
        self.candidateinitflag = 0
        self.sortedflag = 0
        self.quality = None

        #------rinsmq-----
        self.OnePriority = 0  #迁移的优先级
        self.TwoPriority = 0  #迁移的优先级
        self.ThrPriority = 0  #迁移的优先级

        #-----------------

    #获取使用变量（cond和action）
    def getvUseList(self):
        return list(set(self.vDUDict['condVuse']) | set(self.vDUDict['actionVuse']))
    #获取定义变量（event和action）
    def getvDefList(self):
        return list(set(self.vDUDict['eventVdef']) | set(self.vDUDict['actionVdef']))
    #获取cond使用变量（cond）
    def getvcondVuse(self):
        return self.vDUDict['condVuse']
    #获取操作使用变量（action）
    def getvactionVuse(self):
        return self.vDUDict['actionVuse']
    #获取事件定义变量（event）
    def getveventVdef(self):
        return self.vDUDict['eventVdef']
    #获取操作定义变量（action）
    def getvactionVdef(self):
        return self.vDUDict['actionVdef']
    #得到前向迁移列表
    def getCandidatelist(self):
        if len(self.Candidatelist) == 0 and self.candidateinitflag == 0:
            self.Candidatelist = [TranWithInfo(item) for item in obtain_efsm_info.obtain_succ(self.tran)]
            self.candidateinitflag = 1
        else:
            if self.getName() in TranWithInfo.conflictTran.keys():
                self.Candidatelist = list(set(self.Candidatelist) - {TranWithInfo.conflictTran[self.getName()]})
        return self.Candidatelist
    #移除迁移
    def removeCandidate(self, CandidateTran):
        self.Candidatelist.remove(CandidateTran)
    #新的迁移列表替代原迁移列表
    def replaceCandidatelist(self, newCandidatelist):
        self.Candidatelist = newCandidatelist
    #获取迁移名字
    def getName(self):
        return self.tran.name


class PartialList:


    usePercent = None  # type: List[int]

    def __init__(self, targetBranch, starttime):
        # traninforlist = obtain_efsm_info.obtain_tran_info()
        self.targetBranch = targetBranch
        #处理目标分支
        while '.' in self.targetBranch.event:
            self.targetBranch.event = self.targetBranch.event.replace('.', '')
        while '.' in self.targetBranch.cond:
            self.targetBranch.cond = self.targetBranch.cond.replace('.', '')
        while '.' in self.targetBranch.action:
            self.targetBranch.action = self.targetBranch.action.replace('.', '')
        # self.targetBranchSrcList = obtain_efsm_info.getOppositeBranch(self.targetBranch) #返回目标分值起始节点
        self.targetBranchSrcList = obtain_efsm_info.getSecondOppositeBranch(self.targetBranch) #返回目标分值起始节点
        # self.targetBranchSrcList = obtain_efsm_info.tragetState() #返回目标分值起始节点
        self.useList = []
        self.tranlist = [] #部分序列
        self.eventDefList = set
        self.sortKaiGuan = 1
        self.defPercent = config.defPercent  # event action
        self.usePercent = config.usePercent  # cond action
        self.sorttime = 0
        self.sortnum = 0
        #------------rinsmq
        self.defUseList = [] #保存使用已定义的变量
        #------------rinsmq
        print (self.targetBranchSrcList)
        if self.targetBranchSrcList is not None:
            print ("候选的目标分支插入点列表：",(self.targetBranchSrcList, time.time() - starttime))
            # STATE = EFSM.State("State S6")
            # targetBranch.src = STATE
            self.targetBranch.src = self.targetBranchSrcList[0]
            self.targetBranchSrcList.pop(0)
            originTran = TranWithInfo(self.targetBranch)
            originTran.quality = 'relate'
            # print 'originTran=',originTran
            self.useList = list(set(originTran.getvUseList()) - set(originTran.getveventVdef())) #当前迁移使用变量减去当前迁移定义变量，为当前迁移使用变量
            self.tranlist.append(originTran)
            self.eventDefList = set(originTran.getveventVdef())

        else:
            print ("目标分支无对立分支")

        # 一些后面需要用到的东西

    def __repr__(self):
        # return "<PartialList %s %s %s %s>" % (self.currentPartialList, self.nameList,self.vUseList,self.Candidatelist)
        return "<PartialList %s>" % ([item.getName() for item in reversed(self.tranlist)])
    #获取目标分支信息，目标分支起始节点修改为targetBranchSrcList[0]
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
    #添加迁移信息
    def push(self, tranWithInfo):
        self.tranlist.append(tranWithInfo)
    #在部分序列中移除一条迁移
    def pop(self):
        if len(self.tranlist) > 0:
            self.eventDefList = set(self.eventDefList) - set(self.top().getveventVdef())
            self.tranlist.pop()
        else:
            print ("部分迁移序列为空！")
    #返回部分序列顶部迁移
    def top(self):
        return self.tranlist[-1]
    # 保存使用已定义的变量
    def flushdefUseList(self):
        self.defUseList = []
        useVarlist = []
        defVarlist = []
        for item in self.tranlist:
            print ('item=', item)
            defVarlist = item.getvDefList()
            self.defUseList.extend(set(defVarlist) & set(useVarlist))
            print ('defVarlist=', defVarlist)
            midVar = (set(item.getvUseList()) & set(item.getveventVdef()))  # 排除自己定义自己使用的情况
            useVarlist = list(set(useVarlist) | (set(item.getvUseList()) - midVar))
            # print 'useVarlist=',useVarlist

        self.defUseList = set(self.defUseList)
        # print 'defUseList= ',self.defUseList

    #刷新使用变量 self.uselist保存使用但未定义的变量
    def flushUseList(self):
        self.useList = []
        for item in self.tranlist:
            self.useList = [tmp for tmp in self.useList if tmp not in item.getvDefList()]
            # print 'uselist=',self.useList
            self.useList.extend(item.getvUseList())
            # print 'uselist=', self.useList
            self.useList = list(set(self.useList) - set(item.getveventVdef()))
            # print 'uselist=', self.useList
            # print 'item=',item
    #移除候前序迁移中已选择过的迁移
    def removeCandidate(self, CandidateTran):
        self.tranlist[-1].removeCandidate(CandidateTran)

    @property
    #获取候选前序迁移集
    def getCandidatelist(self):
        # firsttime = time.time()
        tmplist = self.tranlist[-1].getCandidatelist()  # 获取栈顶迁移的前序迁移
        print (self.tranlist)
        print ('tmplist=',tmplist)
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
                # print '栈顶迁移的前序迁移tmplist= ',tmplist
                atmplist = [item for item in tmplist if len(set(item.getvDefList()) & set(self.useList)) >= 1]  # 筛选相关迁移
                # rinsmq------------------start
                print ('具有数据相关前序迁移atmplist= ', atmplist)
                self.flushdefUseList()
                self.flushUseList()
                # print 'self.defUseList= ', self.defUseList
                if self.sortKaiGuan == 1 and len(atmplist) >= 1:
                    # print 'rinsmq-start'
                    # print 'priority_use_defition'
                    tmplist = atmplist
                    for tran in tmplist:
                        tran.quality = 'relate'

                    if config.useNodefition == 1:
                        # 按照使用未定义变量优先排序
                        tmplist = self.priority_use_no_definition(tmplist)
                    if config.eventSort == 1:
                        # 按照事件变量优先排序
                        tmplist = self.eventVdef(atmplist)
                    if config.penaltyValue == 1:
                        # 按照惩罚值优先排序
                        tmplist = self.Penalty_value(tmplist)
                    if config.togeSort == 1:
                        # 所有排序共同排序
                        tmplist = sorted(tmplist, key=lambda x: (x.OnePriority,x.TwoPriority,x.ThrPriority))  # 未验证

                # #rinsmq-------------------end
                # if (self.sortKaiGuan == 1 or self.sortKaiGuan == 2) and len(atmplist) >= 1:  # 如果存在相关迁移，且原迁移未筛选过
                #     tmplist = atmplist
                #     for tran in tmplist:
                #         tran.quality = 'relate'
                #     if config.yrzswgbl == 1:
                #         print " 按引入变量的多少排序"
                #         tmplist = sorted(tmplist,
                #                         key=lambda x: len(x.getvcondVuse()) * self.usePercent[0] + len(x.getvactionVuse()) * self.usePercent[1])  # 按引入变量的多少排序，少的优先
                #     if config.achcdpx == 1:
                #         print "按重合程度排序"
                #         tmplist = sorted(tmplist,key=self.achcdpx, reverse=True)  # 按重合程度排序
                #     if config.achxhpx == 1:
                #         print "按重合先后排序"
                #         tmplist = sorted(tmplist, key=self.achxhpx)  # 按重合先后排序
                #     if config.hhpx == 1 and len(tmplist)>1:
                #         if self.achcdpx(tmplist[0]) == self.achcdpx(tmplist[1]):
                #             print "混合排序"
                #             tmplist = sorted(tmplist, key=self.hhpx, reverse=True)  # 混合排序
                #     # self.sortnum += 1;
                # if (self.sortKaiGuan == 1 or self.sortKaiGuan == 3) and len(atmplist) < 1:
                #
                #     tmplist = sorted(tmplist, key=lambda x: len(set(x.getvUseList()) - set(x.getveventVdef())))
                #     for tran in tmplist:
                #         tran.quality = 'noRelate'
                #     # self.sortnum += 1;
                # if config.newtransort == 1:
                #     tmplist = sorted(tmplist, key=self.isNewTran, reverse=True)
                # # self.sorttime += time.time() - firsttime
                # if (self.sortKaiGuan == 3 and len(atmplist) >= 1)or(self.sortKaiGuan == 2 and len(atmplist) < 1):
                #     tmplist=tmplist
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
        # print('^^^^^^^^^^^^^^^^^')
        # for tra in tmplist:
        #     print tra
        # print('^^^^^^^^^^^^^^^^^')
        return tmplist


    #-------------------rinsmq

    # 前序迁移中定义变量与部分序列使用已被定义的变量交集越大，优先级越高
    def priority_use_definition(self,tmplist):
        # print '前序迁移优先级准则：'
        # print 'defUseList=',self.defUseList
        for transition in tmplist:
            defSet = set(transition.getvDefList())
            # print 'transition=', transition
            # print 'defSet=', defSet
            useDefinition = list(defSet & set(self.defUseList))
            transition.priority = len(useDefinition)
        atmplist = sorted(tmplist, key = lambda transition: transition.priority, reverse=True)
        return atmplist
    # 前序迁移中定义变量与部分序列使用但未被定义的变量交集越大，优先级越高
    def priority_use_no_definition(self,tmplist):
        print ('使用但未被定义优先级高')
        for transition in tmplist:
            # 获取迁移定义变量
            defSet = set(transition.getvDefList())
            useNotdefinition = list(defSet & set(self.useList))
            transition.OnePriority = len(useNotdefinition)
        atmplist = sorted(tmplist,key=lambda transition: transition.OnePriority,reverse=True)
        # for transition in atmplist:
        #     print 'transition=',transition
        #     print transition.priority
        return atmplist

    # 前序迁移event变量越少优先级越高
    def eventVdef(self,tmplist):
        print ('事件变量少优先')
        for transition in tmplist:
            defSet = transition.getveventVdef()
            defLen = len(defSet)
            transition.TwoPriority = transition.TwoPriority + defLen
        atmplist = sorted(tmplist,key=lambda transition: transition.TwoPriority,reverse=True)
        return atmplist

    # 前序迁移cond惩罚值 未完成
    # compute cond penalty value
    def Penalty_value(self,tmplist):
        print ('惩罚值越小优先级高')
        for transtion in tmplist:
            # 求每个迁移cond惩罚值
            statements = transtion.cond
            conValue = 0
            for stat in statements.split(";"):
                sclexer.lex.input(stat)
                while 1:
                    tok = sclexer.lex.token()
                    print ('tok=', tok)
                    if not tok:
                        break
                    else:
                        print (tok.type)
                        if tok.type == 'ID':
                            print (tok.value)
                        if tok.type == 'EQ':  # '=='
                            conValue += 16
                        if tok.type == 'GE':  # '>='
                            conValue += 10
                        if tok.type == 'LE':  # '<='
                            conValue += 10
                        if tok.type == 'GT':  # '>'
                            conValue += 11
                        if tok.type == 'LT':  # '<'
                            conValue += 11
                        if tok.type == 'NE':  # '!='
                            conValue += 1

            transtion.ThrPriority = transtion.ThrPriority+conValue
        atmplist = sorted(tmplist, key=lambda transition: transition.ThrPriority)
        return atmplist

    #-------------------rinsmq


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
    #返回是否搜索到模型开始节点
    def isComplete(self):
        # print "--------isComplete()----------"
        # print self.tranlist, self.useList
        # print "-----------------------------"
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

#得到不可行序号
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

    print ('selected_tran=',selected_tran)
    print ('actionDefList=',actionDefList)

    # 分析action
    tmpDic = {}

    for actionDef in actionDefList:
        judge = re.search(actionDef + '[^;]*(?=;{0,1})', selectedTranAction)  # 这里实际上是假设了都是形如a=xxx的形式
        if judge is not None:  # 分四种情况讨论
            judge = judge.group()
            if '=' in judge:
                pos = judge.find('=')
                strDef = judge[pos + 1:].strip()
                leftstrDef = judge[0:pos].strip()
                #包含外部变量的直接跳
                if strDef in eventDefList:
                    eventDefList.add(leftstrDef)  # 拓展，次级外部输入
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
    # for k,v in tmpDic.items():
    #     print k,v
    if len(tmpDic) > 0:  # 只有action存在定义的时候才有可能不可行
        for i in range(len(tran_list) - 1, -1, -1):
            item = tran_list[i]
            # print 'item=',item
            # print item.getvcondVuse()
            # print eventDefList
            if len(item.getvcondVuse()) > 0:
                flag = True
                for cond in item.getvcondVuse():  # 全都要已存在定义
                    if cond not in tmpDic and cond not in eventDefList:
                        flag = False
                        break
                if flag:
                    cond = item.tran.cond[:]
                    # print 'cond=',cond
                    for condUse in item.getvcondVuse():
                        if condUse in eventDefList:
                            stra = re.search("!{0,1}\([^(]*" + condUse + '[^)]*\)', cond)
                            if stra:
                                stra = stra.group()
                                # print 'stra1=', stra
                                cond = cond.replace(stra, 'True')
                            strb = re.search("[^&|(]*" + condUse + '[^&|)]*', cond)
                            if strb:
                                strb = strb.group()
                                # print 'strb=', strb
                                cond = cond.replace(strb, 'True')
                    cond = cond.replace('!(', ' not (')
                    cond = cond.replace('&&', ' and ')
                    cond = cond.replace('&', ' and ')
                    cond = cond.replace('|', ' or ')
                    # print "判断条件：%s" % (cond)
                    while '(True)' in cond or 'True and True' in cond:
                        cond = cond.replace('not (True)', 'True')
                        cond = cond.replace('(True)', 'True')
                        cond = cond.replace('True and True', 'True')
                    # print item.tran.name
                    # print "判断条件：%s" % (cond)
                    tmpDic['isFeasibilityBeforeCorrect'] = True
                    exec ("if not (" + cond + "):\n\tisFeasibilityBeforeCorrect = False", tmpDic)
                    # print '============================start'
                    # for k,v in tmpDic.items():
                    #     print k,v
                    # print '============================end'
                    if not tmpDic['isFeasibilityBeforeCorrect']:
                        return i

            for actionDef in item.getvactionVdef():
                judge = re.search(actionDef + '[^;]*(?=;{0,1})', item.tran.action)  # 这里实际上是假设了都是形如a=xxx的形式
                if judge is not None:  # 分四种情况讨论
                    judge = judge.group()
                    if '=' in judge:
                        pos = judge.find('=')
                        strDef = judge[pos + 1:].strip()
                        leftstrDef = judge[0:pos].strip()
                        # print 'strDef=',strDef
                        # print 'leftstrDef=',leftstrDef
                        # 包含外部变量的直接跳
                        if strDef in eventDefList:
                            # eventDefList.add(strDef)  # 拓展，次级外部输入  错误，待修改
                            eventDefList.add(leftstrDef)  # 拓展，次级外部输入  错误，待修改
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

#搜索
def search():
    # 初始化：name, src=None, tgt=None, event=None, cond=None, action=None
    operator = ['+', '-', '*', '/']  # 4种情况
    loopLimit = config.loopLimit
    numOfPSG = config.numOfPSG
    psDict = {}
    psDict1 = {}
    psDict2 = {}
    psDict3 = {}
    while numOfPSG > 0:
        #print 'num=%s'%(numOfPSG)
        numOfPSG = numOfPSG - 1
        starttime = time.time()

        partialList = PartialList(obtain_efsm_info.targetBranch(), starttime)

        partialList.sortKaiGuan = config.sort  # 排序开关 1是排序； 0是全随机，除了候选对立分支； 2是连接迁移随机
        # partialList = PartialList(obtain_efsm_info.getTran(70))
        valueDict = {}
        # print partialList
        if partialList.targetBranchSrcList is not None:
            while partialList.isComplete() == 2 or ( partialList.isComplete() == 0 and len(partialList.targetBranchSrcList) > 0):

                if partialList.isComplete() == 0 and len(partialList.targetBranchSrcList) > 0:
                    # print '执行newTargetSrc'
                    partialList.newTargetSrc()
                print ("一次执行前的部分序列" , (partialList, time.time() - starttime))
                # print '获取前序迁移候选集合：'
                candidateList = partialList.getCandidatelist
                print ("前序候选迁移集合:", (candidateList))
                # print len(candidateList)
                if len(candidateList) == 0:
                    if config.back == 1:
                        # print 'pop之前：'
                        # print partialList
                        partialList.pop()
                        # print 'pop之后：'
                        # print partialList
                        # continue
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
                selectedTran = candidateList[0]
                partialList.removeCandidate(selectedTran)
                # print partialList.top().getCandidatelist()
                if selectedTran.tran == partialList.top().tran:  # 最优先候选迁移是序列首个迁移本身的情况
                    continue
                # rinsmq add---------------------------
                pb = 0
                for i in range(len(partialList.tranlist)):
                    # print '执行这个for循环'
                    if partialList.tranlist[i].tran == selectedTran.tran:
                        print ('有相同的')
                        pb = 1
                        break
                if pb == 1:
                    continue
                # rinsmq end-------------------------------
                isFeasibility = True
                # 判断是否矛盾变量冲突
                selectedTranCond = selectedTran.tran.cond
                for item in reversed(partialList.tranlist):
                    cond = item.tran.cond
                    opposeCond = "!(" + cond + ")"    #判断矛盾变量冲突只判断在原条件上多个‘！’或者少个‘！’？
                    # print opposeCond
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
                    print ("矛盾变量冲突")
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
                # print actionDefList
                for actionDef in actionDefList:
                    judge = re.search(actionDef + '[^;]*(?=;{0,1})', selectedTranAction)  # 这里实际上是假设了都是形如a=xxx的形式
                    if judge is not None:  # 分四种情况讨论
                        judge = judge.group()
                        # print 'judge=',judge
                        if '=' in judge:
                            pos = judge.find('=')
                            strDef = judge[pos + 1:].strip()
                            # 包含外部变量的直接跳
                            if strDef in eventDefList:
                                eventDefList.add(strDef)  # 拓展，次级外部输入
                                continue
                            '''
                            print time.time()
                            flag = 0
                            for item in eventDefList:
                                if item in strDef:
                                    flag = 1
                                    break
                            if flag == 1:
                                continue
                            print time.time()
                            '''
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
                print ('isFeasibility=',isFeasibility)

                # print (len(tmpDic))
                # for k, v in tmpDic.items():
                #     print k, v
                if len(tmpDic) > 0:
                    print ("开始二阶段可行性判断")
                    num = get_infeasible_order_number(selectedTran, partialList.tranlist, partialList.eventDefList)
                    print (num)
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
                print ('执行到判定完可行性')
                if not isFeasibility:
                    print ("可行性判断无法通过%s" ,(time.time() - starttime))
                    if time.time() - starttime > 1:
                       break
                    continue
                # “纠正”的过程：重复对判断未通过的变量有影响的、对其他变量影响最小的、可重复的、恰当的子序列
                # 现在只处理自循环
                firstFind = []
                for i in range(len(partialList.tranlist)):
                    if partialList.tranlist[i].tran == selectedTran.tran:
                        firstFind.append(i)
                print ('firstFind=',firstFind)
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
                    # partialList.getCandidatelist
                # print "一次执行后的部分序列%s" % (partialList)
                # print "执行后部分序列的变量依赖集:%s %s" % (partialList.useList, time.time() - starttime)
                # print '\n'
                if time.time() - starttime>1:
                    break



        if partialList.isComplete() == 0:
            print ("无任何可行序列")
        else:
            if time.time() - starttime < 1:
                psDict[partialList] = (time.time() - starttime)
                psDict1[partialList] = partialList.sorttime
                psDict2[partialList] = partialList.sortnum
            # print psDict1[partialList]
            # print "已生成序列%s 用时%s" % (partialList, time.time() - starttime)
            #for item in partialList.tranlist:
            #    print ("%s : %s") % (item.getName(), item.quality)
                # pass
    # print '\n'
    res3 = 0
    for item in psDict.keys():
        # print item
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
    sequencenumber=len(psDict)
    # print "生成序列条数为%s" % sequencenumber
    if sequencenumber==0:
        generationtime=0
        generationsorttime=0
        sequencelength=0
        selecenumber=0
        successnumber=0
    else:
        successnumber = 1
        generationtime = res / len(psDict)
        # print "序列生成平均时间为%s" % (generationtime)

        generationsorttime = res1 / len(psDict1)
        # print "优先级排序时间: %s"%(partialList.sorttime)
        # print "优先级排序平均时间: %s" % (generationsorttime)

        sequencelength=float(res3)/float(len(psDict1))
        # print "平均序列长度:"
        print(format(sequencelength,'.2f'))

        selecenumber=float(res2) / float(len(psDict2))
        # print "平均选择次数:"
        print(format(selecenumber, '.2f'))

        #for item in psDict.keys():
        #    for k in item.tranlist:
         #       psDict3[k]=k.getName()
         #   break


    return [item.getName() for item in reversed(partialList.tranlist)]
    #return psDict3.values()




if __name__ == '__main__':
    search()
