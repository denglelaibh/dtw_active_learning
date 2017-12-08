import pandas as pd
import numpy as np
import os

def list_create(list, path):
    for name in os.listdir(path):
        list.append(name)
    return list

def act_simi_calc(dtw_simi, text_simi, w):
    return dtw_simi + w * (1 - text_simi)

if __name__ == '__main__':
    text_simi_file = "text_avg_simi.csv"
    text_simi_pd = pd.read_csv(text_simi_file)
    dtw_simi_file = "dtw_simi.csv"
    dtw_simi_pd = pd.read_csv(dtw_simi_file)
    stock_list = []
    score_list = []
    path_list = ["./DailyNews/NASDAQ/", "./DailyNews/NYSE/"]
    for path in path_list:
        stock_list = list_create(stock_list, path)
    w = 0.6
    for i in range(0, len(stock_list)):
        for j in range(i+1, len(stock_list)):
            score_list.append((stock_list[i], stock_list[j], dtw_simi_pd[stock_list[i]][j],
                               1 - text_simi_pd[stock_list[i]][j], act_simi_calc(dtw_simi_pd[stock_list[i]][j],
                                                                           text_simi_pd[stock_list[i]][j],
                                                                           w)))
    sorted_score = (sorted(score_list, key = lambda t:(t[-1])))
    print(sorted_score[:5])
    print(sorted_score[-6 : -1])
