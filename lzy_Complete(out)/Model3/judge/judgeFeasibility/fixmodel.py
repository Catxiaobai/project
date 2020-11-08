# -*- coding: UTF-8 -*-
import io
import operator
import os
import time
import sys
import time
s = []  # 创建一个空列表
soup = []
def readstate():
    path = "../efsmGA/states/"  # 指定需要读取文件的目录
    filetype = '.html'  # 指定文件类型

    files = os.listdir(path)  # 采用listdir来读取所有文件
    files.sort()  # 排序

    for file_ in files:  # 循环读取每个文件名
        #    print(path +file_)
        if not os.path.isdir(path + file_):  # 判断该文件是否是一个文件夹
            if filetype in file_:
                s.append(file_.replace(filetype, ''))
                f_name = str(file_)
                # print s[0]
                # s.append(f_name)  # 把当前文件名返加到列表里

    statesfiledir = '../efsmGA/states/'
    for i in range(len(s)):
        statesfile = s[i]
        statespath = statesfiledir + statesfile + filetype
        htmlfile = io.open(statespath, 'r', encoding='utf-8')
        htmlhandle = htmlfile.read()
        soup.append(BeautifulSoup(htmlhandle, 'lxml'))  # 选择lxml作为解析器
        # print(s[i], soup[i].find_all())


def isdomsame(i):
    s1 = []
    s2 = []
    for child in soup[i].html.descendants:
        # print(child.name)
        s1.append(child.name)
    for child in soup[len(s) - 1].html.descendants:
        # print(child.name)
        s2.append(child.name)

    if s1 == s2:
        return 1
    else:
        return 0



def fixmodel():
    readstate()
    flag = 1  # 触发状态为新状态

    starttime = time.time()
    target=PartialList(obtain_efsm_info.targetBranch(),starttime).targetBranch
    target.tgt = s[-1]
    target.src=bytes(target.src).split(' ')[1][:-1]
    # print target.src
    f1 = open("../efsmGA/states/oldstates_name.txt", 'a+')
    if flag == 1:  # 加入迁移边和新状态
        f1.write('Transition:'+ '\n\t'+'name='+target.name+'\n\t'+'src='+target.src+ '\n\t'+'tgt='+target.tgt+ '\n\t'+'event='+target.event+ '\n\t'+'cond='+target.cond+ '\n\t'+'action='+target.action)

        f2 = open("../efsmGA/states/oldstates_name.txt", 'r')
        content = f2.read()
        post = content.find('State:')
        if post != -1:
            content = content[:post] + 'State:\n\tname='+target.tgt+'\n'+ content[post:]
            f2 = open("../efsmGA/states/oldstates_name.txt", 'w')
            f2.write(content)
        f2.close()
    elif flag == 0:  #只加入迁移边
        f1.write('Transition:' + '\n\t' + 'name=' + target.name + '\n\t' + 'src=' + target.src + '\n\t' + 'tgt=' + target.tgt + '\n\t' + 'event=' + target.event + '\n\t' + 'cond=' + target.cond + '\n\t' + 'action=' + target.action + '\n')

    f1.close()