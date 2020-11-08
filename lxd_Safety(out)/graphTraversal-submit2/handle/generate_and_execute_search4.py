# encoding:utf-8

import efsmGA.GA.search4 as sequeueGenerate
import generate_data_ga
import seq_to_script
from handle import obtain_efsm_info2
import domanaiyzer
import efsmGA.GA.target as target
import mymodules.EFSM as pathdate
import fileinput


time1=0
count=0
time2=0
number=0
length=0
select=0
flag=0

while target.targetList and flag<=len(target.targetList):

    # 序列生成
    pathT = sequeueGenerate.search()
    time1 += sequeueGenerate.generationtime
    count += sequeueGenerate.successnumber
    number += sequeueGenerate.sequencenumber
    time2 += sequeueGenerate.generationsorttime
    length += sequeueGenerate.sequencelength
    select += sequeueGenerate.selecenumber

    # domanaiyzer.dealbeforeexecute()
    # print pathT
    # 测试数据生成
    # pathT = ['T1','T9','target']
    # SM = obtain_efsm_info2.obtain_efsm()
    # data = generate_data_ga.testProcee(SM, pathT)
    # SM=pathdate.obtain_efsm()
    # data = SM.testGenforPath(pathT)
    # print data
    # 模拟点击
    # SM = obtain_efsm_info2.obtain_efsm()
    # seq_to_script.runcase(SM.TEvent, pathT, data)  # 执行当前序列

    # 模型补全
    # domanaiyzer.fixmodel()

    # print 11111111111111111111111111111111111111111111
    # print target.targetList[0]
    if number == 0:
        flag += 1
        target.sort()
        print target.targetList
    else:
        flag = 0
        target.change()
    # del target.targetList[0]
'''
while target.targetList and flag<=len(target.targetList):
    pathT = sequeueGenerate.search()
    time1 += sequeueGenerate.generationtime
    count += sequeueGenerate.successnumber
    number = sequeueGenerate.sequencenumber
    time2 += sequeueGenerate.generationsorttime
    length += sequeueGenerate.sequencelength
    select += sequeueGenerate.selecenumber
    print target.targetList

    if number==0:
        flag+=1
        target.sort()
        print target.targetList
    else:
        flag=0
        target.change()
'''

print "%s个目标分支生成了序列" % count
print "生成序列条数为%s" % number
print "序列生成平均时间为%s" % (time1/count)
print "优先级排序平均时间: %s" % (time2/count)
print "平均序列长度:"
print(format(length/count,'.2f'))
print "平均选择次数:"
print(format(select/count, '.2f'))