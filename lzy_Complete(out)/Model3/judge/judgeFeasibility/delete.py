import json
from judgeResult import judegeAdd,judegeDelete

# with open("1.json") as f:
#     two_str_json = f.read()
#
# two_str_list = two_str_json.split('][')
#
# two_str_list[0] = two_str_list[0] + ']'
# two_str_list[1] = '[' + two_str_list[1]
# two_json_list = []
# two_json_list.append(json.loads(two_str_list[0]))
# print(two_json_list)
def json_to_txt(node_json, edge_json, result_file):
    with open(node_json) as f:
        data_list = json.load(f)

    result = ''
    for data_dict in data_list:
        if 'text' in data_dict.keys():
            if data_dict['text'] == "start":
                data_dict['text'] = "START"
            result = result + 'State:' + '\n' + '\t'+'name=' + data_dict[
                'text'] + '\n'

    with open(edge_json) as f:
        data_list = json.load(f)

    for data_dict in data_list:
        if str(data_dict['from']) == '0':
            data_dict['from'] = 'TART'
        elif str(data_dict['to']) == '0':
            data_dict['to'] = 'TART'
        result = result + 'Transition:' + '\n' \
                 + '\t' + 'name=' + str(data_dict['text']) + '\n' \
                 + '\t' + 'src=' + 'S' + str(data_dict['from']) + '\n' \
                 + '\t' + 'tgt=' + 'S' + str(data_dict['to']) + '\n' \
                 + '\t' + 'event=' + str(data_dict['event']) + '\n' \
                 + '\t' + 'condition=' + str(data_dict['cond']) + '\n' \
                 + '\t' + 'action=' + str(data_dict['action']) + '\n'
        #print(result)
    with open(result_file, 'wt+', encoding='utf-8') as f:
        f.write(result)

        
def test():
    t = str(judegeDelete())
    print(t)
    with open(filepath+'judgeResult.txt', 'w', encoding='utf-8') as f:
        f.write(t)

#要删除或添加的迁移
def json_to_target(edge_json, result_file):
    with open(edge_json) as f:
        data_list = json.load(f)
    result = ''
    for data_dict in data_list:
        if str(data_dict['from']) == '0':
            data_dict['from'] = 'TART'
        elif str(data_dict['to']) == '0':
            data_dict['to'] = 'TART'
        result = result\
                 + str(data_dict['text']) +','\
                 + 'S'+str(data_dict['from']) + ', ' \
                 + 'S'+str(data_dict['to']) + ', ' \
                 + str(data_dict['event'])+ ', ' \
                 + str(data_dict['cond'])+ ', ' \
                 + str(data_dict['action'])+','
        #print(result)
    with open(result_file, 'wt+', encoding='utf-8') as f:
        f.write(result)


if __name__ == '__main__':
    filepath = 'E:/Code/project301/file/'
    # json_to_txt(filepath+'node.json', filepath+'edge.json',filepath+'resultModel.txt')
    test()
    # json_to_target('3.json','failureTran/target3.txt')
    # t = str(judegeDelete())
    # print(t)
    # with open(filepath+'judgeResult.txt', 'w', encoding='utf-8') as f:
    #     f.write(t)
