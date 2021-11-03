import math
import numpy as np
import matplotlib.pyplot as plt
import utm
import ast
from scipy.spatial import distance


def step_0(path):

    network, parcels = get_lists_from_file(path)

    utm_network = convert_to_utm(network)
    utm_parcels = convert_to_utm(parcels)

    utm_parcels = np.array(utm_parcels, dtype=object)
    utm_network = np.array(utm_network, dtype=object)

    plot_data(utm_network, 'r')
    plot_data(utm_parcels, 'b')
    plt.show()

    return utm_network, utm_parcels


def get_lists_from_file(path):
    with open(path, 'r') as f:
        lines = f.read()

    # split the string into lists TODO: find another way to split
    lines = lines.split('[[')
    lines[1] = '[[' + lines[1]
    lines[2] = '[[' + lines[2]
    network = lines[1][0:lines[1].index(']]') + 2]
    parcels = lines[2][0:lines[2].index(']]') + 2]

    # extract inside lists
    network = ast.literal_eval(network)
    parcels = ast.literal_eval(parcels)

    return network, parcels


def convert_to_utm(list_to_convert):
    utm_list = []

    # add coordinates as utm format to the new list
    for lst in list_to_convert:
        utm_inside_list = []
        for item in lst:
            lat = item['lat']
            lng = item['lng']
            as_utm = utm.from_latlon(lat, lng)
            x = as_utm[0]
            y = as_utm[1]
            # as_utm = pyproj.Proj(proj='utm', zone=36, ellps='WGS84')
            # x, y = as_utm(lat, lng)
            #
            utm_inside_list.append([x, y])
        utm_list.append(utm_inside_list)

    return utm_list


def plot_data(data, color):
    for array in data:
        array = np.array(array, dtype=object)
        x, y = array.T
        plt.plot(x, y, color)

network_array, parcels_array = step_0('python-challenge.txt')

