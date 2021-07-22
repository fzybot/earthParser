"""
The script is parsing the https://votetovid.ru in order to get the surface elevation.
author: Ruslan V. Akhpashev
url: https://github.com/fzybot
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import random
import json

# Start URL format
# 'center' value could not be changed in future, only 'point'
center = [55.0166, 82.9544] # Novosibirsk coordinates
comma = ','
zoom = '16z'
pointer = [55.018772, 82.954974]
i = "i"
trb = 'trb'
# url = 'https://votetovid.ru/#' + str(center[0]) + comma + str(center[1]) + comma + zoom + comma \
#       + str(pointer[0]) + comma + str(pointer[1]) + i + comma + trb

# rectangle borders around the 'center'  -> 55.013843,82.947824,15.75z
borders = [55.009069999999994, 82.933401, 55.018151, 82.960240]
minLon = borders[0]
minLat = borders[1]
maxLon = borders[2]
maxLat = borders[3]

step = 0.0001 # around 60 meters

def writeIntoFileArray(fileName, lon, lat, data):
    f = open(fileName, 'a')
    for i in range(len(data)):
        f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

def writeIntoFile(fileName, lon, lat, data):
    f = open(fileName, 'a')
    f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

def parceOnePoint(Lon_, Lat_):
    driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.19").install())
    url = 'https://votetovid.ru/#' + str(center[0]) + comma + str(center[1]) + comma + zoom + comma \
          + str(Lon_) + comma + str(Lat_) + i + comma + trb
    driver.get(url)
    html_ = driver.page_source
    # for this part of the code you will need to install lxml module: pip install lxml
    soup = BeautifulSoup(html_, 'lxml')
    span_txHgt = soup.find_all('span')[0]
    height = span_txHgt.text
    return height

# TODO:
# Fill the '?' symbol with the actual height
def fillUnknownHeight(fileName):
    file = open(fileName, 'r')
    localString = ''

    driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.19").install())

    for line in file:
        localString = line.split()
        if(localString[2] == '?'):
            url = 'https://votetovid.ru/#' + str(center[0]) + comma + str(center[1]) + comma + zoom + comma \
                  + localString[0] + comma + localString[1] + i + comma + trb
    return 0

def toJSON(inputFile, outputFile):
    iFile = open(inputFile, 'r')
    oFile = open(outputFile, 'a')
    localString = ''
    for line in iFile:
        localString = line.split()

        print(localString)

def main(minLon_, minLat_, maxLon_, maxLat_, step):
    driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.19").install())
    pointer[0] = minLon_
    print("number of steps: ", round((maxLon_ - minLon_) / step))
    for k in range(round((maxLon_ - minLon_) / step)):
        pointer[0] += step
        pointer[1] = minLat_
        for j in range(round((maxLat_ - minLat_) / step)):
            pointer[1] += step
            url = 'https://votetovid.ru/#' + str(center[0]) + comma + str(center[1]) + comma + zoom + comma \
                  + str(pointer[0]) + comma + str(pointer[1]) + i + comma + trb
            # height = '?'
            # while(height == '?'):
            driver.get(url)
            time.sleep(random.randint(1, 5))
            html_ = driver.page_source
            # for this part of the code you will need to install lxml module: pip install lxml
            soup = BeautifulSoup(html_, 'lxml')
            span_txHgt = soup.find_all('span')[0]
            height = span_txHgt.text
            print(pointer[0], pointer[1], height)
            writeIntoFile('Novosibirsk_oktyabrskiy_0001.txt', pointer[0], pointer[1], height)

if __name__ == '__main__':

    # fillUnknownHeight('Novosibirsk_oktyabrskiy_001.txt')
    toJSON('Novosibirsk_oktyabrskiy_001.txt', 'heightAboveSee.json')
    # main(minLon, minLat, maxLon, maxLat, step)


