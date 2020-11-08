# encoding:UTF-8
import re
import os
import sys
import handle.generate_and_execute_search3 as han

def sign(pathT):
    # sys.path.append("D:/graphTraversal-submit2/efsmGA/model/")
    writepath = r'E:/Code/project301/file/'
    filepath = r'E:/Code/project301/file/'
    filename = r'webchess'
    length = len(pathT)
    w=1
    new_list = []
    while w <= length:
        for j in range(w):
            new_list.append(pathT[w-1])
        with open(writepath+filename+'.dot', 'w+') as fout:
            fout.writelines("digraph g {\n")
            with open(filepath+filename+'.txt', 'r') as f:
                line = f.readlines()
                for i in range(0, len(line)):
                    if "Transition:" in line[i]:
                        name = line[i+1].split("name=")[1].replace('\r', '').replace('\n', '')
                        src = line[i + 2].split("src=")[1].replace('\r', '').replace('\n', '')
                        tgt = line[i + 3].split("tgt=")[1].replace('\r', '').replace('\n', '')
                        event = None
                        cond = None
                        action = None
                        #event = line[i + 4].strip().split(';')[0].replace('\r', '').replace('\n', '') #增加event信息
                        #cond = line[i + 5].strip().replace('\r', '').replace('\n', '') #增加cond信息
                        #action = line[i + 6].strip().replace('\r', '').replace('\n', '') #增加action信息
                        i = i + 6
                        fout.writelines(" " + src + " -> " + tgt + ' [ label="' + name + '"')

                        if name in new_list:
                            fout.writelines(',color = red')

                        if event != None:
                            fout.writelines('\n' + event)
                        if cond != None:
                            fout.writelines('\n' + cond)
                        if action != None:
                            fout.writelines('\n' + action)
                        fout.writelines('];\n')
            fout.writelines("}\n")
        w = w+1
        new_list = []
        os.popen("dot -Tpng E:/Code/project301/file/{}.dot -o E:/Code/project301/file/{}.png".format(filename, filename))

