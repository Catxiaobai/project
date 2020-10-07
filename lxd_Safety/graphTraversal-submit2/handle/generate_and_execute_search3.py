# encoding:utf-8

import efsmGA.GA.search3 as sequeueGenerate
import generate_data_ga
import seq_to_script
from handle import obtain_efsm_info2
import domanaiyzer
import efsmGA.GA.target as target
import mymodules.EFSM as pathdate
import fileinput
import re
import os
import sys

def execute():
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
        # print pathT
        # print "\n"
        if len(pathT):
            pathT.pop(len(pathT)-1)
        # print pathT
        # print 1111111111111111111111111111
        #print domanaiyzer.target.src


        # sys.path.append("D:/graphTraversal-submit2/efsmGA/model/")
        # writepath = r''
        # filepath = r''
        # filename = r'webchess'
        #
        # with open(r"D:/graphTraversal-submit2/efsmGA/model/" + writepath + filename + '.dot', 'w+') as fout:
        #     fout.writelines("digraph g {\n")
        #     with open("D:/graphTraversal-submit2/efsmGA/model/" + filepath + filename + '.txt', 'r') as f:
        #         line = f.readlines()
        #         for i in range(0, len(line)):
        #             if "Transition:" in line[i]:
        #                 name = line[i + 1].split("name=")[1].replace('\r', '').replace('\n', '')
        #                 src = line[i + 2].split("src=")[1].replace('\r', '').replace('\n', '')
        #                 tgt = line[i + 3].split("tgt=")[1].replace('\r', '').replace('\n', '')
        #                 event = None
        #                 cond = None
        #                 action = None
        #                 # event = line[i + 4].strip().split(';')[0].replace('\r', '').replace('\n', '') #增加event信息
        #                 # cond = line[i + 5].strip().replace('\r', '').replace('\n', '') #增加cond信息
        #                 # action = line[i + 6].strip().replace('\r', '').replace('\n', '') #增加action信息
        #                 i = i + 6
        #                 fout.writelines(" " + src + " -> " + tgt + ' [ label="' + name + '"')
        #
        #                 if name in pathT:
        #                     fout.writelines(',color = red')
        #
        #                 # if event != None:
        #                 #     fout.writelines('\n' + event)
        #                 # if cond != None:
        #                 #     fout.writelines('\n' + cond)
        #                 # if action != None:
        #                 #     fout.writelines('\n' + action)
        #                 fout.writelines(' ];\n')
        #     fout.writelines("}\n")
        #     fout.close()
        #
        # os.popen(
        #     "dot -Tpng D:/graphTraversal-submit2/efsmGA/model/{}.dot -o D:/graphTraversal-submit2/efsmGA/model/{}.png".format(
        #         filename, filename))



        # print 11111111111111111111111111111111111111111111
        # print target.targetList[0]
        if sequeueGenerate.sequencenumber == 0:
            flag += 1
            target.sort()
            #print target.targetbranchlist
            # print flag
            # print 1111111111111111111111111111111
        else:
            global a
            a = domanaiyzer.dealbeforeexecute()

            # print pathT
            # 测试数据生成
            # pathT = ['T1','T9','target']
            #SM = obtain_efsm_info2.obtain_efsm()
            #data = generate_data_ga.testProcee(SM, pathT)
            # SM=pathdate.obtain_efsm()
            # data = SM.testGenforPath(pathT)
            #print data
            # 模拟点击
            #SM = obtain_efsm_info2.obtain_efsm()
            #seq_to_script.runcase(SM.TEvent, pathT, data)  # 执行当前序列

            # 模型补全
            #domanaiyzer.fixmodel()

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
    #print "迭代次数为%s" % iteration
    #print "%s个目标分支生成了序列" % count
    #print "生成序列条数为%s" % number
    #print "序列生成平均时间为%s" % (time1/count)
    #print "优先级排序平均时间: %s" % (time2/count)
    #print "平均序列长度:"
    #print(format(length/count,'.2f'))
    #print "平均选择次数:"
    #print(format(select/count, '.2f'))
    return pathT

