#-*- coding:utf-8 -*-
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora,models,similarities
import numpy as np
import os
import csv
#import pandas as pd


#预处理，去停词、符号
def pre_process(doc):
    #对于每个文档，先进行utf-8解码，然后进行tokenize，再对每个单词小写化
    texts_tokenized = [[word.lower() for word in word_tokenize(document)] for document in doc]

    #过滤完停用词，但是标点符号没有过滤
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]

    english_punctuations = [',','.',':',';','?','!','(',')','[',']','@','&','#','%','$','{','}','--','-']
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
    return texts_filtered

def text_comp(path1, path2):
    doc = []

    addresses = os.listdir(path1)
    for address in addresses:
        try:
            file = open(path1+address,'r')
            doc.append(file.read())
            #doc.extend(file.read())
            file.close()
        except:
            continue


    #接下来将这些英文单词词干化，词干化可以提取不同语态及各种后缀的词干
    texts_filtered = pre_process(doc)
    print(texts_filtered)
    st = PorterStemmer()
    texts_stemmed = [[st.stem(word) for word in document] for document in texts_filtered]
    all_stems = sum(texts_stemmed,[])
    stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
    texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]

    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]

    #print(corpus)
    lsi = models.LsiModel(corpus,id2word=dictionary,num_topics=20)
    index = similarities.MatrixSimilarity(lsi[corpus])
    print(index)

    compare_doc = []

    addresses = os.listdir(path2)
    for address in addresses:
        file=open(path2 + address,"r")
        compare_doc.append(file.read())
        file.close()
    compare_texts = pre_process(compare_doc)
    ave_sim = []
    for compare_text in compare_texts:
        vec_bow = dictionary.doc2bow(compare_text)
        vec_lsi = lsi[vec_bow]
        #print(vec_lsi)
        sims = index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        #print(sims)
        sim_score = 0
        for sim in sims:
            sim_score = sim_score + sim[1]
        ave_sim.append(sim_score/len(sims))
    print(ave_sim)
    if len(ave_sim)!=0:
        return (sum(ave_sim)/len(ave_sim))
    else:
        return 0

def path_gen(path):
    folder_list= os.listdir(path)
    path_list = []
    for folder in folder_list:
        path_list.append(path+folder+"/")
    return path_list

if __name__ == '__main__':
    dir_name = ["./DailyNews/NASDAQ/", "./DailyNews/NYSE/"]
    path_list = []
    name = [""]
    for dir in dir_name:
        path_list.extend(path_gen(dir))
        for stock in os.listdir(dir):
            name.append(stock)

    file = open("text_avg_simi.csv", "w")
    writer = csv.writer(file)
    writer.writerow(name)
    for i in range(1, len(name)):
        row = []
        row.append(name[i])
        for j in range(0, len(path_list)):
            if (i - 1) == j:
                row.append(1)
            else:
                row.append(text_comp(path_list[i-1], path_list[j]))
        writer.writerow(row)

    file.close()

