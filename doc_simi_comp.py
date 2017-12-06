import logging
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora,models,similarities
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv
import os
path ='./DailyNews/'
english_stopwords = stopwords.words('english')
english_punctuations = [',','.',':',';','?','!','(',')','[',']','@','&','#','%','$','{','}','--','-']

# Go through the files in certain path, return the doc list
def path2doclist(path):
    doc_list = os.listdir(path)
    doc = []
    for docfile in doc_list:
        f=open(path+docfile,"r")
        doc.append(f.read())
        f.close()
    return doc

# filter out the stopwords, punctions etc.
def preProcess(doc):
    #texts_lower = [[word for word in document.lower().split()] for document in doc]
    texts_tokenized = [[word.lower() for word in word_tokenize(document.decode('utf-8'))] for document in doc]
    texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
    return texts_filtered

# Form the LSI matrix
def featureMatrix(doc):
    st = PorterStemmer()
    texts_filtered = preProcess(doc)
    texts_stemmed = [[st.stem(word) for word in document] for document in texts_filtered]
    dictionary = corpora.Dictionary(texts_stemmed)
    corpus = [dictionary.doc2bow(text) for text in texts_stemmed]
    lsi = models.LsiModel(corpus,id2word=dictionary,num_topics=20)
    index = similarities.MatrixSimilarity(lsi[corpus])
    return lsi, index, dictionary


# Calculating the simlilarity against the corpus
def simiQuery(comp_path, dictionary, lsi, index):
    compare_doc = []
    compare_doc_list = os.listdir(comp_path)
    for comp_file in compare_doc_list:
        try:
            file = open(comp_path+comp_file, "r")
            compare_doc.append(file.read())
            file.close()
        except:
            continue
    comp_texts = preProcess(compare_doc)
    for compare_text in comp_texts:
        vec_bow = dictionary.doc2bow(compare_text)
        vec_lsi = lsi[vec_bow]
    #print(vec_lsi)
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    sim_score = 0
    for sim in sims:
        sim_score = sim_score + sim[1]
    ave_sim = (sim_score/len(sims))
    return ave_sim


if __name__ == '__main__':

    csvfile = open('newsAveSimi.csv',"wb")
    writer = csv.writer(csvfile)
    writer.writerow(['Date','GOOGL', 'AIRT', 'CVX', 'FB', 'BOFl', 'XOM', 'MSFT'])
    # interest Co.
    dir_name = ['AAPL/', 'GOOGL/', 'AIRT/', 'CVX/', 'FB/', 'BOFl/', 'XOM/', 'MSFT/']
    # 22 trading dates
    date_list = ['0921/', '0922/', '0925/', '0926/', '0927/',
                 '0928/', '0929/', '1002/', '1003/', '1004/',
                 '1005/', '1006/', '1009/', '1010/', '1011/',
                 '1012/', '1013/', '1016/', '1017/', '1018/',
                 '1019/', '1020/']
    for i in range(len(date_list)):
        row = []
        row.append(date_list[i])
        bs_doc = path2doclist(path+dir_name[0]+date_list[i])
        lsi, index, dictionary = featureMatrix(bs_doc)
        for j in range(1,len(dir_name)):
            compath = path + dir_name[j] +date_list[i]
            simi = simiQuery(compath, dictionary, lsi, index)
            row.append(simi)
        writer.writerow(row)

    csvfile.close()
