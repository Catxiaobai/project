#encoding:utf-8
import sys

import EFSM

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../model")
sys.path.append("../spath")

loopLimit = 5  # 纠正次数上限
numOfPSG = 1    # 序列生成的生成条数
sort = 1  # 排序开关 1是全排序(连接迁移排序按引入变量多少)； 0是DFS（除了候选对立分支）； 2是相关迁移排序； 3是连接迁移排序
# 数据相关迁移的排序
yrzswgbl = 1  # 引入最少无关变量
achcdpx = 1  # 按重合程度排序
mbfzpax = 1 # 目标分支排序
achxhpx = 0  # 按重合先后排序(控制距离)
hhpx = 1  # 混合排序
#新迁移优先
newtransort = 1
# 权重
defPercent = [10, 1]  # 权重：event action
usePercent = [10, 1]  # 权重：cond action
# 回溯
back = 1  # 1是单步回溯，0是回溯至上一数据相关迁移(全排序和仅连接迁移随机时可用)





# 两个映射函数（混合排序：根据映射函数的不同可以退化成按数量排序或是按先后顺序排序）
def distMap(dist):
        return 1 / dist

def numMap(num):
        return num

# 获取用于序列生成的目标分支
def getTargetBranch(targetBranch):
    '''
    targetBranch = EFSM.Transition('target', None, None,
                                   "Receipt()",
                                   "l=='s'",
                                   'Print("Balanza=",cb); write("Ahorros/Corriente")')
    #T23
    targetBranch = EFSM.Transition('target', None, None,
                                   "input(username,password,password2,x_type);xpath=(//input[@  value='Add User'])[2];click",
                                   "password == password2 && password != ''",
                                   'documentaddusersubmit()')
    #T59
    targetBranch = EFSM.Transition('target', None, None,
                                   "input(username,password,password2,x_type);xpath=(//input[@  value='Edit user'])[2];click",
                                   "!((!(password == '' && password2 == ''))&&(password == password2))",
                                   'documentaddusersubmit()')
    # T165
    targetBranch = EFSM.Transition('target', None, None,
                                   ";xpath=(//input[@ value='Edit'])[2];click",
                                   "!(documentstudentsselectstudentvalue == 1)",
                                   'documentstudentssubmit()')
    # T249
    targetBranch = EFSM.Transition('target', None, None,
                                   "input(documentregistrationelementschecked);xpath=(//input[@ value='$reg[0]'])[2];click",
                                   "documentregistrationelementschecked == 1",
                                   'documentregistrationselectregvalue = documentregistrationselectregvalue + 1')
    # T189
    targetBranch = EFSM.Transition('target', None, None,
                                   "input(documentteacherselementschecked);xpath=(//input[@ value='$teacher[0]'])[2]);click",
                                   "documentteacherselementschecked == 1",
                                   "documentteachersselectteachervalue = documentteachersselectteachervalue + 1")
    # T5
    targetBranch = EFSM.Transition('target', None, None,
                                   ";xpath=(//input[@ value='Cancel'])[2];click",
                                   "!(b==1)",
                                   "submit()")
    # T33
    targetBranch = EFSM.Transition('target', None, None,
                                   "input(f);link=Attendance;click",
                                   "!(f==1)",
                                   "documentadminpage2value=30;documentadminsubmit()")
    # T137
    targetBranch = EFSM.Transition('target', None, None,
                                   "input(documentparentselementschecked);xpath=(//input[@ value='$parent[0]'])[2];click",
                                   "!(documentparentselementschecked == 1)",
                                   "documentparentsselectparentvalue = documentparentsselectparentvalue - 1")
    # T221
    targetBranch = EFSM.Transition('target', None, None,
                                   "input(documentuserselementschecked);xpath=(//input[@ value='$user[0]'])[2]);click",
                                   "!(documentuserselementschecked == 1)",
                                   "documentusersselectuservalue = documentusersselectuservalue + 1")
    # T131
    targetBranch = EFSM.Transition('target', None, None,
                                   "input(g);xpath=(//input[@ value='Add'])[2];click",
                                   "!(g==0)",
                                   "submit()")



    # T22
    targetBranch = EFSM.Transition('target1', None, None,
                                   "input(txtFirstName,txtLastName,pwdOldPassword,pwdPassword,pwdPassword2);xpath=/html/body/div[2]/div[2]/div[1]/div/div/div[1]/form/div/input[1];click",
                                   "!(pwdPassword == pwdPassword2)",
                                   "")
    '''


    return targetBranch


