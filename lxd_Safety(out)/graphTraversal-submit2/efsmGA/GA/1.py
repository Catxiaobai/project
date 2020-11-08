import fileinput
for line in fileinput.input("../model/file.txt", inplace=1):
    if not fileinput.isfirstline():
        print(line.replace('\n',''))