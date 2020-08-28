
filepath = r'E:/Code/project301/file/'


def formatfile():
    f1 = open(filepath+"result.txt","r")
    f2 = open(filepath+"webchess.txt","w")

    l1=[]
    l1=f1.readlines()
    l2 = []
    l3 = []
    str1 = "S0"
    str2 = "START"
    str3 = "condition"
    str4 = "cond"
    str5 = "null"
    str6 = ""
    exit = ""
    for line in l1:
        l2.append(line.strip())

    for i in range(0,len(l2)):
        if(l2[i] == "Transition:"):
            exit = l2[i-2].split("=")[1]
            break
    # def alter(old_str,new_str):
    #     file_data = ""
    #     with open("D:/result.txt","r")as f:
    #         for line in f:
    #             if old_str in line:
    #                 line = line.replace(old_str,new_str)
    #             file_data += line
    #     with open("D:/result.txt","w") as f:
    #         f.write(file_data)
    def alter(old_list,old_str,new_str):
        for i in range(0,len(old_list)):
            if(old_str in old_list[i]):
                old_list[i] = old_list[i].replace(old_str,new_str)
        return old_list
    l2 = alter(l2,str1,str2)
    l2 = alter(l2,str3,str4)
    l2 = alter(l2,str5,str6)
    l2 = alter(l2,exit,"Exit")
    for lent in range(0,len(l2)):

        if "State" in l2[lent] :
            f2.writelines("State:"+"\n")

            f2.writelines("\t"+"name="+l2[lent+1].split("=")[1]+"\n")

        if "Transition" in l2[lent]:
            f2.writelines("Transition:"+"\n")
            f2.writelines("\t" + l2[lent + 1] + "\n")
            f2.writelines("\t" + l2[lent + 2] + "\n")
            f2.writelines("\t" + l2[lent + 3] + "\n")
            f2.writelines("\t" + l2[lent + 4] + "\n")
            f2.writelines("\t" + l2[lent + 5] + "\n")
            f2.writelines("\t" + l2[lent + 6] + "\n")
    f2.close()
