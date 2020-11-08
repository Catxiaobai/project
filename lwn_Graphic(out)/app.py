# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import dash
import dash_core_components as dcc
import dash_cytoscape as cyto  ## 需要安装 pip install dash-cytoscape==0.0.5
import dash_html_components as html
from dash.dependencies import Input, Output, State
from checking import check
import copy


filepath = r'E:/Code/project301/file/'
FILENAME = 'result.txt'
node_category = {"START": 0, "END": 1}

first_time = True


def read_txt(file_name):
    lines = open(file_name, 'r', encoding='UTF-8').readlines()
    index_line = 0
    read_data = []
    while index_line < len(lines):
        if lines[index_line].strip() == "State:":
            index_line += 1
            node_label = lines[index_line].strip().split('=')[1]
            index_line += 1
            node_name = lines[index_line].strip().split('=', 1)[1]
            # data.append({"data": {"id": node_name, "label": node_name, "category": node_category.get(node_name, 2)}})
            # data.append({"data": {"id": node_name, "label": node_label,"name":node_name}})
            read_data.append({"data": {"id": node_label, "label": node_label, 'name': node_name, "color": "gray"}})
        if lines[index_line].strip() == "Transition:":
            index_line += 1
            name = lines[index_line].strip().split('=', 1)[1]
            index_line += 1
            src = lines[index_line].strip().split('=', 1)[1]
            index_line += 1
            tgt = lines[index_line].strip().split('=', 1)[1]
            index_line += 1
            event = lines[index_line].strip().split('=', 1)
            event = event[1] if len(event) > 1 else ""
            index_line += 1
            cond = lines[index_line].strip().split('=', 1)
            cond = cond[1] if len(cond) > 1 else ""
            index_line += 1
            action = lines[index_line].strip().split('=', 1)
            action = action[1] if len(action) > 1 else ""
            edge = {"id": src + tgt, "source": src, "target": tgt, "name": name, "event": event, "cond": cond,
                    "action": action, "color": "black"}
            read_data.append({"data": edge})

        index_line += 1
    return read_data


data = read_txt(filepath+FILENAME)
'''NEW_DATA = 'newdata.txt'
lines = open(NEW_DATA, 'r').readlines()
index_line = 0
while index_line < len(lines):
    if lines[index_line].strip() == "State:":
        index_line += 1
        node_label = lines[index_line].strip().split('=')[1]
        if all([node_label != node["data"]["id"] for node in data]):
            data.append({"data": {"id": node_label, "label": node_label, "color": "green"}}) # here modify your node color
    if lines[index_line].strip() == "Transition:":
        index_line += 1
        name = lines[index_line].strip().split('=', 1)[1]
        index_line += 1
        src = lines[index_line].strip().split('=', 1)[1]
        index_line += 1
        tgt = lines[index_line].strip().split('=', 1)[1]
        index_line += 1
        event = lines[index_line].strip().split('=', 1)
        event = event[1] if len(event) > 1 else ""
        index_line += 1
        cond = lines[index_line].strip().split('=', 1)
        cond = cond[1] if len(cond) > 1 else ""
        index_line += 1
        action = lines[index_line].strip().split('=', 1)
        action = action[1] if len(action) > 1 else ""
        # assume all edge are new in new data!
        edge = {"id":src+tgt, "source": src, "target": tgt, "name": name, "event":event, "cond":cond, "action":action, "color": "blue"} # here modify your new edge color
        data.append({"data": edge})

    index_line += 1'''

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'label:  ',
        dcc.Input(id='label-state', type='text', ),
    ]),
    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'name:',
        dcc.Input(id='name-state', type='text', ),
    ]),
    html.Button(id='submit-button-state', n_clicks=0, children='add node'),
    html.P(),
    html.Div(id='output-state'),

    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'name:',
        dcc.Input(id='name-1-state', type='text', ),
    ]),
    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'src:',
        dcc.Input(id='src-state', type='text', ),
    ]),
    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'tgt:',
        dcc.Input(id='tgt-state', type='text', ),
    ]),
    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'event:',
        dcc.Input(id='event-state', type='text', ),
    ]),
    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'condition:',
        dcc.Input(id='condition-state', type='text', ),
    ]),
    html.Div(style={'width': '50%', 'display': 'inline', 'visibility': "visible"}, children=[
        'action:',
        dcc.Input(id='action-state', type='text', ),
    ]),
    html.Button(id='edge-button-state', n_clicks=0, children='add edge'),
    html.P(),
    html.Div(id='message', style={'width': '50%', 'display': 'block', 'visibility': "visible"}, children=[
        html.P(children='', style={'color': 'green'}),
        html.Button(id='confirm', n_clicks=0, children='确认', style={'color': 'blue'}),
        html.Button(id='cancel', n_clicks=0, children='取消', style={'color': 'blue', 'margin-left': '20px'}),
    ]),
    cyto.Cytoscape(
        id='cytoscape-event-callbacks-2',
        style={'width': '100%', 'height': '550px'},
        elements=data,
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'content': 'data(event)',
                    'label': 'data(name)',
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'triangle',

                }
            },
        ],
        layout={
            'name': 'breadthfirst',
            'roots': '[id = "S0"]'
        }
    ),
    html.P(id='cytoscape-text3', children="S0是初始节点"),
    html.P(id='cytoscape-text1', children="最近节点信息"),
    html.P(id='cytoscape-tapNodeData-output', style={'visibility': 'visible'}),
    html.P(id='cytoscape-text2', children="最近边信息"),
    html.P(id='cytoscape-tapEdgeData-output', style={'visibility': 'visible'}),
])


