# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import dash 
import dash_cytoscape as cyto   ## 需要安装 pip install dash-cytoscape==0.0.5
import dash_html_components as html
from dash.dependencies import Input, Output, State

filepath = r'E:/Code/project301/file/'
FILENAME = 'result.txt'

lines = open(filepath+FILENAME, 'r', encoding='utf-8').readlines()
index_line = 0

data = []
node_category = {"START": 0, "END": 1}

while index_line < len(lines):
    if lines[index_line].strip() == "State:":
        index_line += 1
        node_label = lines[index_line].strip().split('=')[1]
        data.append({"data": {"id": node_label, "label": node_label, "color": "gray"}})
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
        edge = {"id":src+tgt, "source": src, "target": tgt, "name": name, "event":event, "cond":cond, "action":action, "color":"black"}
        data.append({"data": edge})

    index_line += 1

app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-event-callbacks-2',
        style={'width': '100%', 'height': '800px'},
        elements=data,
        stylesheet= [
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'color': 'data(color)',
            'background-color': 'data(color)',
            }
        },
        {
            'selector': 'edge',
            'style': {
                'label': 'data(name)',
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'target-arrow-color': 'data(color)',
                'line-color': 'data(color)',
            }
        },
    ],
        layout={
        'name': 'breadthfirst',
        'roots': '[id = "START"]'
        }
    ),
    html.P(id='cytoscape-text3', children="S0是初始节点"),
    html.P(id='cytoscape-text1', children="最近点击的节点信息"),
    html.P(id='cytoscape-tapNodeData-output', style={'visibility': 'visible'}),
    html.P(id='cytoscape-text2', children="最近点击的边信息"),
    html.P(id='cytoscape-tapEdgeData-output', style={'visibility': 'visible'}),
])


@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
                  [Input('cytoscape-event-callbacks-2', 'tapNodeData')])
def displayTapNodeData(data):
    if data:
        data.pop('color')
        return str(data)


@app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
              [Input('cytoscape-event-callbacks-2', 'tapEdgeData')])
def displayTapEdgeData(data):
    if data:
        data.pop('color')
        return str(data)


if __name__ == '__main__':
    app.run_server(debug=True)
