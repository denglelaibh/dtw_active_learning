#coding:utf-8
import sys
import time
from urllib2 import urlopen, Request
import re
from bs4  import BeautifulSoup                              #from BeautifulSoup  import BeautifulSoup 旧的版本，
import os
import csv
import json

urlBases = [ "https://finance.google.com/finance/company_news?q=NASDAQ:",
            "https://finance.google.com/finance/company_news?q=NYSE:"]



def trackNews(company, urlBase, folderName):
    fileMame = folderName + company + '.csv'
    dirName=  folderName + company + '/'
    #print fileMame
    with open(fileMame,"wb") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date","Title","Link","Status","Source"])
        start='&start='
        num = '&num='
        id = 1
        for i in range(1,40,40):
            urlAddress = urlBase+ company +start+str(i)+num+str(40)
            print( urlAddress)
            url = urlopen(urlAddress)
            soup = BeautifulSoup(url, "lxml")
            links = []
            titles = []
            n_dates=[]
            n_srcs=[]
            taglist = soup.find_all('span', attrs={'class': re.compile("name")})
            reflist = soup.find_all('div', attrs={'class': re.compile("byline")})
            for ref in reflist:
                dates = ref.find_all('span', attrs={'class': re.compile("date")})
                for date in dates:
                    n_dates.append( json.dumps( date.string ))
                srcs  = ref.find_all('span', attrs={'class': re.compile("src")})
                for src in srcs:
                    n_srcs.append(json.dumps(src.string))
            for tag in taglist:
                links.append( json.dumps( tag.a.get("href") ))
                titles.append(json.dumps(tag.a.string))
            for date in dates:
                n_dates.append(json.dumps(date.string))
            for src in srcs:
                n_srcs.append(json.dumps(src.string))
            for pos in range(0,len(links)):
                row = []
                row.append(n_dates[pos])
                row.append(titles[pos])
                row.append(links[pos])
                try:
                    request = Request(json.loads(links[pos]))
                    response = urlopen(request)
                    row.append(id)
                    name = str(id)+'_'+json.loads(n_dates[pos])+'.html'

                    open(dirName+name,"w").write(response.read())
                    id = id + 1

                except:
                    row.append("Not Reachable")
                row.append(n_srcs[pos])
                writer.writerow(row)


if __name__ == "__main__":

   companis=[
            # NASDAQ
            os.listdir("./NASDAQ/"),
            #NYSE
            os.listdir("./NYSE/")
            ]

   for i in range(len(companis)):
        for company in companis[i]:
            if i == 0:
                trackNews(company, urlBases[i], './NASDAQ/')
            else:
                trackNews(company, urlBases[i], './NYSE/')