@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              [Input('cytoscape-event-callbacks-2', 'mouseoverNodeData')])
def displayTapNodeData(data):
    if data:
        data.pop('color')
        return str(data)


@app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
              [Input('cytoscape-event-callbacks-2', 'mouseoverEdgeData'),
               ])
def displayTapEdgeData(data):
    if data:
        data.pop('color')
        return str(data)


@app.callback([Output('cytoscape-event-callbacks-2', 'elements')],
              [Output('message', 'children')],
              [Input('submit-button-state', 'n_clicks')],
              [Input('edge-button-state', 'n_clicks')],
              [Input('confirm', 'n_clicks')],
              [Input('cancel', 'n_clicks')],
              [Input('cytoscape-event-callbacks-2', 'tapNodeData')],
              [Input('cytoscape-event-callbacks-2', 'tapEdgeData')],
              [State('name-1-state', 'value'),
               State('src-state', 'value'),
               State('tgt-state', 'value'),
               State('event-state', 'value'),
               State('condition-state', 'value'),
               State('action-state', 'value'),
               State('label-state', 'value'),
               State('name-state', 'value'),
               ],
              )
def update_charts(btn_node, btn_edge, btn_confirm, btn_cancel, node_data, edge_data, e_name, e_src, e_tgt, e_event,
                  e_condition, e_action,
                  n_label, n_name):
    global first_time
    if first_time:
        data = read_txt("./2020-result.txt")
    else:
        data = read_txt('./result.txt')
    if int(btn_confirm) > int(btn_cancel):
        div_children = [
            html.P(children='执行成功', style={'color': 'green'}),
            html.Button(id='confirm', n_clicks=0, children='确认', style={'color': 'blue', 'visibility': "hidden"}),
            html.Button(id='cancel', n_clicks=0, children='取消', style={'color': 'blue', 'visibility': "hidden"}),
        ]
        new_data = read_txt("./check.txt")
        create_txt(new_data, checking=False)
        first_time = False
        return new_data, div_children
    elif int(btn_cancel) > int(btn_confirm):
        div_children = [
            html.P(children='已取消执行', style={'color': 'green'}),
            html.Button(id='confirm', n_clicks=0, children='确认', style={'color': 'blue', 'visibility': "hidden"}),
            html.Button(id='cancel', n_clicks=0, children='取消', style={'color': 'blue', 'visibility': "hidden"}),
        ]
        return data, div_children
    else:
        new_data = copy.deepcopy(data)
        if int(btn_edge) > int(btn_node) and e_name and e_src and e_tgt and e_event and e_condition and e_action:
            e_edge = {"id": e_src + e_tgt, "source": e_src, "target": e_tgt, "name": e_name, "event": e_event,
                      "cond": e_condition,
                      "action": e_action, "color": "black"}
            new_data.append({"data": e_edge})
        elif int(btn_node) > int(btn_edge) and n_label and n_name:
            new_data.append({"data": {"id": n_label, "label": n_label, 'name': n_name, "color": "gray"}})
        elif node_data:
            dict_node_data = {"data": node_data}
            new_data.remove(dict_node_data)
        elif edge_data:
            edge_node_data = {"data": edge_data}
            new_data.remove(edge_node_data)

        create_txt(new_data, checking=True)  # 创建check文件
        check_success = check()  # 检查是否可以执行

        if check_success == 'Yes':
            div_children = [
                html.P(children='执行成功', style={'color': 'green'}),
                html.Button(id='confirm', n_clicks=0, children='确认', style={'color': 'blue', 'visibility': "hidden"}),
                html.Button(id='cancel', n_clicks=0, children='取消', style={'color': 'blue', 'visibility': "hidden"}),
            ]
            create_txt(new_data, checking=False)
            first_time = False
            return new_data, div_children
        elif check_success == 'No':
            div_children = [
                html.P(children='执行失败', style={'color': 'red'}),
                html.Button(id='confirm', n_clicks=0, children='确认', style={'color': 'blue', 'visibility': "hidden"}),
                html.Button(id='cancel', n_clicks=0, children='取消', style={'color': 'blue', 'visibility': "hidden"}),
            ]
            return data, div_children
        else:
            div_children = [
                html.P(children='存在风险,确认执行吗？', style={'color': 'red'}),
                html.Button(id='confirm', n_clicks=0, children='确认', style={'color': 'blue', 'visibility': "visible"}),
                html.Button(id='cancel', n_clicks=0, children='取消', style={'color': 'blue', 'visibility': "visible"}),
            ]
            return data, div_children


def create_txt(result_data, checking):
    result = ''
    for va in result_data:
        data_dict = va['data']
        if 'label' in data_dict.keys():
            result = result + 'State:' + '\n' + '    label=' + data_dict['label'] + '\n' + '    name=' + data_dict[
                'name'] + '\n'
    for va in result_data:
        data_dict = va['data']
        if 'target' in data_dict.keys():
            result = result + 'Transition:' + '\n' \
                     + '        name=' + data_dict['name'] + '\n' \
                     + '        src=' + data_dict['source'] + '\n' \
                     + '        tgt=' + data_dict['target'] + '\n' \
                     + '        event=' + data_dict['event'] + '\n' \
                     + '        condition=' + data_dict['cond'] + '\n' \
                     + '        action=' + data_dict['action'] + '\n'
    if checking:
        with open('check.txt', 'wt+', encoding='utf-8') as f:
            f.write(result)
            print("成功生成文件！")
    else:
        with open('result.txt', 'wt+', encoding='utf-8') as f:
            f.write(result)
            print("成功生成文件！")


if __name__ == '__main__':
    app.run_server(debug=True)
