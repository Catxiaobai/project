#!/usr/bin/python
#incoding:UTF-8
from Model3.ConstructModel1 import getTransState1,ConstructModel1
from Model3.completeModel1 import completeModel1
from Model3.judgeModelComplete import judgeModelComplete1

if __name__ == "__main__":
    # # #从Trace里获取状态集和迁移集
    # StateSet,TransSet,TraceSet=getTransState1()
    # # #合并状态和迁移
    TraceSet,StateSet,TransSet,State2,T=ConstructModel1()
    # # #模型完整性ConConstructModel1.pystructModel1.py验证及补全
    State2,counterCondSet=judgeModelComplete1()
    # completeModel1(TraceSet,StateSet, TransSet, State2, T)
    completeModel1()
