# encoding:utf-8

import EFSM
import obtain_efsm_info

filepath = r'E:/Code/project301/file/'

f = open(filepath+"targetInvalid.txt", 'r')
# f = open("F:/graphTraversal-submit2/efsmGA/model/target.txt", 'r')
targetList=[]
#targetList = f.readlines()
targetList = f.read().replace('\n','').replace('\r','')
f.close()
# s=[]

s = []
k=0
targetbranchlist=[]

# print 22222222222222222222222222222
# print targetList[0]
#for item in targetList:
    # print item
l1 = targetList[targetList.index("name")+5:targetList.index("src")]

l2 = targetList[targetList.index("event")+6:targetList.index("cond")]
l3 = targetList[targetList.index("cond")+5:targetList.index("action")]
l4 = targetList[targetList.index("action")+7: ]
if len(l2) == 0:
    l2 = l2 + " "
if len(l3) == 0:
    l3 = l3+" "
if len(l4) == 0:
    l4 = l4 + " "

#s.append(item.split(', '))
    #print s[0][0]+"   "+s[0][1]+"  "+s[0][2]

#targetbranchlist.append(EFSM.Transition(s[k][0], None, None, s[k][1], s[k][2], s[k][3]))
targetbranchlist.append((EFSM).Transition(l1,None,None,l2,l3,l4))
k+=1
    #print 111

# targetbranchlist = sorted(targetbranchlist,key=lambda x: len(obtain_efsm_info.getOppositeBranch(x)), reverse=True)


def targetBranch():

    print targetbranchlist[0].name

    return targetbranchlist[0]
    # targetList.pop(0)
def change():
    targetbranchlist.pop(0)

def sort():
    targetbranchlist.append(targetbranchlist[0])
    targetbranchlist.remove(targetbranchlist[0])

# s=targetList[0].split(', ')

# targetBranch = EFSM.Transition(targetList.pop(0))
# targetBranch = EFSM.Transition(s[0],None,None,s[1],s[2],s[3])


    # targetList.pop(0)
    # print targetList
'''
f = open("../model/target.txt", 'r')
targetList=[]
targetList = f.readlines()
f.close()
s=[]

while targetList:
    print targetList[0]
    s=targetList[0].split(', ')

# targetBranch = EFSM.Transition(targetList.pop(0))
    targetBranch = EFSM.Transition(s[0],None,None,s[1],s[2],s[3])
    del targetList[0]

'''