# -*- coding: UTF-8 -*-
import sys
sys.path.append('E:/Code/project301/lxd_Safety/graphTraversal-submit2') 
from Tkinter import *
from PIL import Image,ImageTk,ImageDraw,ImageFont
import handle.generate_and_execute_search3 as handle
import time
import os
import threading


root = Tk()  # 创建窗口对象的背景色
root.geometry('1200x800')


def thread_it(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()


class draw(object):
    def __init__(self):
        super(draw,self).__init__()

    def start(self):
        yuanzu = handle.execute()
        label1.configure(text=yuanzu[1])
        # sys.path.append("D:/graphTraversal-submit2/efsmGA/model/")
        writepath = r'E:/Code/project301/file/'
        filepath = r'E:/Code/project301/file/'
        filename = r'webchess'
        length = len(yuanzu[0])
        w = 1
        new_list = []
        flag_list = []   # 标记列表
        while w <= length:
            flag_name = TRUE
            for j in range(w):
                new_list.append(yuanzu[0][j])
            with open(writepath + filename + '.dot', 'w+') as fout:
                fout.writelines("digraph g {\n")
                fout.writelines("ratio = 1.25 \n")

                with open(filepath + filename + '.txt', 'r') as f:
                    line = f.readlines()
                    global tgt1
                    node_f = FALSE
                    for i in range(0, len(line)):
                        if "Transition:" in line[i]:
                            name = line[i + 1].split("name=")[1].replace('\r', '').replace('\n', '')
                            src = line[i + 2].split("src=")[1].replace('\r', '').replace('\n', '')
                            tgt = line[i + 3].split("tgt=")[1].replace('\r', '').replace('\n', '')
                            event = None
                            cond = None
                            action = None
                            # event = line[i + 4].strip().split(';')[0].replace('\r', '').replace('\n', '') #增加event信息
                            # cond = line[i + 5].strip().replace('\r', '').replace('\n', '') #增加cond信息
                            # action = line[i + 6].strip().replace('\r', '').replace('\n', '') #增加action信息
                            i = i + 6
                            fout.writelines(" " + src + " -> " + tgt + ' [ label="' + name + '"')
                          
                            if name in new_list:
                                if name not in flag_list :
                                    flag_list.append(name)
                                    fout.writelines(',color = red')
                                    node_f = True
                                    tgt1 = tgt
                                else:
                                    if new_list[w-1] != name:
                                        fout.writelines(',color = red')
                                        node_f = True

                                    else:
                                        fout.writelines(',color = black')

                                        flag_list.remove(name)
                                        flag_name = FALSE
                            if event != None:
                                fout.writelines('\n' + event)
                            if cond != None:
                                fout.writelines('\n' + cond)
                            if action != None:
                                fout.writelines('\n' + action)
                            fout.writelines('];\n')
                            # if flag == 1:
                            #     fout.writelines("node [filename = \""+tgt+"\",shape =\"egg\",color = \"red\" ]\n")
                    if node_f:

                        fout.writelines(tgt1+"[color=red]")
                    #flag_node = yuanzu[1]
                    #fout.writelines(flag_node+"[color=red]")
                fout.writelines("}\n")
            if flag_name == FALSE:
                w = w-1
            w = w + 1
            new_list = []
            os.popen(
                "dot -Tpng E:/Code/project301/file/{}.dot -o E:/Code/project301/file/{}.gif".format(
                    filename, filename))
            img = Image.open(filepath+"webchess.gif")
            img.thumbnail((1000, 800))
            global photo
            photo = ImageTk.PhotoImage(img)
            lalel2.configure(image=photo)

            time.sleep(1)
draw1 = draw()

Button (root,text = '确定',command = lambda:thread_it(draw1.start)).pack()
label1 = Label(root)
label1.pack()
lalel2 = Label(root)
lalel2.pack()


root.mainloop()