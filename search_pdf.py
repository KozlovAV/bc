# -- coding: utf-8 --

from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

mypath = 'd://00.Inbox//bootcamp3//html//'

onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
# print (onlyfiles)


for filename in onlyfiles:
        with open(filename, 'r', encoding='utf-8') as source:
            print('processing file ... ' + filename)
            # soup = BeautifulSoup(source, 'html.parser')
            soup = BeautifulSoup(source, 'lxml')
            links = soup.find_all('a')
            links = [link for link in links if 'pdf' in link.get('href') and 'publicoffer_msk.pdf' not in  link.get('href')]
            print ('  ', links)