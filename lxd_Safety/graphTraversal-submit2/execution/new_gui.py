# -*- coding: UTF-8 -*-
from graphviz import Digraph
from PIL import Image,ImageTk,ImageDraw,ImageFont

dot = Digraph(comment='这是一个有向图')
dot.node('A', '作者')
dot.node('B', '医生')
dot.node('C', '律师')

dot.edges(['AB', 'AC'])
dot.edge('B', 'C')

dot.format = 'png'
dot.render('output-graph.gv', view=True)
Image(dot.render('output-graph.gv'))