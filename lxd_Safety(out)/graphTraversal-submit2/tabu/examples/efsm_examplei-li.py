import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../subjects")
import os

import EFSM
import lusst
import lusst.SM as LSM
import lusst.Skip as SKIP

#sys.setrecursionlimit(5000)


def example():
    """This example show how to create a marked Laurie state machine"""
##################################################
#select a example here
#     currentdir = os.curdir
#     imagedir = os.path.join(currentdir, "..\..\subjects")
#     imagefile = os.path.join(imagedir, "test.txt")
#     print imagefile

    modelfiledir = '../../subjects/'
#    currentdir = os.path.dirname(__file__)


#imagedir = os.path.join(currentdir, "images")
#    modelfile="test.txt"

#    modelfile="ntscd_example.txt"
#    modelfile="sm3.txt"
#    modelfile="fairnessEG.txt"
#    modelfile="kellysample.txt"
    modelfile="EFSM_ATM.txt"    #by zhao
#    modelfile="EFSM_ATM_noexit.txt"
#    modelfile="EFSM_Cashier.txt"
#    modelfile="EFSM_Cashier_noexit.txt"
#    modelfile="EFSM_CruiseControl.txt"
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
#    print "%s has %s states and  %s transitions" %(SM.name, len(SM.stateList), len(SM.transitionList))
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
        srcState=[state for state in states if state.name == tran.src.name].pop()
        tgtState=[state for state in states if state.name == tran.tgt.name].pop()
        transitions.append(LSM.Transition(tran.name, srcState, tgtState, True))

    EFSMGraph = LSM.State_Machine(states, transitions)
    EFSMGraph.visualize()
##################################################
#initialize the dependence of model
    EFSM.initEFSM(SM)

##################################################
#TEST
#    print SM.stateTransitiveSuccessor(SM.state('START'))
#    print SM.ntscdSuccessor(SM.transition('TS12'))
#    print SM.maxPathDict[SM.transition('TS11').name]
#   print SM.findSuccSinkPath(SM.transition('TS2'))
#     for transition in SM.transitionList:
#         print transition, ":\n"
# #        print SM.findMaxPath(transition)
#         print SM.maxPathDict[transition.name]
#         print "\n"
    # print SM.findSuccMaxPath(SM.transition('T3'))
    # print SM.maxPathDict[SM.transition('T2').name]

##################################################
# #output variables for each transition
#     ofile=open(SM.name+"_variables_list.txt", "w") 
#     vSet=set()
#     for tran in SM.transitionList:
# #       {eventVdef:vlist, condVuse:vlist, actionVdef:vlist, actionVuse,vlist}
#         for x in ["eventVdef", "condVuse", "actionVdef", "actionVuse"]:
#             ofile.write(tran.name+'\t'+x+':\t')
#             for y in SM.tranVarDict[tran.name][x]:
#                 ofile.write(y+'\t')
#                 vSet.add(y)
#             ofile.write('\n')

#     ofile.write("\ntotal variables: "+str(len(vSet))+'\n')
#     for v in vSet:
#         ofile.write(v+', ')
#     ofile.close()

##################################################
#generate dependence graph
#    print 'generate the dependence graph...'

#    SMDG=SM.makeDependenceGraph('DATA', 'NTSCD')
#    SMDG=SM.makeDependenceGraph('DATA', 'NTICD')
#    SMDG=SM.makeDependenceGraph('DATA', 'UNTICD')
#    SMDG.view()    # view the dependence graph

    for cd in ['NTICD', 'NTSCD', 'UNTICD']:
        SMDG=SM.makeDependenceGraph('DATA', cd)
        SMDG.view()    # view the dependence graph
    

# ##################################################
# #define a slicing criterion here
    criterion=SM.transition('T7')


# ##################################################
#generate the dependence graph wrt the criterion
    subDG=SMDG.subBWGraphwrtNode(criterion)
    subDG.view(criterion) # view the subdependence graph

#create Laurie SM, with marked transitions
    states=[]
    for s in SM.stateList:
        if s.name=='START':
            states.append(LSM.State(s.name, True))
        else:
            states.append(LSM.State(s.name))

    transitions=[]
    for tran in SM.transitionList:
        srcState=[state for state in states if state.name == tran.src.name].pop()
        tgtState=[state for state in states if state.name == tran.tgt.name].pop()
        if tran in subDG.nodeList:
            transitions.append(LSM.Transition(tran.name, \
                                                 srcState, tgtState, True))
        else:
            transitions.append(LSM.Transition(tran.name, \
                                                 srcState, tgtState, False))

    SMGraph=LSM.State_Machine(states,transitions)   # added by zhao on 21.04.2009
    SMGraph.visualize()     # added by zhao on 21.04.2009
# ####################################

#     LaurieSM = LSM.State_Machine(states, transitions)    

#     print "  Before (%d states, %d transitions)" % (len(LaurieSM.states), len(LaurieSM.transitions))
#     print " ", LaurieSM.states
#     print " ", LaurieSM.transitions  

#     LaurieSM.visualize(criterion)

#     LaurieSM.slice()
#     LaurieSM.visualize()

#     print "  After (%d states, %d transitions)" % (len(LaurieSM.states), len(LaurieSM.transitions))
#     print " ", LaurieSM.states
#     print " ", LaurieSM.transitions  

####################################
# using skip algorithm

#     SkipSM = SKIP.State_Machine(states, transitions) 

#     print "  Before (%d states, %d transitions)" % (len(SkipSM.states), len(SkipSM.transitions))
#     print " ", SkipSM.states
#     print " ", SkipSM.transitions  

# #     SkipSM.visualize()
#     SkipSM.slice()
#     SkipSM.visualize()

#     print "  After (%d states, %d transitions)" % (len(SkipSM.states), len(SkipSM.transitions))
#     print " ", SkipSM.states
#     print " ", SkipSM.transitions 


# ####################################
# def convertfile():
# #    inputfile="EFSM_ATM.txt"
# #    inputfile="EFSM_Cashier.txt"
# #    inputfile="EFSM_CruiseControl.txt"
# #    inputfile="EFSM_FuelPump.txt"
# #    inputfile="EFSM_Lift.txt"
# #    inputfile="EFSM_PrinTok.txt"
# #    inputfile="EFSM_SimplifiedPhone.txt"
#     inputfile="EFSM_VendingMachine.txt"

#     from kvparser import Parser, ListParser
#     f=open(inputfile)
#     ofile=open(inputfile.split('.')[0]+"_new.txt", "w")
#     s=f.read()
#     SMBlockList = ListParser().parse(s)
#     label={}
#     for block in SMBlockList:
#         if block[0] == 'State':
#             (value)= [item[1] for item in block[1]]
#             ofile.write("State:\n\tname=" + value[0] +"\n")
#         elif block[0] == 'Label':
# #            print 'label block = ',  block[0]
#             (name, event, cond, action) = [item[1] for item in block[1]]
#             label[name]=(event, cond, action)
#         elif block[0] == 'Transition':
#             (name, srcName, tgtName, labelname) = [item[1] for item in block[1]]
#             ofile.write("Transition:\n\tname="+labelname+"\n")
#             ofile.write("\tsrc="+srcName+"\n")
#             ofile.write("\ttgt="+tgtName+"\n")
#             ofile.write("\tevent="+label[labelname][0]+"\n")
#             ofile.write("\tcond="+label[labelname][1]+"\n")
#             ofile.write("\taction="+label[labelname][2]+"\n")
#         else:
#             pass
#     f.close()
#     ofile.close()



if __name__ == '__main__':
    example()
#    convertfile()    
