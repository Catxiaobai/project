# encoding:utf-8

import efsmGA.GA.search2 as sequeueGenerate
import generate_data_ga
import seq_to_script
from handle import obtain_efsm_info2
import domanaiyzer
import efsmGA.GA.target as target
import mymodules.EFSM as pathdate
import fileinput
import time


time1=0
count=0
time2=0
number=0
length=0
select=0
flag=0
iteration=0
while target.targetbranchlist and flag <= len(target.targetbranchlist):

    # 序列生成
    pathT = sequeueGenerate.search()
    time1 += sequeueGenerate.generationtime
    count += sequeueGenerate.successnumber
    number += sequeueGenerate.sequencenumber
    time2 += sequeueGenerate.generationsorttime
    length += sequeueGenerate.sequencelength
    select += sequeueGenerate.selecenumber
    iteration+=1
    print pathT
    print 1111111111111111111111111111

    for item in pathT:
        #path=[item.getName() for item in reversed(item.tranlist)]
        print item


    if sequeueGenerate.sequencenumber == 0:
        flag += 1
        target.sort()
        print flag
        print 1111111111111111111111111111111
    else:
        domanaiyzer.dealbeforeexecute()
        flag = 0
        target.change()


print "迭代次数为%s" % iteration
print "%s个目标分支生成了序列" % count
print "生成序列条数为%s" % number
print "序列生成平均时间为%s" % (time1/count)
print "优先级排序平均时间: %s" % (time2/count)
print "平均序列长度:"
print(format(length/count,'.2f'))
print "平均选择次数:"
print(format(select/count, '.2f'))