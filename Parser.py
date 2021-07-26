import json
import numpy as np
import matplotlib.pyplot as plt
import math
import re
import time
from mpl_toolkits.mplot3d import Axes3D

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Parser:
    """Here is Parser!"""
# -------------------------PLOT----------------------------------#
    __slots__ = ['__plots', '__borders', '__pointer', '__step']
    def __init__(self):
        self.__plots = {}
        self.__borders = []
        self.__pointer = [0.0, 0.0]
        self.__step = 1

    def addPlot(self,name):
        self.__plots[name] = {
            "axis":{
            "x":{"name":"X","value":0},
            "y":{"name":"Y","value":0},
            "z":{"name":"Z","value":0, "step":1, "limit":200}
        }}

    def getPlotsName(self):
        return self.__plots.keys()

    def delPlot(self,name):
        del(self.__plots[name])

    def getPlotSettings(self,num):
        return self.__plots[num]

    def configPlot(self, num, plot):
        self.__plots[num] = plot

    def setBorders(self,borders):
        self.__borders = borders

    def getBorders(self):
        return self.__borders

    def readFromTxtFile(self,fileName, *args):
        """Read .txt file's columns and convert they to one list of lists"""
        f = open(fileName, 'r')
        if f:
            data = f.readlines()

            lists=[[]for i in args]
            for n in args:
                for line in range(0, len(data)):
                    lists[args.index(n)].append(data[line].split()[n])
        return (lists)

    def writeInFile(fileName, *args):
        """Write lists in .txt file"""
        f = open(fileName, 'w')
        length = len(args[0])
        for i in range(length):
            line = ''
            for n in args:
                line += str(n[i]) + ' '
            line += '\n'
            f.write(line)
        f.close()


    def __checkCells(self, lon, lat, i, j, checkI, checkJ):
        if (checkI + i) < 0:
            checkI = 0
        else:
            if (checkI + i) >= lon:
                checkI = 0

        if (checkJ + j) < 0:
            checkJ = 0
        else:
            if (checkJ + j) >= lat:
                checkJ = 0

        return (checkI, checkJ)

    def plot(self, list):
        """Plot"""
        for name in list:
            new_x = sorted(self.__plots[name]["axis"]["x"]["value"])

            y_len = 0
            while new_x[0] == new_x[y_len]:
                y_len += 1

            x_len = int(len(self.__plots[name]["axis"]["x"]["value"]) / y_len)

            Z = np.zeros((x_len, y_len))
            for i in range(x_len):
                for j in range(y_len):
                    Z[i][j] = self.__plots[name]["axis"]["z"]["value"][i * y_len + j]

            X = np.arange(0, y_len, 1)
            Y = np.arange(0, x_len, 1)
            X, Y = np.meshgrid(X, Y)

            fig = plt.figure()

            ax = Axes3D(fig, auto_add_to_figure=False, box_aspect=(1, 1 * (x_len / y_len), self.__plots[name]["axis"]["z"]["step"]),title=name)
            fig.add_axes(ax)

            ploT = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', antialiased=True)

            ax.set(xlim=[0, y_len], ylim=[0, x_len], zlim=[0, self.__plots[name]["axis"]["z"]["limit"]])

            ax.set_xlabel(self.__plots[name]["axis"]["x"]["name"], labelpad=20)
            ax.set_ylabel(self.__plots[name]["axis"]["y"]["name"])
            ax.set_zlabel(self.__plots[name]["axis"]["z"]["name"])

            fig.colorbar(ploT, shrink=0.3, aspect=5)

        plt.show()

    def getBuildingsBoundaries(self, lat, lon, storey):
        latC = 0
        while lat[0] == lat[latC]:
            latC += 1

        lonC = int(len(lon) / latC)

        map = [[0 for j in range(latC)] for i in range(lonC)]

        Z = np.zeros((lonC, latC))

        for i in range(lonC):
            for j in range(latC):
                map[i][j] = int(storey[i * latC + j])

        buildingID = 2
        for i in range(0, lonC, 1):
            for j in range(0, latC, 1):
                if map[i][j] == 0:
                    Z[i][j] = 1

        for i in range(0, lonC, 1):
            for j in range(0, latC, 1):
                if Z[i][j] == 0:
                    self.__check(i, j, i, j, map, Z, lonC, latC, buildingID)
                    buildingID += 1

        buildings = [0 for i in range(len(lat))]

        for i in range(lonC):
            for j in range(latC):
                buildings[i * latC + j] = int(Z[i][j])

        return (buildings)

    def __check(self, origin_i, origin_j, i, j, map, mapA, lonC, latC, bulID):
        for check_i in range(-1, 2):
            for check_j in range(-1, 2):
                check_i, check_j = self.__checkCells(lonC, latC, i, j, check_i, check_j)
                if i == check_i and j == check_j:
                    continue
                if map[origin_i][origin_j] == map[i + check_i][j + check_j]:
                    if mapA[i + check_i][j + check_j] == 0:
                        mapA[i + check_i][j + check_j] = bulID
                        self.__check(origin_i, origin_j, i + check_i, j + check_j, map, mapA, lonC, latC, bulID)
                    else:
                        continue
                else:
                    continue

# -------------------------PARSER----------------------------------#
    def parse(self, filename):
        minLat = self.__borders[0]
        minLon = self.__borders[1]
        maxLat = self.__borders[2]
        maxLon = self.__borders[3]

        self.__pointer[1] = minLon
        self.__pointer[0] = minLat

        driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")

        latStep = self.__step / 111000  # [degrees]
        lonStep = self.__step / (111300 * math.cos(math.radians(self.__pointer[0])))  # [degrees]

        while self.__pointer[1] <= maxLon and self.__pointer[0] <= maxLat:
            url = 'https://2gis.ru/novosibirsk/geo/' + str(self.__pointer[1]) + '%2C' + str(self.__pointer[0]) + "?m=" + str(
                self.__pointer[1]) + '%2C' + str(self.__pointer[0]) + "%2F16"
            try:
                driver.get(url)
                time.sleep(1)
                element = driver.find_element_by_xpath(
                    "/html/body/div/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[2]")

                height = re.findall("\d{1,2} этаж\w*", element.text)
            except:
                try:
                    driver.close()
                except:
                    pass
                driver = webdriver.Firefox(executable_path="/opt/WebDriver/bin/geckodriver")
                continue

            if height:
                if len(height) == 1:
                    height = height.pop(0)
                else:
                    height = height.pop(len(height) - 1)

                test = str(height).find("'")
                text = str(height)[test + 1:test + 3]
            else:
                text = "0"

            self.__writeIntoFile(filename, self.__pointer[0], self.__pointer[1], text)

            self.__pointer[1] += lonStep
            if self.__pointer[1] > maxLon:
                self.__pointer[1] = minLon
                self.__pointer[0] += latStep
                lonStep = self.__step / (111300 * math.cos(math.radians(self.__pointer[0])))

        driver.close()

    def __writeIntoFile(self, filename, lon, lat, data):
        f = open(filename, 'a')
        f.write(str(lon) + ' ' + str(lat) + ' ' + str(data) + '\n')

    def __del__(self):
        pass

def main():
    parser = Parser()

    parser.setBorders([55.00916009009005, 82.933401, 55.018151, 82.960240])

    parser.parse('Novosibirsk_storeys_HD.txt')

if __name__ == '__main__':
    main()