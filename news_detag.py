#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from bs4 import BeautifulSoup

source_dir_list = ["./NASDAQ/", "./NYSE/"]
dest_dir_list = ["./DailyNews/NASDAQ/", "./DailyNews/NYSE/"]
for source_dir in source_dir_list:
    id_dir_list = os.listdir(source_dir)
    for id in id_dir_list:
        source_path = source_dir + id + "/"
        dest_path = source_path.replace("./", "./DailyNews/")
        news_list = os.listdir(source_path)
        for i in range(0, len(news_list)):
            if (i +1 ) > 21:
                break
            news = open(source_path + news_list[i],"r")
            contains = news.read()
            soup = BeautifulSoup(contains, 'lxml')
            p_tag = soup.find_all("p")
            dest_file = open(dest_path + str(i+1) +".txt", "w")
            for p in p_tag:
                dest_file.write(p.get_text())
            dest_file.close()