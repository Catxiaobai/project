from judgeResult import judegeAdd,judegeDelete

if __name__ == '__main__':
    #print(judegeAdd())
    t = str(judegeDelete())
    with open('judgeResult.txt', 'w', encoding='utf-8') as f:
        f.write(t)