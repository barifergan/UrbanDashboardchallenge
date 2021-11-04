import math
import sys

import numpy as np
import matplotlib.pyplot as plt
import utm
import ast


def step_0(path):
    network, parcels = get_lists_from_file(path)

    utm_network = convert_to_utm(network)
    utm_parcels = convert_to_utm(parcels)

    utm_parcels = np.array(utm_parcels, dtype=object)
    utm_network = np.array(utm_network, dtype=object)

    plot_data(utm_network, False, 'r')
    plot_data(utm_parcels, False, 'b')
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
            utm_inside_list.append([x, y])
        utm_list.append(utm_inside_list)

    return utm_list


def plot_data(data, is_edge, color):
    if data is None:
        return
    if is_edge:
        x, y = data.T
        plt.plot(x, y, color)
    else:
        for array in data:
            array = np.array(array, dtype=object)
            x, y = array.T
            plt.plot(x, y, color)


def step_1(network, parcels):
    # TODO: fix distance between 2 edges!!

    plot_data(network, False, 'r')
    plot_data(parcels, False, 'b')
    # for parcel in parcels:
    #     for i in range(0, len(parcel) - 1):
    #         parcel_edge = parcel[i], parcel[i + 1]
    #         for net in network:
    #             shortest_distance = sys.maxsize
    #             closest_edge = None
    #             for j in range(0, len(net) - 1):
    #                 network_edge = net[j], net[j + 1]
    #                 dist = get_two_lines_distance(parcel_edge, network_edge)
    #                 if dist <= 20:
    #                     if dist < shortest_distance:
    #                         shortest_distance = dist
    #                         closest_edge = parcel_edge
    #                         closest_edge = np.array(closest_edge, dtype=object)
    #             plot_data(closest_edge, True, 'g')

    for net in network:
        for i in range(0, len(net) - 1):
            network_edge = net[i], net[i + 1]
            for parcel in parcels:
                closest_edge = None
                shortest_distance = sys.maxsize
                for j in range(0, len(parcel) - 1):
                    parcel_edge = parcel[j], parcel[j + 1]
                    dist = get_two_lines_distance(parcel_edge, network_edge)
                    if dist <= 20 and dist < shortest_distance:
                        shortest_distance = dist
                        closest_edge = parcel_edge
                        closest_edge = np.array(closest_edge, dtype=object)
                plot_data(closest_edge, True, 'g')

    plt.show()


def get_two_lines_distance(edge1, edge2):

    distances = []

    # edge1 endpoints
    p1 = edge1[0]
    p2 = edge1[1]

    # edge 2 endpoints
    p3 = edge2[0]
    p4 = edge2[1]

    # midpoints
    midpoint1 = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2
    midpoint2 = (p3[0] + p4[0])/2, (p3[1] + p4[1])/2

    edge1_points = [p1, midpoint1, p2]
    edge2_points = [p3, midpoint2, p4]

    for e1_p in edge1_points:
        for e2_p in edge2_points:
            dist = euclidean_distance(e1_p[0], e2_p[0], e1_p[1], e2_p[1])
            distances.append(dist)

    shortest_dist = min(distances)
    return shortest_dist


def euclidean_distance(x1, x2, y1, y2):
    pow_x = math.pow((x1 - x2), 2)
    pow_y = math.pow((y1 - y2), 2)
    dist = math.sqrt(pow_x + pow_y)
    return dist


def get_edge_length(edge):
    p1 = edge[0]
    p2 = edge[1]

    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]

    pow_x = math.pow((x1 - x2), 2)
    pow_y = math.pow((y1 - y2), 2)
    dist = math.sqrt(pow_x + pow_y)
    return dist


def step_2():
    pass


network_array, parcels_array = step_0('python-challenge.txt')
step_1(network_array, parcels_array)
