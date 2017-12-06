import os
list = os.listdir("./NYSE/")
n_list = []
for i in list:
    i = i.replace(".csv","")
    n_list.append(i)
print n_list

for dir in n_list:
    dir = "./NYSE/"+dir
    os.mkdir(dir)