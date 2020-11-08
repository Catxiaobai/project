import random


def check():
    # FILENAME = './checking.txt'
    # lines = open(FILENAME, mode='r', encoding='UTF-8').readlines()
    a = random.randint(1, 3)
    if a == 1:
        check_flag = 'Yes'
    elif a == 2:
        check_flag = 'No'
    else:
        check_flag = 'at risk'

    return check_flag
