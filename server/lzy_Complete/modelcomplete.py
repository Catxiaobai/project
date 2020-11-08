import re
import json
import os
def target_json():
    file_name = './file/result2.txt'
    lines = open(file_name, 'r', encoding='UTF-8').readlines()
    index_line = 0
    data_node = []
    data_edge = []
    while index_line < len(lines):
        if lines[index_line].strip() == "State:":
            index_line += 1
            node_num0 = lines[index_line].strip().split('=')[1]
            node_num = int(node_num0[1:])
            node_label = lines[index_line].strip().split('=')[1]
            index_line += 1
            node_name = lines[index_line].strip().split('=', 1)[1]
            # data.append({"data": {"id": node_name, "label": node_name, "category": node_category.get(node_name, 2)}})
            # data.append({"data": {"id": node_name, "label": node_label,"name":node_name}})
            data_node.append({"id": node_num, "label": node_label, 'name': node_name})
        if lines[index_line].strip() == "Transition:":
            index_line += 1
            name = lines[index_line].strip().split('=', 1)[1]
            name0 = int(name[1:])
            index_line += 1
            src0 = lines[index_line].strip().split('=', 1)[1]
            src = int(src0[1:])
            index_line += 1
            tgt0 = lines[index_line].strip().split('=', 1)[1]
            tgt = int(tgt0[1:])
            index_line += 1
            event = lines[index_line].strip().split('=', 1)
            event = event[1] if len(event) > 1 else ""
            index_line += 1
            cond = lines[index_line].strip().split('=', 1)
            cond = cond[1] if len(cond) > 1 else ""
            index_line += 1
            action = lines[index_line].strip().split('=', 1)
            action = action[1] if len(action) > 1 else ""
            edge = {"id": name0, "from": src, "to": tgt, "name": name, "event": event, "cond": cond,
                    "action": action, "color": 'black'}
            data_edge.append(edge)
        index_line += 1
    file_name = 'out.txt'
    lines = open(file_name, 'r', encoding='UTF-8').readlines()
    index_line = 0
    if os.path.getsize(file_name):
        while index_line < len(lines):
            edge_name = lines[index_line].strip().split(',')[0]
            edge_num = int(edge_name[1:])
            src = lines[index_line].strip().split(',')[1]
            src0 = int(src[2:])
            src = src.replace(' ', '')
            tgt = lines[index_line].strip().split(',')[2]
            tgt0 = int(tgt[2:])
            tgt = tgt.replace(' ', '')
            event = lines[index_line].strip().split(',')[3].split('=',1)[1]
            cond = lines[index_line].strip().split(',')[4].split('=',1)[1]
            action = lines[index_line].strip().split(',')[5].split('=',1)[1]
            t = 1 #判断增加节点是否需要新添
            for data_dict in data_node:
                if src0 == data_dict['id']:
                    t = 0
                    print()
            if t == 1:
                data_node.append({"id": src0, "label": src , 'name': ''})
            t = 1
            for data_dict in data_node:
                if tgt0 == data_dict['id']:
                    t = 0
            if t == 1:
                data_node.append({"id": tgt0, "label": tgt, 'name': ''})

            edge = {"id": edge_num, "from": src0, "to": tgt0, "name": edge_name, "event": event, "cond": cond,
                    "action": action}
            index_line +=1
            data_edge.append(edge)
        print(data_edge)
        print(data_node)
    else:
        return "complete"

if __name__ == '__main__':
    target_json()


