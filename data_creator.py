# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 14:39:14 2018

@author: Ася
"""

from igraph import *
from plotly.graph_objs import *
import requests, re
from bs4 import BeautifulSoup
from collections import Counter
import itertools
import csv
import random
import plotly
plotly.offline.init_notebook_mode(connected=True)

import plotly.offline as pyo
pyo.offline.init_notebook_mode()
import math
from collections import OrderedDict
from operator import itemgetter

""" функция замены наименования компаний (можно добавлять аналогично дрцгие исключения)"""
def rename(company):
    company = re.sub(r' U ', ' University ', company) 
    company = re.sub(r' U. ', ' University ', company)
    company = re.sub(r'[\s\S]*Skol[\s\S]*', 'Skolkovo', company) 
    company = re.sub(r'[\s\S]*ADNOC[\s\S]*', 'ADNOC', company) 
    company = re.sub(r'[\s\S]*Beicip[\s\S]*', 'Beicip', company)
    company = re.sub(r'[\s\S]*BP[\s\S]*', 'BP', company)
    company = re.sub(r'[\s\S]*Southwest Petroleum University[\s\S]*', 'Southwest Petroleum University', company)
    company = re.sub(r'[\s\S]*SOUTHWEST[\s\S]*', 'Southwest Petroleum University', company)
    company = re.sub(r'[\s\S]*CEPSA[\s\S]*', 'CEPSA', company)
    company = re.sub(r'[\s\S]*Chevron[\s\S]*', 'Chevron', company)
    company = re.sub(r'[\s\S]*China University of Petroleum[\s\S]*', 'China University of Petroleum', company)
    company = re.sub(r'[\s\S]*Computer Modelling Group[\s\S]*', 'Computer Modelling Group', company)
    company = re.sub(r'[\s\S]*Croda Europe[\s\S]*', 'Croda Europe', company)
    company = re.sub(r'[\s\S]*Ecopetrol[\s\S]*', 'Ecopetrol', company)
    company = re.sub(r'[\s\S]*[Ee]ni [Ss]*.*[Pp]*.*[Aa]*[\s\S]*', 'Eni SpA', company)
    company = re.sub(r'[\s\S]*eni SpA [\s\S]*', 'Eni SpA', company)
    company = re.sub(r'[\s\S]*Epic Consulting[\s\S]*', 'Epic Consulting', company)
    company = re.sub(r'[\s\S]*Exxon[\s\S]*', 'Exxon', company)
    company = re.sub(r'[\s\S]*H[Ee][Ss][sS][\s\S]*', 'Hess', company)
    company = re.sub(r'[\s\S]*IFP[\s\S]*', 'IFP', company)
    company = re.sub(r'[\s\S]*Imperial College[\s\S]*', 'Imperial College', company)
    company = re.sub(r'[\s\S]*T[Aa][Tt][Nn][Ee][Ff][Tt][\s\S]*', 'Tatneft', company)
    company = re.sub(r'[\s\S]*Missouri University of Science & Tech[\s\S]*', 'Missouri University of Science & Tech', company)
    company = re.sub(r'[\s\S]*Mobil[\s\S]*', 'Mobil', company)
    company = re.sub(r'[\s\S]*OMV[\s\S]*', 'OMV', company)
    company = re.sub(r'[\s\S]*PDVSA[\s\S]*', 'PDVSA', company)
    company = re.sub(r'[\s\S]*Petroleum Recovery Institute[\s\S]*', 'Petroleum Recovery Institute', company)
    company = re.sub(r'[\s\S]*Petronas[\s\S]*', 'Petronas', company)
    company = re.sub(r'[\s\S]*PETRONAS[\s\S]*', 'Petronas', company)
    company = re.sub(r'[\s\S]*Rogaland Research[\s\S]*', 'Rogaland Research', company)
    company = re.sub(r'[\s\S]*Salym Petroleum[\s\S]*', 'Salym Petroleum', company)
    company = re.sub(r'[\s\S]*Schlumb?erger[\s\S]*', 'Schlumberger', company)
    company = re.sub(r'[\s\S]*S[Hh][Ee][Ll]+[\s\S]*', 'Shell', company)
    company = re.sub(r'[\s\S]*Solvay[\s\S]*', 'Solvay', company)
    company = re.sub(r'[\s\S]*SPD[\s\S]*', 'SPD', company)    
    company = re.sub(r'[\s\S]*ADMA[\s\S]*', 'ADMA', company)
    company = re.sub(r'[\s\S]*Statoil[\s\S]*', 'Statoil', company)
    company = re.sub(r'[\s\S]*Abu Dhabi Co[\s\S]*', ' Abu Dhabi Company for Onshore Petroleum Operations Ltd.', company)
    company = re.sub(r'[\s\S]*ADCO[\s\S]*', 'ADCO', company)
    company = re.sub(r'[\s\S]*Advanced Resources International[\s\S]*', 'Advanced Resources International', company)
    company = re.sub(r'[\s\S]*Anadarko[\s\S]*', 'Anadarko', company)
    company = re.sub(r'[\s\S]*A[Rr][Cc][Oo][\s\S]*', 'Arco', company)
    company = re.sub(r'[\s\S]*Bandung Institute of Technology[\s\S]*', 'Bandung Inst. of Tech', company)
    company = re.sub(r'[\s\S]*China Natl[.]* Offshore Oil Corp[\s\S]*', 'China National Offshore Oil Corp.', company)
    company = re.sub(r'[\s\S]*CNOOC[\s\S]*', 'CNOOC', company)
    company = re.sub(r'[\s\S]*CNPC[\s\S]*', 'CNPC', company)
    company = re.sub(r'[\s\S]*Conoco[\s\S]*', 'Conoco', company)
    company = re.sub(r'[\s\S]*Kelko[\s\S]*', 'CP Kelko', company)
    company = re.sub(r'[\s\S]*Culgi[\s\S]*', 'Culgi BV', company)
    company = re.sub(r'[\s\S]*IRIS[\s\S]*', 'IRIS', company)
    company = re.sub(r'[\s\S]*JOGMEC[\s\S]*', 'JOGMEC', company)
    company = re.sub(r'[\s\S]*King Saud University[\s\S]*', 'King Saud University', company)
    company = re.sub(r'[\s\S]*Maersk Oil[\s\S]*', 'Maersk Oil', company)
    company = re.sub(r'[\s\S]*Nalco[\s\S]*', 'Nalco', company)
    company = re.sub(r'[\s\S]*Repsol[\s\S]*', 'Repsol', company)
    company = re.sub(r'[\s\S]*SNF[\s\S]*', 'SNF', company)
    company = re.sub(r'[\s\S]*Staatsolie[\s\S]*', 'Staatsolie Suriname NV', company)
    company = re.sub(r'[\s\S]*Surtek[\s\S]*', 'Surtek', company)
    company = re.sub(r'[\s\S]*University of Alaska[\s\S]*', 'University of Alaska', company)
    company = re.sub(r'[\s\S]*Petrobras[\s\S]*', 'Petrobras', company)
    company = re.sub(r'[\s\S]*Petroleum Development[ of Oman]?[s\S]*', 'Petroleum Development Oman', company)
    company = re.sub(r'[\s\S]*P[oO][wW][eE][lL][tT][eE][cC][\s\S]*', 'Poweltec', company)
    company = re.sub(r'[\s\S]*Texas A&M University[\s\S]*', 'Texas A&M University', company)
    company = re.sub(r'[\s\S]*The University of Adelaide[\s\S]*', 'The University of Adelaide', company)
    company = re.sub(r'[\s\S]*Tiorco[\s\S]*', 'Tiorco', company)
    company = re.sub(r'[\s\S]*TIORCO[\s\S]*', 'Tiorco', company)
    company = re.sub(r'[\s\S]*T[Oo][Tt][Aa][Ll][\s\S]*', 'Total E&P', company)
    company = re.sub(r'[\s\S]*Turkish Petroleum[\s\S]*', 'Turkish Petroleum', company)
    company = re.sub(r'[\s\S]*of Texas at Austin[\s\S]*', 'The University of Texas at Austin', company)
    company = re.sub(r'[\s\S]*VNIIneft[\s\S]*', 'VNIIneft JSC', company)
    company = re.sub(r'[\s\S]*Wintershall Holding GmbH[\s\S]*', 'Wintershall Holding GmbH', company)
    return company
    
def pre_processing(query, f_year, t_year, numb):
    query = query.replace(" ", "+") # заменяем пробел знаком +
    param = query+'&peer_reviewed=&published_between=&from_year='+f_year+'&to_year='+t_year+'&rows=25&start='  # формируем параметры запроса
    url = 'https://www.onepetro.org/search?q='+param+str(0) # доступ к странице запроса
    html = requests.get(url) # извлечение html кода
    N= re.findall(r'<h2>[a-zA-Z:\s.]+([\s,0-9]+)\s', html.text)[0] # извлечение строки, гда содержится информация о числе результатов
    N = N.replace(",", "") # удаление запятых 
    N = N.replace(" ", "") # удаление пробелов
    # если введено ограничение на количество статей, то учитываем его
    if numb != '':
        if int(numb)<int(N):
            N = numb

    auths = []
    forgraph = []
    comp = []
    # для каждой страницы (по 100 статей) выполняем
    for ii in range(0, math.ceil(int(N)/100)):
        url = 'https://www.onepetro.org/search?q='+param+str(ii*100) # доступ к старнице
        html = requests.get(url) # извлечение html
        soup = BeautifulSoup(html.text, 'html.parser') #извлекаем текст из html
#        soup = BeautifulSoup(html, 'html.parser') # для тестирования на текстовом файле
        papers = soup('div', {"class":"result-item"}) # извлекаем все статьи на странице
        # для каждой публикации (они все ограничены тегом "result-item")
        for p in papers:
            authors=[] # массив для записи всех авторов статьи
       
            #extract authors
            auth = p('div', {"class":"result-item-author"}) #для каждого класса с пометкой "result-item-author" автора
            for tag in auth:
                tag = re.sub(r'\s+',' ',tag.text) # удаляем все лишние пробелы и переносы
                tag = tag.replace('&amp;', '') #удаляем служебные символы &, числа и тд
                tag = tag.replace('&amp;apos;', '')
                tag = tag.replace('&apos;', '')
                tag = tag.replace('Ø', 'O')
                tag = tag.replace('ª', 'a')
                tag = tag.replace('©', 'c')                
                tag = re.sub(r'#[0-9]*;', '', tag)
                # если есть подходящие под шаблон строки
                if (re.findall(r"^ ([àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, \S{1})[À-ÿa-zA-Z-_;()'&.\s]*,", tag) != []):
                    authors.append(re.findall(r'^ ([àèéìíîòóóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿa-zA-Z0-9-.,&\s\S]*)', tag)[0])
                    company = ''.join(re.findall(r"^[àèéìíîòóóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, [àèéìíîòóóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+,([\s\S]+)", tag))
                    company = rename(company)
                    auths.append(re.findall(r"^ ([àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, \S{1})[À-ÿa-zA-Z-_;()'&.\s]*,", tag)[0]+'.'+','+company)
            # составление комбинаций авторов (апример для А,Б,В получим АА, АБ, АВ, ББ, БВ, ВВ)
            A = itertools.combinations_with_replacement(authors,2) 
            for i in A:
                l=[]
                # компания и авор первого элемена из комбинации
                company = ''.join(re.findall(r"^[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, [àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+,([\s\S]+)", i[0]))
                company = rename(company)            
                l.append(re.findall(r"^([àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, \S{1})[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿa-zA-Z-_;()'&.\s]*,", i[0])[0]+'.'+','+company)
                # компания и авор второго элемена из комбинации
                company = ''.join(re.findall(r"^[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, [àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+,([\s\S]+)", i[1]))
                company = rename(company)   
                l.append(re.findall(r"^([àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, \S{1})[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿa-zA-Z-_;()'&.\s]*,", i[1])[0]+'.'+','+company)
                # запись в общий массив
                forgraph.append(l)
    auths = OrderedDict(sorted(dict(Counter(auths)).items(), key=itemgetter(1))) # словарь со всеми авторами - без повторов, ключь - фамилия, значение - количество статей
    reb = auths[(list(auths)[len(auths)*2//10])] # порог, по которому отсекаем авторов (80%)
    new_auths = {k: v for k, v in auths.items() if v >reb} # новый список авторов - без "малостатейных"

    pairs = set() # перемнная для записи пар автор-соавтор, которые вошли в 80%
    for i in forgraph:
        # условие что и автор и соавтор входят в 80%
        if ((i[0] in list(new_auths)) & (i[1] in list(new_auths))):
            pairs.add(tuple(i))
            # запись в перемнную компаний 
            comp.append(''.join(re.findall(r"^[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, [àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+,([\s\S]+)", i[0])))
            comp.append(''.join(re.findall(r"^[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, [àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+,([\s\S]+)", i[1])))

    comp = dict(Counter(comp)) # словарь для компаний
    color = [] # переменная для записи цветов 
    # цикл для задания рандомных цветов (нужно бы что-то другое найти, чтоб они не были блеклыми)
    for c, v in comp.items():
        r = lambda: random.randint(0,255)
        r = '#%02X%02X%02X' % (r(),r(),r())
        color.append(r)

    # запись в csv файл вершин
    outfile = open('node.csv','w', newline='')
    writer=csv.writer(outfile, delimiter =';')
    writer.writerow(['Author', 'Company', 'Number of publications', 'Color'])
    for k, v in new_auths.items():
        n = list(comp).index(re.findall(r"^[àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, [àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+,([\s\S]*)", k)[0])
        writer.writerow([re.findall(r"^([àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿA-Za-z-_;()'&.\s]+, [àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚÀ-ÿa-zA-Z-_;()'&.\s]+),",k)[0], re.findall(r"^[A-Za-z-_;()'&.\s]+, [A-Za-z-_;()'&.\s]+,([\s\S]*)", k)[0], str(v),  str(color[n])])
    outfile.close()

    # запись в csv файл ребер
    outfile = open('edges.csv','w', newline='')
    writer=csv.writer(outfile, delimiter =';')
    writer.writerow(['Author, company', 'Co-author, company'])
    for f in pairs:
        writer.writerow(f)
    outfile.close()