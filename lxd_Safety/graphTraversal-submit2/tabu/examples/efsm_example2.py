import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../subjects")
import os
import sys

import EFSM1
import lusst
import lusst.SM as LSM
import lusst.Skip as SKIP

def example():
    """This example show how to create a marked Laurie state machine"""


    modelfiledir = '../../subjects/'

#    modelfile="ntscd_example.txt"
#    modelfile="sm3.txt"
#    modelfile="fairnessEG.txt"
#    modelfile="kellysample.txt"
#    modelfile="EFSM_ATM.txt"    
#    modelfile="EFSM_ATM_noexit.txt"
    modelfile="EFSM_Cashier.txt"
#    modelfile="EFSM_Cashier_noexit.txt"
#    modelfile="EFSM_CruiseControl-new.txt"
#    modelfile="EFSM_FuelPump.txt"
#    modelfile="EFSM_FuelPump_noexit.txt"
#    modelfile="EFSM_INRES.txt"
#    modelfile="EFSM_INRES_noexit.txt"
#    modelfile="EFSM_Lift.txt"
#    modelfile="EFSM_PrinTok.txt"
#    modelfile="EFSM_SimplifiedPhone.txt"
#    modelfile="EFSM_SimplifiedPhone_noexit.txt"
#    modelfile="EFSM_TCP.txt"
#    modelfile="EFSM_TCSbin.txt"
#    modelfile="EFSM_TCSbin_EXIT.txt"
#    modelfile="EFSM_VendingMachine.txt"
#    modelfile="EFSM_VendingMachine_noexit.txt"
##################################################
#initialize the model and dependence of SM
    inputfile = modelfiledir+modelfile
    SM=EFSM1.efsmFromFile(inputfile)
    print "%s has %s states and  %s transitions" %(SM.name, len(SM.stateList), len(SM.transitionList))
#    print '\transiton\n', SM.transitionList

##################################################
#view the model
#create Laurie SM, with marked transitions

    states=[]
    for s in SM.stateList:
       if s.name=='START':
            states.append(LSM.State(s.name, True))
       else:
            states.append(LSM.State(s.name))

    transitions=[]
    for tran in SM.transitionList:
       # tran.src=SM.state(tran.src)
       # tran.tgt=SM.state(tran.tgt)
        srcState=[state for state in states if state.name == tran.src.name].pop()
        tgtState=[state for state in states if state.name == tran.tgt.name].pop()
        transitions.append(LSM.Transition(tran.name, srcState, tgtState, True))

    EFSMGraph = LSM.State_Machine(states, transitions)
#   EFSMGraph.visualize()  #zhao temp delete

##################################################
    
    SM.allPathNum()
#    SM.duAnalysis()
    SM.testGen()
#    SM.execuTrans('T7')


if __name__ == '__main__':
    example()
#    convertfile()    
