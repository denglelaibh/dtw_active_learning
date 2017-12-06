#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
from dtw import dtw
from numpy.linalg import norm
import numpy as np
from sklearn import preprocessing
import csv
import pandas as pd
import os
nasdaq_pool = os.listdir("./Price_Norm/NASDAQ/")
nyse_pool = os.listdir("./Price_Norm/NYSE/")


def pool_combine(pool1, pool2):
    list = pool1
    list.extend(pool2)
    return list

def dtw_dist(price1, price2):
    x = []
    y = []
    for i in price1:
        x.append(i)
    for i in price2:
        y.append(i)
    x = preprocessing.scale(x)
    y = preprocessing.scale(y)
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    dist, cost, acc, path = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))
    return dist


if __name__ == '__main__':
    pivot = 0
    pos = 0
    dtw_result = file("./Output/dtw_simi.csv","wb")
    dtw_writer = csv.writer(dtw_result)
    pool_list = pool_combine(nasdaq_pool, nyse_pool)
    name_list = [""]
    for pool in pool_list:
        name_list.append(pool.replace(".csv",""))
    dtw_writer.writerow(name_list)
    for stock in nyse_pool:
        nasdaq_pool.remove(stock)
    while pos < len(nasdaq_pool)+len(nyse_pool):
        if pos < len(nasdaq_pool):
            row = [name_list[pos + 1]]
            price1_sf = pd.read_csv("./Price_Norm/NASDAQ/" + nasdaq_pool[pos])
            price1 = price1_sf["Price"]
            for file in nasdaq_pool:
                price2_sf = pd.read_csv("./Price_Norm/NASDAQ/" + file)
                price2 = price2_sf["Price"]
                dist = dtw_dist(price1, price2)
                row.append(dist)
            for file in nyse_pool:
                price2_sf = pd.read_csv("./Price_Norm/NYSE/" + file)
                price2 = price2_sf["Price"]
                dist = dtw_dist(price1, price2)
                row.append(dist)
            dtw_writer.writerow(row)
            pos += 1
        else:
            row = [name_list[pos + 1]]
            price1_sf = pd.read_csv("./Price_Norm/NYSE/" + nyse_pool[pos - len(nasdaq_pool)])
            price1 = price1_sf["Price"]
            for file in nasdaq_pool:
                price2_sf = pd.read_csv("./Price_Norm/NASDAQ/" + file)
                price2 = price2_sf["Price"]
                dist = dtw_dist(price1, price2)
                row.append(dist)
            for file in nyse_pool:
                price2_sf = pd.read_csv("./Price_Norm/NYSE/" + file)
                price2 = price2_sf["Price"]
                dist = dtw_dist(price1, price2)
                row.append(dist)
            dtw_writer.writerow(row)
            pos += 1
    dtw_result.close()