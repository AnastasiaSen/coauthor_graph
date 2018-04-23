# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:28:55 2018

@author: Ася
"""

from data_creator import pre_processing
from flask import Flask, render_template, request
from graph_flask import plot_graph
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def search():
    result = '' # переменная для записи результата (поясняющая надпись)
    error = '' # переменная для записи ошибки
    # получаем данные с веб-страницы
    if request.method=='POST':
        # если нажата кнопка поиска
        query = request.form['query'] # запрос - ключевые слова
        f_year = request.form['f_year'] # год, с которого начать просмотр
        t_year = request.form['t_year'] # год, младше которого не рассматривать
        numb = request.form['numb']  # количество анализируемых публикаций
        if request.form['submit'] == 'Search':
            # если запрос введен
            if query:
                try:       
                    pre_processing(query, f_year, t_year, numb) # вызываем функцию обработки данных и записи их в файл
                    result = 'csv files are ready' # посяняюзщая надпись
                except ValueError:
                    # ошибка
                    error = 'Please write your query.'
        # если нажата кнопка построения графа
        elif request.form['submit'] == 'Plot graph':
            try:
                param = query
                if f_year != '':
                    param = param+', from year '+f_year
                if t_year != '':
                    param = param+', to year '+t_year 
                if numb != '':
                    param = param+', number of publications '+numb
                param = '"'+param+'"'
                plot_graph(param) # вызов функции построения графа
                result = 'Graph is plot' # поясняюща надпись
            except ValueError:
                error = 'Some error with data' # ошибка с данными
     # вывод результатов на веб страницу
    return render_template('search_ui2.html', result=result, error=error)

if __name__ == "__main__":
    app.run(threaded=True)