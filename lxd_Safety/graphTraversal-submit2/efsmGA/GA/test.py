# encoding:UTF-8
import obtain_efsm_info
import re
from graphviz import Digraph


class TranWithInfo:
    conflictTran = {}

    def __repr__(self):
        return "<Transition %s>" % (self.tran.name)

    def __init__(self, tran):
        self.tran = tran
        self.vDUDict = obtain_efsm_info.getSimplevDefUseList(self.tran)
        self.Candidatelist = []
        self.candidateinitflag = 0
        self.sortedflag = 0

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
            self.Candidatelist = [item for item in self.Candidatelist if
                                  item.getName() not in TranWithInfo.conflictTran]
        return self.Candidatelist

    def removeCandidate(self, CandidateTran):
        self.Candidatelist.remove(CandidateTran)

    def replaceCandidatelist(self, newCandidatelist):
        self.Candidatelist = newCandidatelist

    def getName(self):
        return self.tran.name


class PartialList:

    def __init__(self, targetBranch):
        # traninforlist = obtain_efsm_info.obtain_tran_info()
        self.targetBranchSrcList = obtain_efsm_info.getOppositeBranch(targetBranch)
        targetBranch.src = self.targetBranchSrcList[0]
        originTran = TranWithInfo(targetBranch)
        self.useList = originTran.getvUseList()
        self.tranlist = []
        self.tranlist.append(originTran)
        self.eventDefList = originTran.getveventVdef()
        self.kaiguan = 1 #开关，1代表优先级排序，0代码全随机

    def __repr__(self):
        # return "<PartialList %s %s %s %s>" % (self.currentPartialList, self.nameList,self.vUseList,self.Candidatelist)
        return "<PartialList %s>" % ([item.getName() for item in self.tranlist])

    def push(self, tranWithInfo):
        self.tranlist.append(tranWithInfo)

    def pop(self):
        if self.tranlist is not []:
            self.tranlist.pop()
        else:
            print "部分迁移序列为空！"

    def top(self):
        return self.tranlist[-1]

    def flushUseList(self):
        self.useList = []
        for item in self.tranlist:
            '''
            for vUse in self.useList:  # 循环删除已有定义的使用变量
                if vUse in item.getvDefList():
                    self.useList.remove(vUse)
            '''
            self.useList = [vUse for vUse in self.useList if vUse not in item.getvDefList()]
            self.useList.extend(item.getvUseList())
            #for vUse in item.getvUseList():
            #    self.useList.append(vUse)
            self.useList = list(set(self.useList) - set(item.getveventVdef()))
            #print "加入的定义集:%s"%(item.getvDefList())
            #print self.useList
        #print '\n'

    def removeCandidate(self, CandidateTran):
        self.tranlist[-1].removeCandidate(CandidateTran)

    def getCandidatelist(self):
        tmplist = self.tranlist[-1].getCandidatelist()  # 获取栈顶迁移的前序迁移
        print 'tmplist'
        print tmplist
        atmplist = []
        if self.kaiguan == 1 and self.tranlist[-1].sortedflag == 0:
            ''''''
            for item in tmplist:
                print "vDEF%s" % (item.getvDefList())
                print "useList%s" % (self.useList)
                if len(set(item.getvDefList()) & set(self.useList)) >= 1:
                    atmplist.append(item)
            ''''''
            # atmplist = [item for item in tmplist if len(set(item.getvDefList()) & set(self.useList)) >= 1]  # 筛选相关迁移
            if len(atmplist) >= 1:  # 如果存在相关迁移，且原迁移未筛选过
                tmplist = atmplist
                print "atmpList%s" % (atmplist)
                tmplist = sorted(tmplist, key=lambda x: len(set(x.getvDefList()) & set(self.useList)),
                                 reverse=True)  # 按重合程度排序
                tmplist = sorted(tmplist,
                                 key=lambda x: (len(set(x.getvDefList()) & set(self.useList)) + 1) / (
                                         len(self.useList) + 1),
                                 reverse=True)
                tmplist = sorted(tmplist, key=self.achxhpx)  # 按重合先后排序
            else:  # 全是连接迁移，根据引入的无关变量的多少排序，少的优先
                tmplist = sorted(tmplist, key=lambda x: len(x.getvUseList()), reverse=True)
            tmplist = sorted(tmplist, key=self.isNewTran)
            self.tranlist[-1].sortedflag = 1
            self.tranlist[-1].replaceCandidatelist(tmplist)
        return tmplist

    def achxhpx(self, tran):  # 按重合先后排序
        dist = 0
        for item in reversed(self.tranlist):
            dist += 1
            if len(set(tran.getvDefList()) & set(item.getvUseList())) != 0:
                break
        return dist

    def isNewTran(self, tran):
        if tran in self.tranlist:
            return 1
        return 0

    def isComplete(self):
        if len(self.tranlist) == 0:  # 目标分支出发的所有路径全无法达成
            return 0
        if self.tranlist[-1].tran.src.name == "START" and len(self.useList) == 0:  # 成功的情况
            return 1
        else:
            return 2  # 其余情况

'''
partialList = PartialList(obtain_efsm_info.getTran(16))
partialList.push(TranWithInfo(obtain_efsm_info.getTran(4)))
print partialList.tranlist[-1].getCandidatelist()
partialList.flushUseList()
#print partialList.useList
partialList.push(TranWithInfo(obtain_efsm_info.getTran(1)))
partialList.flushUseList()
#print partialList.useList

judge = re.search('attempts[^;]*(?=;{0,1})', 'write("Enter PIN"); attempts = 0;;').group()
#print judge

if ((True)) :
    print 1
'''
stra = re.search('documentusersselectuservalue[^;]*(?=;{0,1})', "documentusersselectuservalue = documentusersselectuservalue + 1")
stra = stra.group()
print stra
documentusersselectuservalue = 0
exec "documentusersselectuservalue = documentusersselectuservalue + 1"
print documentusersselectuservalue
'''
fout = open(r'../subjects/JSefsm2.txt', 'w+')
with  open(r'../subjects/JSefsm.txt' , 'r') as f:
    for line in f.readlines():
        if '	filename=' not in line:
            fout.writelines(line)
'''
'''
dot = Digraph(comment='The Round Table')

# 添加圆点 A, A的标签是 King Arthur
dot.node('A', 'king')
#dot.view()  #后面这句就注释了，也可以使用这个命令查看效果

# 添加圆点 B, B的标签是 Sir Bedevere the Wise
dot.node('B', 'Sir Bedevere the Wise')
#dot.view()

# 添加圆点 L, L的标签是 Sir Lancelot the Brave
dot.node('L', 'Sir Lancelot the Brave')
#dot.view()

#创建一堆边，即连接AB的边，连接AL的边。
dot.edges(['AB', 'AL'])
#dot.view()

# 在创建两圆点之间创建一条边
dot.edge('B', 'L', constraint='false')
#dot.view()

# 获取DOT source源码的字符串形式
print(dot.source)

# 保存source到文件，并提供Graphviz引擎
dot.render('test-output/round-table.gv', view=True)
dot.attr('graph',rankdir='LR')
'''

#lista = input()
#listb = input()
lista = [int(temp) for temp in input().split()]
print lista
if 'a' not in lista:
'''
if len(lista) == 2:
    m, n = lista
else:
    m = int(lista)
    n = int(input())
print n+m
'''