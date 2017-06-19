#Веб-приложение: с определённой периодичностью
#скачивает новые статьи из газеты "Коммерсант"
#и строит для пользователя график частотности
#самых частотных политических терминов за неделю и за месяц

import urllib.request, re

from pymystem3 import Mystem
import pymorphy2


import matplotlib.pyplot as plt
import numpy as np


def download_page(pageUrl):
    arrUrl = []
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('windows-1251')
        arrUrl.append(pageUrl)
        #print(pageUrl)

        regex = 'b-article__text.*'
        for element in arrUrl:
            page = urllib.request.urlopen(element)
            text = page.read().decode('windows-1251')
            
        
            text_article = re.findall(regex, text, flags = 0)

            s = ''

            for el in text_article:
                s = s + el

            f = open('articles.txt','a', encoding='utf-8')
            f.write(s)
            f.close()

            #f = open('articles.txt', 'a', encoding='utf-8')
            #f.write(text_article)
            #f.close()
        
    except:
        print('Error at', pageUrl)
        return arrUrl

def text():
    f = open('articles.txt','r', encoding='utf-8')
    texts = f.read()
    regex = '<.*?>'
    regex1 = 'b-article.*?>'
    texts_clean = re.sub(regex, '', texts)
    texts_clean = re.sub(regex1, '', texts_clean)
    texts_clean = re.sub('&mdash;', '', texts_clean)
    f.close()
    f = open('cleantexts.txt', 'w', encoding='utf-8')
    f.write(texts_clean)
    
    return 0

def counting():
    f = open('cleantexts.txt', 'r', encoding='utf-8')
    text = f.read()
    arr = text.split() #делим очищенные от тегов тексты на слова
    
    arr1 = [] # массив, куда я кладу все словоформы в тексте, очищенные от знаков препинания
    for element in arr:
        element1 = element.strip('",.?!:;\n')
        arr1.append(element1) # все словоформы в тексте
    
    
    m = Mystem()
    d_count = {} #здесь будут лежать пары "лексема:частота", вообще все лексемы текста
    for element in arr1:
        try:
            lemma = m.lemmatize(element)
            lemma1 = lemma[0]      
            if lemma1 not in d_count:
                d_count[lemma1] = 1
            else:
                d_count[lemma1] += 1
        except:
            continue
     
    arr_gram = [] #здесь будут лежать грам разборы всех лексем в тексте
    i = 0
    
    for element in arr1:
        try:
            lemma = m.analyze(element) #лемматизируем все словоформы
        
            lemma1 = lemma[0]
            gram = lemma1.get('analysis')

            if gram:
                arr_gram.append(gram)
        except:
            continue
    
     
    #а дальше надо выцепить все существительные

    arr_nouns = [] # массив,в котором лежат все лексемы существитьельные
    
    for element in arr_gram:
        d_gram = element[0]  #d_gram - dict 
        if 'S,' in d_gram['gr'] and 'сокр' not in d_gram['gr']:
            arr_nouns.append(d_gram['lex'])

    d_nouns = {} # здесь лежат пары "сущ:частотность"          
    for element in arr_nouns:
        if element not in d_nouns:
            d_nouns[element] = 1
        else:
            d_nouns[element] += 1


            
   # for key in d_nouns:
#        f = open('dict.txt', 'a', encoding='utf-8')
#        f.write(key + '\n')

    return d_nouns

def drawing_graph(d_nouns):

# список политических терминов взят отсюда
# http://web-local.rudn.ru/web-local/uem/ido/13/gloss.html

    the_great_dict = ['аккламация','выборы', 'джерримандеринг',
                      'мандат', 'манипулирование','праймериз',
                      'голосование', 'ценз', 'электорат','этатизм','социализация',
                      'культура','активист','секулярность','аристократия','бихевиорализм',
                      'легальность','легитимность','легитимация','лоббизм',
                      'меритократия','пропаганда', 'харизма', 'конституция',
                      'теократия', 'абсентеизм', 'консенсус',
                      'анархизм', 'антропологизм', 'бюрократия', 'глобализация',
                      'государство', 'идентификация', 'идентичность', 'детерминизм',
                      'диктатура', 'конфессия','политический',
                      'лидер', 'либидо', 'маргинальность', 'маргинализация',
                      'монархия','демократия','патернализм', 'пацифизм',
                      'партия', 'психоанализ',  'республика',
                      'инаугурация','конфедерация','сублимация', 'статус',
                      'тирания', 'фрустрация', 'этнос', 'этология', 'парадигма',
                      'политизация', 'сегрегация', 'толерантность', 'авторитаризм',
                      'актор', 'демократия', 'идеология', 'импичмент', 'лобби',
                      'оппозиция','институционализация', 'секуляризация',
                      'полиархия', 'тоталитаризм', 'антиутопия', 'кооптация', 'остракизм',
                        'плюрализм',  'элита', 'элитология', 'федерация', 'верификационизм',
                      'вето', 'гетерогенность', 'гомогенность', 'социал-дарвинизм', 
                      'государство', 'общество', 'консенсус', 'методология', 'имидж']
    arr_X = [] #сюда занесем термины
    arr_Y = [] #сюда занесем частоты
    terms = {}
    for key in d_nouns:
        if key in the_great_dict:
            terms[key] = d_nouns[key]
    
    for key in sorted(terms, key=terms.get):
        arr_X.append(key)
        arr_Y.append(terms[key])

    terms_arr = []
    values_arr = []

    for i in reversed(arr_X):
        terms_arr.append(i)
    for element in reversed(arr_Y):
        values_arr.append(element)
    
 
        
    plt.xlabel("термины")
    plt.ylabel("частота")
    
    plt.figure(1)
    x = range(len(terms_arr))
    plt.xticks(x, terms_arr, rotation = 'vertical')
    plt.plot(x, values_arr, "g")
    plt.show()

   
 

def main():

    
    url = 'https://www.kommersant.ru/doc/'

    
    
    for i in range(3329273, 3329373):
        pageUrl = url + str(i)
        download_page(pageUrl)
    text()
    d_nouns = counting() #получаем словарь из существительных и их частот
    drawing_graph(d_nouns)
   

  
if __name__ == '__main__':
    main()
