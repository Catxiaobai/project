#import sys
#sys.path.append("D:/cxc/mymodules")
#sys.path.append("..")
#sys.path.append("../..")
#sys.path.append("../../subjects")
#sys.path.append("D:/cxc/subjects")
#import os

import EFSM
#import lusst
#import lusst.SM as LSM
#import lusst.Skip as SKIP

def example():
    """This example show how to create a marked Laurie state machine"""


    modelfiledir = '../subjects/'

#    modelfile="ntscd_example.txt"
#    modelfile="sm3.txt"
#    modelfile="fairnessEG.txt"
#    modelfile="kellysample.txt"
    modelfile="webchess.txt"
#    modelfile="EFSM_ATM_noexit.txt"
#    modelfile="EFSM_ATM_noexit_TEMP.txt"
#    modelfile = 'efsm_atm_not23.txt'
#    modelfile = 'efsm_cashier_noexit.txt'
#    modelfile = 'efsm_cashier_shortpin.txt'
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
#    for item in SM.transitionList:
#        print item.name
#        print SM.findPathforGivenTrans(item.name)
    
#    print '\transiton\n', SM.transitionList
    SM.allPathNum()
#    SM.alltransitions()
#    <**Path ['T1', 'T2', 'T4', 'T5', 'T8', 'T17', 'T21', 'T20', 'T22', 'T10', 'T7', 'T9', 'T23']**>
#    path='<**Path ['T1',\'T3\']**>'
#    print path
#    SM.pathInputVar(path)
#    for item in SM.transitionList:
#        print item.name
#        print SM.findPathforGivenTrans(item.name)
#    SM.duAnalysis()
    SM.testGen()
#    SM.execuTrans('T7')


if __name__ == '__main__':
    example()
#    convertfile()    
