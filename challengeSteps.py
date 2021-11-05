import sys
import numpy as np
import matplotlib.pyplot as plt
import utm
import ast
from shapely.ops import split
from shapely.geometry import *


def step_0(path):
    network, parcels = get_lists_from_file(path)

    utm_network = convert_to_utm(network)
    utm_parcels = convert_to_utm(parcels)

    utm_parcels = utm_parcels[1:]  # ignoring the first parcel (frame square)

    utm_parcels = np.array(utm_parcels, dtype=object)
    utm_network = np.array(utm_network, dtype=object)

    plot_data(utm_network, False, 'r')
    plot_data(utm_parcels, False, 'b')
    plt.show()

    return utm_network, utm_parcels


def step_1(network, parcels):
    plot_data(network, False, 'r')
    plot_data(parcels, False, 'b')

    for net in network:
        for i in range(len(net) - 1):
            network_edge = net[i], net[i + 1]
            network_linestring = LineString(network_edge)
            for parcel in parcels:
                closest_edge = None
                shortest_distance = sys.maxsize
                for j in range(len(parcel) - 1):
                    parcel_edge = parcel[j], parcel[j + 1]
                    parcel_linestring = LineString(parcel_edge)
                    dist = network_linestring.distance(parcel_linestring)
                    if dist <= 20 and dist < shortest_distance:
                        shortest_distance = dist
                        closest_edge = parcel_edge
                        closest_edge = np.array(closest_edge, dtype=object)
                plot_data(closest_edge, True, 'g')
    plt.show()


def step_2(parcels, threshold, margin=0):
    parcels_to_split = []
    final_result = []

    for parcel in parcels:
        polygon = Polygon(parcel)
        resize_polygon = polygon.buffer(-margin)
        parcels_to_split.append(polygon_to_parcel(resize_polygon))  # get bounding-box of the polygon

    for parcel in parcels_to_split:
        final_result.append(split_box(parcel, threshold))  # send bounding-box and get all sub boxes into list

    return final_result


def step_3(parcels, margin):
    polygons = step_2(parcels, 100, margin)
    # convert polygon object into list of coordinates (for plot)
    for polygon in polygons:
        for sub in polygon:
            coordinates_list = polygon_to_parcel(sub)
            result = np.array(coordinates_list)
            plot_data(result, True, 'lightgray')

    step_1(network_array, parcels_array)
    plt.show()


def polygon_to_parcel(polygon):
    coordinates_list = []
    x, y = polygon.exterior.coords.xy
    for i in range(len(x)):
        coordinates_list.append([x[i], y[i]])
    return coordinates_list


def get_lists_from_file(path):
    with open(path, 'r') as f:
        lines = f.read()

    # split the string into lists
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
        for item in lst:  # lst is dictionary with keys(lat, lng)
            lat = item['lat']
            lng = item['lng']
            as_utm = utm.from_latlon(lat, lng)  # convert lat-lon to utm, get (coordinate, zone, N/S/W/E)
            x = as_utm[0]
            y = as_utm[1]
            utm_inside_list.append([x, y])
        utm_list.append(utm_inside_list)

    return utm_list


def plot_data(data, is_edge, color):
    if data is None:
        return

    if is_edge:
        if len(data) > 0:
            x, y = data.T
            plt.plot(x, y, color, linewidth=1.5)
    else:
        for array in data:
            array = np.array(array, dtype=object)
            x, y = array.T
            plt.plot(x, y, color, linewidth=1.5)


def split_box(bounding_box, threshold):
    poly = Polygon([[p[0], p[1]] for p in bounding_box])
    final_result = split(poly, threshold)

    return final_result


# recursive function to split polygons
def split(geometric, threshold, count=0):
    bounds = geometric.bounds
    if not bounds:
        return [geometric]
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    if max(width, height) <= threshold or count == 250:
        # either the polygon is smaller than the threshold, or the maximum number of recursions has been reached
        return [geometric]
    if height >= width:
        # split left to right
        a = box(bounds[0], bounds[1], bounds[2], bounds[1] + height / 2)
        b = box(bounds[0], bounds[1] + height / 2, bounds[2], bounds[3])
    else:
        # split top to bottom
        a = box(bounds[0], bounds[1], bounds[0] + width / 2, bounds[3])
        b = box(bounds[0] + width / 2, bounds[1], bounds[2], bounds[3])

    result = []
    for d in (a, b,):
        c = geometric.intersection(d)
        if not isinstance(c, GeometryCollection):
            c = [c]
        for e in c:
            if isinstance(e, (Polygon, MultiPolygon)):
                result.extend(split(e, threshold, count + 1))
    if count > 0:
        return result

    # convert multipart into single part
    final_result = []
    for g in result:
        if isinstance(g, MultiPolygon):
            final_result.extend(g)
        else:
            final_result.append(g)

    return final_result


network_array, parcels_array = step_0('python-challenge.txt')
step_1(network_array, parcels_array)
step_3(parcels_array, 5)
