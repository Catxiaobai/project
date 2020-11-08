# -*- coding: UTF-8 -*-
import sys
sys.path.append('E:/Code/project301/lxd_Safety/graphTraversal-submit2') 
import handle.generate_and_execute_search3 as handle
result_list = handle.execute()
with open('E:/Code/project301/file/path.txt','w')as f:
    list1 = list(map(lambda x:int(x.split('t')[1]),result_list))
    f.write(str(list1))