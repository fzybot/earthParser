import copy
import ctypes.wintypes
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

#i, j ,k - numbers of column  in the file
def read_from_file(fileName,i,j,k):
    f = open(fileName,'r')
    if f:
        data = f.readlines()

    x = []
    y = []
    z = []
    for line in range(0,len(data)):
        x.append(data[line].split()[i])
        y.append(data[line].split()[j])
        z.append(data[line].split()[k])

    return (x,y,z)

#*args - lists
def write_in_file(fileName,*args):
    f = open(fileName,'w')
    length = len(args[0])
    for i in range(length):
        line = ''
        for n in args:
            line+=str(n[i])+' '
        line+='\n'
        f.write(line)
    f.close()

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
        file.close()

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

#filename, x - x axis, y - y axis, z - z axis, x_name - x axis display name, y_name - y axis display name, z_name - z axis display name, z_lim - limiting the values of the z axis
def plot(filename,x,y,z, x_name, y_name, z_name, z_lim):
    list_x,list_y,list_z = read_from_file(filename,x,y,z)

    new_x = sorted(list_x)

    y_len = 0
    while new_x[0] == new_x[y_len]:
        y_len += 1

    x_len = int(len(list_x) / y_len)

    Z = np.zeros((x_len,y_len))
    for i in range(x_len):
        for j in range(y_len):
            Z[i][j]=list_z[i*y_len+j]

    X = np.arange(0, y_len, 1)
    Y = np.arange(0, x_len, 1)
    X, Y = np.meshgrid(X, Y)

    fig = plt.figure()
    ax = Axes3D(fig,auto_add_to_figure=False, box_aspect=(1,1*(x_len/y_len),0.1))

    fig.add_axes(ax)

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.viridis, antialiased=True)
    ax.set(xlim=[0,y_len],ylim=[0,x_len], zlim = [0,z_lim])

    ax.set_xlabel(x_name,labelpad=20)
    ax.set_ylabel(y_name)
    ax.set_zlabel(z_name)

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

def get_buildings_boundaries(lat,lon,storey):
    latC = 0
    while lat[0] == lat[latC]:
        latC += 1

    lonC = int(len(lon) / latC)

    map = [[0 for j in range(latC)] for i in range(lonC)]

    Z = np.zeros((lonC,latC))

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

    buildings = [0 for i in range(len(lat))]

    for i in range(lonC):
        for j in range(latC):
            buildings[i * latC + j] = int(Z[i][j])

    return(buildings)

    #to_json(lat,latC,lon,lonC,storey,Z)

# N: 210, 211, 217, 254, 268 - some buildings' numbers

def main():
    plot('Novosibirsk_storeys_V2.txt',0,1,2,"LON","LAN","STOREY",50)

if __name__ == '__main__':
    main()