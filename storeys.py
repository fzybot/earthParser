"""
The script is parsing the https://2gis.ru in order to find out the number of storeys
author: Ruslan V. Akhpashev, Timofey M. Leonenko
url: https://github.com/fzybot
"""

from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import re
import random
import math
import cmath

#from bs4 import BeautifulSoup

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

# rectangle borders around the 'center'
borders = [55.009069999999994, 82.933401, 55.018151, 82.960240] #- goal

#borders = [55.013004, 82.948081, 55.013025, 82.948161]

minLat = borders[0]
minLon = borders[1]
maxLat = borders[2]
maxLon = borders[3]

#step = 0.0001 # around 6 meters
step = 0.000166     #around 10 meters


#earthRad = 6371200      # [m] - Earth's radius
#earthSMAxis = 6378200  # [m] - equator
#earthCom = 1/298.3      # Compression


def writeIntoFileArray(filename, lon, lat, data):
    f = open(filename, 'a')
    for i in range(len(data)):
        f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

def writeIntoFile(filename, lon, lat, data):
    f = open(filename, 'a')
    f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

def initSpher(a, f):
    b = a * (1. - f)
    c = a / (1. - f)
    e2 = f * (2. - f)
    e12 = e2 / (1. - e2)
    return (b, c, e2, e12)

def fromLatLong(lat, lon, h, a, f):
    b, c, e2, e12 = initSpher(a, f)
    cos_lat = math.cos(lat)
    n = c / math.sqrt(1. + e12 * cos_lat ** 2)
    p = (n + h) * cos_lat
    x = p * math.cos(lon)
    y = p * math.sin(lon)
    z = (n + h - e2 * n) * math.sin(lat)
    return (x, y, z)

def toLatLong(x, y, z, a, f):
    b, c, e2, e12 = initSpher(a, f)
    p = math.hypot(x, y)
    if p == 0.:
        lat = math.copysign(math.pi / 2., z)
        lon = 0.
        h = math.fabs(z) - b
    else:
        t = z / p * (1. + e12 * b / math.hypot(p, z))
        for i in range(2):
            t = t * (1. - f)
            lat = math.atan(t)
            cos_lat = math.cos(lat)
            sin_lat = math.sin(lat)
            t = (z + e12 * b * sin_lat ** 3) / (p - e2 * a * cos_lat ** 3)
        lon = math.atan2(y, x)
        lat = math.atan(t)
        cos_lat = math.cos(lat)
        n = c / math.sqrt(1. + e12 * cos_lat ** 2)
        if math.fabs(t) <= 1.:
            h = p / cos_lat - n
        else:
            h = z / math.sin(lat) - n * (1. - e2)
    return (lat, lon, h)



def main(minLon_, minLat_, maxLon_, maxLat_, step):


    pointer[1]=minLon
    pointer[0]=minLat

    while pointer[1]<=maxLon and pointer[0]<=maxLat:
        driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")
        url = 'https://2gis.ru/novosibirsk/geo/' + str(pointer[1]) + '%2C' + str(pointer[0]) + "?m=" + str(
            pointer[1]) + '%2C' + str(pointer[0]) + "%2F16"
        driver.get(url)
        time.sleep(random.randint(1, 5))

        element = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]")

        height = re.findall("\d{1,2} этаж\w*", element.text)
        if height:
            if len(height) == 1:
                height = height.pop(0)
            else:
                height = height.pop(len(height) - 1)

            test = str(height).find("'")
            text = str(height)[test + 1:test + 3]
        else:
            text = "0"

        writeIntoFile('Novosibirsk_storeys.txt', pointer[0], pointer[1], text)

        pointer[1]+=step
        if pointer[1]>maxLon:
            pointer[1]=minLon
            pointer[0]+=step

        driver.close()



if __name__ == '__main__':
    main(minLon, minLat, maxLon, maxLat, step)


