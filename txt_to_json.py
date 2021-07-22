import copy
import ctypes.wintypes
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


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


def to_json(lat,latC,lon,lonC,storey,Z):


    data={'ID':None,'borders':{'x':latC,'y':lonC,'minlon':lon[0], 'minlat':lat[0], 'maxlon':lon[len(lon)-1], 'maxlat':lat[len(lat)-1]}}

    data.update({'ID':{str(int(Z[0][0])):{'lon':[lon[0]], 'lat':[lat[0]], 'storeys':[storey[0]], 'x':[0], 'y':[0]}}})

    for i in range(lonC):
        for j in range(latC):
            if str(int(Z[i][j])) not in data['ID'].keys():
                data['ID'][str(int(Z[i][j]))] ={'lon':[lon[i]], 'lat':[lat[j*lonC + i]], 'storeys':storey[i*latC+j], 'x':[j], 'y':[i]}
            else:
                data['ID'][str(int(Z[i][j]))]['lon'].append(lon[i])
                data['ID'][str(int(Z[i][j]))]['lat'].append(lat[j*lonC + i])
                data['ID'][str(int(Z[i][j]))]['x'].append(j)
                data['ID'][str(int(Z[i][j]))]['y'].append(i)


    with open('storeys.json','w') as file:
        json.dump(data,file, indent=1)





def check_cells(lon, lat, i, j, check_i, check_j):
    if (check_i+i) < 0:
        check_i=0
    else:
        if (check_i+i) >= lon:
            check_i = 0

    if (check_j + j) < 0:
        check_j = 0
    else:
        if (check_j + j) >= lat:
            check_j = 0


    return(check_i,check_j)

def plot():
    lat,lon,storey = read_from_file('Novosibirsk_storeys.txt')

    latC = 0
    while lat[0] == lat[latC]:
        latC += 1


    lonC = int(len(lon)/latC)

    map = [[0 for j in range(latC)] for i in range(lonC)]

    print(len(storey))

    Z = np.zeros((lonC,latC))

    for i in range(lonC):
        for j in range(latC):
            map[i][j]=storey[i*latC+j]
            Z[i][j]=storey[i*latC+j]


    X = np.arange(0, latC, 1)
    Y = np.arange(0, lonC, 1)
    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    ax = Axes3D(fig,auto_add_to_figure=False, box_aspect=(1,1*(lonC/latC),0.1))

    fig.add_axes(ax)

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.viridis, antialiased=False, edgecolor ='none',linewidth=20)
    ax.set(xlim=[0,latC],ylim=[0,lonC], zlim = [0,200])

    ax.set_xlabel("LON",labelpad=20)
    ax.set_ylabel("LAT")
    ax.set_zlabel("STOREY")

    plt.show()


def check(origin_i,origin_j, i,j,map,mapA, lonC, latC, bulID):

    for check_i in range(-1,2):
        for check_j in range(-1,2):
            check_i, check_j = check_cells(lonC,latC,i,j,check_i,check_j)
            if i==check_i and j==check_j:
                continue

            if map[origin_i][origin_j]==map[i+check_i][j+check_j]:
                if mapA[i+check_i][j+check_j]==0:
                    mapA[i+check_i][j+check_j] = bulID
                    check(origin_i,origin_j,i+check_i,j+check_j,map,mapA,lonC,latC,bulID)
                else:
                    continue
            else:
                continue



def get_buildings_boundaries():
    lat, lon, storey = read_from_file('Novosibirsk_storeys.txt')

    latC = 0
    while lat[0] == lat[latC]:
        latC += 1

    j = 0
    i = 0

    lonC = int(len(lon) / latC)

    map = [[0 for j in range(latC)] for i in range(lonC)]

    Z = np.zeros((lonC,latC))

    print(len(storey))


    for i in range(lonC):
        for j in range(latC):
            map[i][j] = int(storey[i * latC + j])


    buildingID=2


    for i in range(0,lonC,1):
        for j in range(0,latC,1):
            if map[i][j]==0:
                Z[i][j]=1

    for i in range(0,lonC,1):
        for j in range(0,latC,1):
            if Z[i][j] == 0:
                check(i,j,i,j,map,Z,lonC,latC,buildingID)
                buildingID+=1


    X = np.arange(0, latC, 1)
    Y = np.arange(0, lonC, 1)
    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    ax = Axes3D(fig,auto_add_to_figure=False, box_aspect=(1,1*(lonC/latC),0.1))

    fig.add_axes(ax)

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="hot", antialiased=False, edgecolor ='none',linewidth=20)
    ax.set(xlim=[0,latC],ylim=[0,lonC], zlim = [0,100000000000000])

    ax.set_xlabel("LON",labelpad=20)
    ax.set_ylabel("LAT")
    ax.set_zlabel("STOREY")

    plt.show()

    to_json(lat,latC,lon,lonC,storey,Z)

# N: 210, 211, 217, 254, 268


def main():

    #plot()
    get_buildings_boundaries()


if __name__ == '__main__':
    main()