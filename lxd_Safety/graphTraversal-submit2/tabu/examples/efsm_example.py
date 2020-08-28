import sys
sys.path.append("D:\\cxc\\mymodules")
#sys.path.append("..")
#sys.path.append("../..")
sys.path.append("D:/cxc/subjects")
import os
import sys

import EFSM
#import lusst
#import lusst.SM as LSM
#import lusst.Skip as SKIP

def example():
    """This example show how to create a marked Laurie state machine"""


    modelfiledir = 'D:/cxc/subjects/'

#    modelfile="ntscd_example.txt"
#    modelfile="sm3.txt"
#    modelfile="fairnessEG.txt"
#    modelfile="kellysample.txt"
    modelfile="efsm_atm.txt"    
#    modelfile="EFSM_ATM_noexit.txt"
#    modelfile="EFSM_ATM_noexit_TEMP.txt"
#    modelfile="EFSM_ATM_noexit_new.txt"
#    modelfile="EFSM_Cashier.txt"
#   modelfile="EFSM_Cashier_shortPin.txt"
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
    SM=EFSM.efsmFromFile(inputfile)
    print "%s has %s states and  %s transitions" %(SM.name, len(SM.stateList), len(SM.transitionList))
#    print '\transiton\n', SM.transitionList
    SM.allPathNum()
    SM.duAnalysis()
#    SM.testGen()
#    SM.execuTrans('T7')


if __name__ == '__main__':
    example()
#    convertfile()    
