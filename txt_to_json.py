import copy
import ctypes.wintypes
import json
import numpy as np

def read_from_file(fileName):
    f = open(fileName,'r')

    if f:
        data = f.readlines()


    lat = []
    lon = []
    storey = []


    for i in range(0,len(data)):
        lat.append(data[i].split()[0])
        lon.append(data[i].split()[1])
        storey.append(data[i].split()[2])

    return (lat,lon,storey)

def main():
    lat,lon,storey = read_from_file('Novosibirsk_storeys.txt')

    x=lat[0]

    latC = 0
    while lat[0] == lat[latC]:
        latC += 1

    j=0
    i=0

    lonC = int(len(lon)/latC)

    map = [[0 for j in range(latC)] for i in range(lonC)]

    print(len(storey))

    mapA = copy.deepcopy(map)
    mapB = copy.deepcopy(map)

    for i in range(lonC):
        for j in range(latC):
            map[i][j]=storey[i*latC+j]



    buildingID=1

    stop=False

    while not stop:
        stop=True
        print('a')
        for i in range(0,lonC):
            for j in range(0,latC):
                if (i==0 and j==0) or (i==0 and j==latC-1) or (i==lonC-1 and j==0) or (i==lonC-1 and j==latC-1):
                    if i == 0:
                        if j == 0:
                            if map[i][j] == map[i][j + 1]:
                                if map[i][j] == 0:
                                    mapA[i][j] = buildingID
                            if map[i][j] == map[i + 1][j]:
                                if map[i][j] == 0:
                                    mapA[i][j] = buildingID
                            if map[i][j] == map[i + 1][j + 1]:
                                if map[i][j] == 0:
                                    mapA[i][j] = buildingID
                        else:
                            if j == latC-1:
                                if map[i][j] == map[i][j - 1]:
                                    if map[i][j] == 0:
                                        mapA[i][j] = buildingID
                                if map[i][j] == map[i + 1][j - 1]:
                                    if map[i][j] == 0:
                                        mapA[i][j] = buildingID
                                if map[i][j] == map[i + 1][j]:
                                    if map[i][j] == 0:
                                        mapA[i][j] = buildingID
                    else:
                        if i == lonC-1:
                            if j == 0:
                                if map[i][j] == map[i - 1][j]:
                                    if map[i][j] == 0:
                                        mapA[i][j] = buildingID
                                if map[i][j] == map[i - 1][j + 1]:
                                    if map[i][j] == 0:
                                        mapA[i][j] = buildingID
                                if map[i][j] == map[i][j + 1]:
                                    if map[i][j] == 0:
                                        mapA[i][j] = buildingID
                            else:
                                if j == latC - 1:
                                    if map[i][j] == map[i - 1][j - 1]:
                                        if map[i][j] == 0:
                                            mapA[i][j] = buildingID
                                    if map[i][j] == map[i - 1][j]:
                                        if map[i][j] == 0:
                                            mapA[i][j] = buildingID
                                    if map[i][j] == map[i][j - 1]:
                                        if map[i][j] == 0:
                                            mapA[i][j] = buildingID
                else:
                    if map[i][j] == map[i - 1][j - 1]:
                        if map[i][j]==0:
                            mapA[i][j]=buildingID
                    if map[i][j] == map[i - 1][j]:
                        if map[i][j]==0:
                            mapA[i][j]=buildingID
                    if map[i][j] == map[i - 1][j + 1]:
                        if map[i][j]==0:
                            mapA[i][j]=buildingID
                    if map[i][j] == map[i][j - 1]:
                        if map[i][j]==0:
                            mapA[i][j]=buildingID
                    if map[i][j] == map[i][j + 1]:
                        if map[i][j]==0:
                            mapA[i][j]=buildingID
                    if map[i][j] == map[i + 1][j - 1]:
                        if map[i][j]==0:
                            mapA[i][j]=buildingID
                    if map[i][j] == map[i + 1][j]:
                        if map[i][j]==0:
                            mapA[i][j]=buildingID
                    if map[i][j] == map[i + 1][j + 1]:
                        if map[i][j]==0:
                            mapA[i][j]=buildingID

        for i in range(0,lonC):
            for j in range(0,latC):
                if mapA[i][j]==0:
                    stop=True
        buildingID+=1

    for i in range(lonC):
        print(mapA[i])

    print("-----")
    for i in range(lonC):
        print(map[i])

if __name__ == '__main__':
    main()