#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import os
from dtw import dtw
import pandas as pd
from numpy.linalg import norm
import numpy as np
import csv
from sklearn import preprocessing
import random
# AAPL FB
source_dir = './Historial_Data/'
dest_dir = './Price_Norm/'
stock_class_list =["NASDAQ/", "NYSE/"]


def stdlize(x):
    x_n = []
    if np.std(x) == 0:
        return None
    else:
        for price in x:
            price = (price - np.mean(x)) / np.std(x)
            x_n.append(price)
        return x_n

if __name__ == '__main__':
    for stock_class in stock_class_list:
        source_path = source_dir + stock_class
        dest_path = dest_dir + stock_class
        file_list = os.listdir(source_path)
        for file in file_list:
           dest = dest_path + file
           dest_file = open(dest, "wb")
           writer = csv.writer(dest_file)
           writer.writerow(['Price'])
           price_sf = pd.read_csv(source_path + file)
           price = price_sf["Close"]
           x = []
           for i in price:
               x.append(i)
           y = stdlize(x)
           if y is None:
               print(source_path+file)
           else:
                for line in y:
                    writer.writerow([line])
