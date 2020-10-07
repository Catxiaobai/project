from judgeResult import judegeAdd

if __name__ == '__main__':
    t = str(judegeAdd())
    with open('judgeResult.txt', 'w', encoding='utf-8') as f:
        f.write(t)