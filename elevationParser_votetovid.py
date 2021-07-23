"""
The script is parsing the https://votetovid.ru in order to get the surface elevation.
author: Ruslan V. Akhpashev
url: https://github.com/fzybot
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

import time
import math
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
def fillUnknownHeights(fileName):
    file = open(fileName, 'r')
    localString = ''

    driver = webdriver.Chrome(ChromeDriverManager(version="91.0.4472.19").install())

    for line in file:
        localString = line.split()
        if(localString[2] == '?'):
            url = 'https://votetovid.ru/#' + str(center[0]) + comma + str(center[1]) + comma + zoom + comma \
                  + localString[0] + comma + localString[1] + i + comma + trb
    return 0

# Method calculating distance between two geographical points in [meters]
# Works fine. Tested by 2GIS.ru
def calculateDistance(lon1, lat1, lon2, lat2):
    R = 6371210
    dLon = math.radians(lon2 - lon1)
    dLat = math.radians(lat2 - lat1)
    a = math.sin(dLon / 2) * math.sin(dLon / 2) + math.cos(math.radians(lon1)) * math.cos(
        math.radians(lon2)) * math.sin(dLat / 2) * math.sin(dLat / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def interpolateHeights(lon_, lat_, localArrayHeights_):
    localSumm = 0
    counter = 1
    for i in range(len(localArrayHeights_)):
        distance = calculateDistance(lon_, lat_, localArrayHeights_[i][0], localArrayHeights_[i][1])
        if distance <= 300:
            localSumm += localArrayHeights_[i][2]
            counter += 1
    return localSumm/counter

def addHeightsToStoreys():
    fileStoreys = open("Novosibirsk_storeys_V2.txt", 'r')
    fileHeights = open("Novosibirsk_oktyabrskiy_001.txt", 'r')
    fileCombined = open("Novosibirsk_storeys_heights.txt", 'a')
    localStringStoreys = ''
    localStringHeights = ''

    localArrayStoreys = []
    localArrayHeights = []
    localArrayCombined = []
    # Parse the files in order to make one file with the same values
    for line in fileStoreys:
        localStringStoreys = line.split()
        localArrayStoreys.append( [float(localStringStoreys[0]), float(localStringStoreys[1]),
                                   int(localStringStoreys[2]), int(localStringStoreys[3])])
        for lineHeights in fileHeights:
            localStringHeights = lineHeights.split()
            if(localStringHeights[2] != '?'):
                localArrayHeights.append( [float(localStringHeights[0]), float(localStringHeights[1]), float(localStringHeights[2])] )
    pdHeights = pd.DataFrame(localArrayHeights)
    pdStoreys = pd.DataFrame(localArrayStoreys)
    print(pdHeights)

    for i in range(len(localArrayStoreys)):
        interpolValue = interpolateHeights(localArrayStoreys[i][0], localArrayStoreys[i][1], localArrayHeights)
        localArrayCombined.append( [localArrayStoreys[i][0], localArrayStoreys[i][1], localArrayStoreys[i][2],
                                  localArrayStoreys[i][3], interpolValue] )
        fileCombined.write(str(localArrayStoreys[i][0]) + ' ' + str(localArrayStoreys[i][1]) + ' ' +
                           str(localArrayStoreys[i][2]) + ' ' + str(localArrayStoreys[i][3]) + ' ' +
                           str(interpolValue) + '\n')
    pdCombined = pd.DataFrame(localArrayCombined)
    print(pdCombined)

    fileStoreys.close()
    fileHeights.close()
    fileCombined.close()
    return 0

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
    addHeightsToStoreys()
    # fillUnknownHeight('Novosibirsk_oktyabrskiy_001.txt')
    # toJSON('Novosibirsk_oktyabrskiy_001.txt', 'heightAboveSee.json')
    # main(minLon, minLat, maxLon, maxLat, step)


