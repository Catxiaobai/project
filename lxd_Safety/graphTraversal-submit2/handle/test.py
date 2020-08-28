# -*- coding: utf-8 -*-
import json
import xmltodict

import execjs
import domanaiyzer
from bs4 import BeautifulSoup
import io



statespath1 = '../efsmGA/states/T16.html'
htmlfile1 = io.open(statespath1, 'r', encoding='utf-8')
htmlhandle1 = htmlfile1.read()
soup1=BeautifulSoup(htmlhandle1, 'lxml')  # 选择lxml作为解析器



statespath2 = '../efsmGA/states/target1.html'
htmlfile2 = io.open(statespath2, 'r', encoding='utf-8')
htmlhandle2 = htmlfile2.read()
soup2=BeautifulSoup(htmlhandle2, 'lxml')  # 选择lxml作为解析器

s1=[]
s2=[]
for child in soup1.html.descendants:
    print(child.name)
    s1.append(child.name)
for child in soup2.html.descendants:
    print(child.name)
    s2.append(child.name)


if s1==s2:
    print 1
else:
    print 0


index=0

def diff(oldHtml,newHtml):
    walk(oldHtml,newHtml,index)

def walk(oldHtml,newHtml, index):
    patch=[]
    if newHtml is None:
        return 0
