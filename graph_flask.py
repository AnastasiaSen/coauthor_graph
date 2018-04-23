# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 17:00:30 2018

@author: Ася
"""
from igraph import *
from plotly.graph_objs import *
import pandas as pd
import csv
import numpy as np
import plotly
plotly.offline.init_notebook_mode(connected=True)


def plot_graph(param):
    df_nodes = pd.read_csv('node.csv', encoding='mac_roman', delimiter =';') # чтание из файла с вершинами
    reader = csv.DictReader(open("edges.csv"), dialect="excel", delimiter=';') # чтение из файла со связями
    graph = Graph.DictList(vertices=None, edge_foreign_keys=('Author, company', 'Co-author, company'), edges=reader) # составление графа
    nodes=list(graph.vs['name']) # вершины
    edges = [e.tuple for e in graph.es] # ребра
    layt=graph.layout('kk') # задание координат вершин в зависимости от из связности по алгоритму Kamada–Kawai
    N=len(nodes) # число вершин
    Xn=[layt[k][0] for k in range(N)] # задание координат для вершин по оси х
    Yn=[layt[k][1] for k in range(N)] # задание координат вершин по оси у
    Xe=[] # вектор-переменная для записи у-координат отрезков-связей
    Ye=[] # вектор-переменная для записи х-координат отрезков-связей
    for e in edges:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]
        Ye+=[layt[e[0]][1],layt[e[1]][1], None] 
    
    # создание списка для связей (рёбер)
    edge_trace=Scatter(x=Xe,
               y=Ye,
               mode='lines',
               line=Line(color='rgb(210,210,210)', width=1),
               hoverinfo='none'
               )
    # создание списка для вершин
    
    node_trace = Scatter(
                    x=[],
                    y=[],
                    text=[],
                    name = [], 
                    mode='markers',
                    hoverinfo='text',
                    marker=Marker(
                        color=[],
                        size= [],
                        line=dict(width=2)))
    # заполнение списка для вершин
    # для каждой вершины из файла
    for i in range(len(df_nodes)):
        i_node = nodes.index(df_nodes['Author'][i]+','+df_nodes['Company'][i]) # определение индекса вершины в списке node из графа graph
        x, y = Xn[i_node], Yn[i_node] # определение по индексу соответствующих оординат
        node_trace['x'].append(x) # добавление координаты х
        node_trace['y'].append(y) # добавление координаты у
        node_trace['marker']['size'].append(4*df_nodes['Number of publications'][i]) # добавление размера пропорционально количеству статей у автора
        node_trace['marker']['color'].append(df_nodes['Color'][i]) # добавление цвета в соответствии с компанией
         # извлечение автора для создания подписи
        auth = df_nodes['Author'][i]
        t = auth +'<br>'+'Numb of publications: '+str(df_nodes['Number of publications'][i])+'<br>'+'Company: '+str(df_nodes['Company'][i])
         # доавление подписи
        node_trace['text'].append(t)
        node_trace['name'].append(df_nodes['Company'][i])
        
    # попытка создать вершины, отнесенные к одной из компаний (может быть пригодится) 
    #comp = np.unique(df_nodes['Company'].values[0])
    #node_trace2 = []
    #edge_trace2 = []
    #for c in comp:
    #    x = []
    #    y = []
    #    xe = []
    #    ye = []
    #    buf = df_nodes.loc[df_nodes['Company']==c,'Author'].values
    #    print(buf)
    #    for i in buf:
        #        i_node = nodes.index(i+','+c)
        #        xe.append(Xe[i_node])
        #        ye.append(Ye[i_node])
        #        i_edge = edges.index()
        #        x.append(Xn[i_node])
        #        y.append(Yn[i_node])
        #    edge_trace2.append({'type':'scatter',
            #                    'mode':'lines',
            #                    'x':xe,
            #                    'y':ye,
            #                    'line':Line(color='rgb(210,210,210)', width=1),
            #                    'hoverinfo':'none'})
        #    node_trace2.append({'type':'scatter',
              #                  'mode':'markers',    
              #                  'y':y,
              #                  'x':x,
              #                  'text':buf,
              #                  'name':c,
              #                  'marker':{'size': 4*df_nodes.loc[df_nodes['Company']==c,'Number of publications'],'opacity':0.7,
            #                            'line':{'width':1.25,'color':'black'}}})

    # координатные оси и их параметры
    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='' 
          )
    # задание размера отображения
    width=1000
    height=1000
    # задание расположения графа и подписи
    layout=Layout(title= "Co-authorship network of "+param+\
              "<br> Data source: <a href='https://onepetro.org'> OnePetro</a>",  
        font= Font(size=12),
        showlegend=False,
        autosize=False,
        width=width,
        height=height,
        xaxis=XAxis(axis),
        yaxis=YAxis(axis),          
        margin=Margin(
                      l=40,
                      r=40,
                      b=85,
                      t=100,
                      ),
        hovermode='closest',
        annotations=Annotations([
           Annotation(
           showarrow=False, 
            text='This igraph.Graph has the Kamada-Kawai layout',  
            xref='paper',     
            yref='paper',     
            x=0,  
            y=-0.1,  
            xanchor='left',   
            yanchor='bottom',  
            font=Font(
            size=14 
            )     
            )
        ]),           
    )
    # запись в переменную вершин и ребер
    data=Data([edge_trace, node_trace])
    fig=Figure(data=data, layout=layout)
    # отображение и сохранение в html
    plotly.offline.plot(fig, filename='Coautorship-network-igraph.html')