# 获取用于序列生成的模型
def getGenerateModule():
    modelfiledir = 'E:/Code/project301/file/'
    # modelfile = "EFSM_ATM.txt"
    # modelfile = "schoolmate_ADMIN_new1.txt"
    modelfile = "webchess.txt"
    # modelfile = "addressbookv3.txt"
    # modelfile = "FAQfoege.txt"
    # modelfile = "phpCSSv3.txt"
    # modelfile = "motivation.txt"
    # modelfile="EFSM_Cashier.txt"
    # modelfile="EFSM_CruiseControl-old.txt"
    # modelfile="EFSM_PrinTok.txt"
    # modelfile="EFSM_SimplifiedPhone.txt"
    # modelfile="EFSM_FuelPump.txt"
    inputfile = modelfiledir + modelfile
    return inputfile


# 下面是模拟执行及以后的部分
# 获取生成数据所需要的模组
def getExecuteModule():
    modelfiledir = '../module/'
    # modelfile = "schoolmate_Vtest9_addnavigation.txt" #跑测试用例，增加模块间的导航
    # modelfile = "schoolmate_Vtest8_sample.txt"    # 跑测试用例，去除了关于删除的迁移
    # modelfile = "schoolmate_Vtest7.txt"     #跑测试用例生成的
    # modelfile = "FAQfoege.txt"  # 跑测试用例生成的,聚类用的
    # modelfile = "schoolmate_ADMIN_new1.txt"
    modelfile = "webchess.txt"
    # modelfile = "motivation.txt"
    # modelfile = "teacher_v3.txt"
    # modelfile = "addressbookv3.txt"
    # modelfile ="phpCSSv3.txt"
    inputfile = modelfiledir + modelfile
    return inputfile


# 获取模拟执行所需要的网址
def getUrl():
    # url = "http://localhost/schoolmate/"  # schoolmate
    # url = "http://localhost/2faqforge_new/"  # faqforge
    url = "http://localhost/4webchess/"  #webchess
    # url ="http://localhost/1addressbook/"  # addressbook
    # url="http://localhost/phpaaCMS/admin/login.php" #phpCSS
    return url


# 下面的都是没用到的
def getInstrumentFile():
    # 插桩获得的信息文件路径要与插桩路径一致
    # schoolmate
    # file = "E:\\Wamp\\wamp\\www\\schoolmate2\\b.txt"
    # file2 = "E:\\Wamp\\wamp\\www\\schoolmate2\\bbb.txt"
    # faqforg
    # file = "E:\\Wamp\\wamp\\www\\2faqforge_new\\b.txt"
    # file2 = "E:\\Wamp\\wamp\\www\\2faqforge_new\\bbb.txt"
    # webchess
    # file = "E:\\Wamp\\wamp\\www\\4webchess\\b.txt"
    # file2 = "E:\\Wamp\\wamp\\www\\4webchess\\bbb.txt"

    file = "E:\\Wamp\\wamp\\www\\1addressbook\\b.txt"
    file2 = "E:\\Wamp\\wamp\\www\\1addressbook\\bbb.txt"

    # file = "E:\\Wamp\\wamp\\www\\phpaaCMS_0.5\\admin\\b.txt"
    # file2 = "E:\\Wamp\\wamp\\www\\phpaaCMS_0.5\\admin\\bbb.txt"
    return file, file2

def getRecordFundFile():
    filepath = "../dataset/"  # schoolmate的
    return filepath


def getSpathFile():
    modelfiledir = '../spath/'
    # modelfile = "spath_flag_schoolmate_admin.txt"  #schoolmate
    # modelfile = "spath_flag_schoolmate_teacher.txt"
    # modelfile = "spath_flag_faqforg.txt"  # faqfore
    # modelfile = "spath_flag_webchess.txt"
    modelfile = "spath_flag_addressbook.txt"
    # modelfile = "spath_flag_phpcss.txt"
    inputfile = modelfiledir + modelfile
    return inputfile

def getPopParameter():
    # popsize不能为奇数
    # popsize = 22 #schoolmate_teacher  sensitive path has 19
    # popsize = 28 # schoolmate_admin   sensitive path has 24
    # popsize = 18 #webchess   sensitive path has 12
    # popsize = 6  #faqforge   sensitive path has 3
    popsize = 10 # addressbook sensitive path has 5
    # popsize = 26  # phpcss sensitive path has 18
    pc = 0.8
    pm = 0.9
    Max = 2000
    return popsize,pc,pm,Max



if __name__ == '__main__':
    getExecuteModule()