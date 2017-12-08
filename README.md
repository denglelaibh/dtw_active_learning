# dtw_active_learning
An improvement experiment on combination between dtw and text simi, with active learning.
* [DailyNews](./DailyNews) Saving the detaged news in two directories
  * [NASDAQ](./DailyNews/NASDAQ) Nasdaq detaged news text
  * [NYSE](./DailyNews/NYSE) NYSE detaged news text
* [Historial_Data](./History_Data) Initial historial trading data, from Yahoo Finance
  * [NASDAQ](./History_Data/NASDAQ) Initial trading data of Nasdaq
  * [NYSE](./History_Data/NYSE) Initial trading data of NYSE
* [NASDAQ_record](./NASDAQ_record) Records for the source and related info of Nasdaq News
* [NYSE_record](./NYSE_record) Records for the source and related info of NYSE News
* [Output](./Output) output files
* [Price_Norm](./Price_Norm) Normalized close prices of each stock
* [create_folder.py](create_folder.py) create related folders
* [doc_simi_comp.py](doc_simi_comp.py) compare the cosine similarity of stockes daily news
* [dtw_simi.csv](dtw_simi.csv) Similarity Matrix of dtw
* [dtw_time_series.py](dtw_time_series.py) Calculate the dtw distance
* [folder_cleaner.py](folder_cleaner.py) Clean the rubbish of folder
* [main.py](main.py) Calculate the score, using Active Learning to find appropriate w value
* [news_clean.py](folder_cleaner.py) Clean the rubbish news of  news  folder
* [news_detag.py](news_detag.py) Remove the tags of html files
* [news_normalize.py](news_normalize.py) Return the normalized close price of each stock
* [news_simi_compare.py](news_simi_compare.py) Compare the text cosine similarity of each pair of  stocks
* [series_scrapy.py](series_scrapy.py) Get the daily news of stocks
* [text_avg_simi.csv](text_avg_simi.csv) Text simi matix of stocks
