# Functions
import math
import json
import ast
from shapely.geometry import Point
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import geopandas as gpd
import networkx as nx
import numpy as np

def DutchRDtoWGS84(rdX, rdY):
    """ Convert DutchRD to WGS84
    """
    RD_MINIMUM_X = 11000
    RD_MAXIMUM_X = 280000
    RD_MINIMUM_Y = 300000
    RD_MAXIMUM_Y = 630000
    if (rdX < RD_MINIMUM_X or rdX > RD_MAXIMUM_X
        or rdY < RD_MINIMUM_Y or rdY > RD_MAXIMUM_Y):
        resultNorth = -1
        resultEast = -1
        return resultNorth, resultEast
    # else
    dX = (rdX - 155000.0) / 100000.0
    dY = (rdY - 463000.0) / 100000.0
    k = [[3600 * 52.15517440, 3235.65389, -0.24750, -0.06550, 0.0],
        [-0.00738   ,   -0.00012,  0.0    ,  0.0    , 0.0],
        [-32.58297   ,   -0.84978, -0.01709, -0.00039, 0.0],
        [0.0       ,    0.0    ,  0.0    ,  0.0    , 0.0],
        [0.00530   ,    0.00033,  0.0    ,  0.0    , 0.0],
        [0.0       ,    0.0    ,  0.0    ,  0.0    , 0.0]]
    l = [[3600 * 5.38720621,    0.01199,  0.00022,  0.0    , 0.0],
        [5260.52916   ,  105.94684,  2.45656,  0.05594, 0.00128],
        [-0.00022   ,    0.0    ,  0.0    ,  0.0    , 0.0],
        [-0.81885   ,   -0.05607, -0.00256,  0.0    , 0.0],
        [0.0       ,    0.0    ,  0.0    ,  0.0    , 0.0],
        [0.00026   ,    0.0    ,  0.0    ,  0.0    , 0.0]]
    resultNorth = 0
    resultEast = 0
    powX = 1

    for p in range(6):
        powY = 1
        for q in range(5):
            resultNorth = resultNorth + k[p][q] * powX * powY / 3600.0
            resultEast = resultEast + l[p][q] * powX * powY / 3600.0
            powY = powY * dY
        powX = powX * dX
    return resultNorth, resultEast

def WGS84toDutchRD(wgs84East, wgs84North):
    # translated from Peter Knoppers's code

    # wgs84East: longtitude
    # wgs84North: latitude

    # Western boundary of the Dutch RD system. */
    WGS84_WEST_LIMIT = 3.2

    # Eastern boundary of the Dutch RD system. */
    WGS84_EAST_LIMIT = 7.3

    # Northern boundary of the Dutch RD system. */
    WGS84_SOUTH_LIMIT = 50.6

    # Southern boundary of the Dutch RD system. */
    WGS84_NORTH_LIMIT = 53.7

    if (wgs84North > WGS84_NORTH_LIMIT) or \
        (wgs84North < WGS84_SOUTH_LIMIT) or \
        (wgs84East < WGS84_WEST_LIMIT) or \
        (wgs84East > WGS84_EAST_LIMIT):
        resultX = -1
        resultY = -1
    else:
        r = [[155000.00, 190094.945,   -0.008, -32.391, 0.0],
            [-0.705, -11832.228,    0.0  ,   0.608, 0.0],
            [0.0  ,   -114.221,    0.0  ,   0.148, 0.0],
            [0.0  ,     -2.340,    0.0  ,   0.0  , 0.0],
            [0.0  ,      0.0  ,    0.0  ,   0.0  , 0.0]]
        s = [[463000.00 ,      0.433, 3638.893,   0.0  ,  0.092],
            [309056.544,     -0.032, -157.984,   0.0  , -0.054],
            [73.077,      0.0  ,   -6.439,   0.0  ,  0.0],
            [59.788,      0.0  ,    0.0  ,   0.0  ,  0.0],
            [0.0  ,      0.0  ,    0.0  ,   0.0  ,  0.0]]
        resultX = 0
        resultY = 0
        powNorth = 1
        dNorth = 0.36 * (wgs84North - 52.15517440)
        dEast = 0.36 * (wgs84East - 5.38720621)

        for p in range(5):
            powEast = 1
            for q in range(5):
                resultX = resultX + r[p][q] * powEast * powNorth
                resultY = resultY + s[p][q] * powEast * powNorth
                powEast = powEast * dEast
            powNorth = powNorth * dNorth
    return resultX, resultY


def extract_and_round(values):
    # Convert and round the values to one decimal place
    rounded_values = (round(float(values[0]), 3), round(float(values[1]), 3))

    # Convert the tuple to a string representation
    return f'({rounded_values[0]}, {rounded_values[1]})'


def remove_duplicates_ordered(input_list):
    seen = set()
    output_list = []
    for item in input_list:
        if item not in seen:
            output_list.append(item)
            seen.add(item)
    return output_list

def distance_convert(distances):
    new_store = []
    for value in distances[1:]:
        new_store.append(distances[0] - value)
    new_store.append(distances[0])
    return new_store[::-1]

def road_combine(x, y, df):
    df = df[df['route_x'] != 'LEEG']
    for index, row in df.iterrows():
        # print(type(row['route_x']))
        rx = remove_duplicates_ordered(row['route_x'])
        ry = remove_duplicates_ordered(row['route_y'])
        if (x in rx) and (y in ry):
            idx = rx.index(x)
            break
    # print(f'road combo function x: {x}, y: {y}')
    result = {'last_point_x': row['last_point_x'], 'last_point_y': row['last_point_y'],
                'counter': row['count'], 'combine': row['combine'],'route_x': rx[(idx):],
              'route_y': ry[(idx):], 'dis_dec': row['dis_dec'][idx:]}
    if len(rx[(idx):]) != len(ry[(idx):]):
        print(f"\033[91m error!!!!!!!!!!!!\033[0m")
        rx = row['route_x'][idx:]
        ry = row['route_y'][idx:]
        result = {'last_point_x': rx[-1], 'last_point_y': ry[-1],
                  'counter': row['count'], 'combine': row['combine'], 'route_x': rx,
                  'route_y': ry, 'dis_dec': row['dis_dec'][idx:]}


    return result


def flatten_list(nested_list):
    flattened = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(item)
        else:
            flattened.append(item)
    return flattened

def calculate_distance(x_start, y_start, x_end, y_end):
    distance = math.sqrt((x_end - x_start)**2 + (y_end - y_start)**2)
    return round(distance)

def error_solver(index):
    with open('error_solver.txt', "r") as file:
        loaded_dict = json.load(file)
        new = loaded_dict[str(index)]
    return(new)

def parse_coordinate(coordinate_string):
    # Remove parentheses and split the string by comma
    cleaned_string = coordinate_string.strip('()')
    x_str, y_str = cleaned_string.split(',')

    # Convert the string values to floats
    x = float(x_str.strip())
    y = float(y_str.strip())

    return x, y


def heuristic(node, goal):
    x1, y1 = ast.literal_eval(node)
    x2, y2 = ast.literal_eval(goal)
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def find_linestrings(gdf, path, tolerance=10):
    matching_lines = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry', crs=gdf.crs)
    cost = 0
    # Iterate through each LineString geometry in the GeoDataFrame
    for index, row in gdf.iterrows():
        line = row['geometry']

        # Iterate through each pair of consecutive nodes in the path
        for i in range(len(path) - 1):
            x1, y1 = parse_coordinate(path[i])
            x2, y2 =parse_coordinate(path[i + 1])
            point1 = Point(x1, y1)
            point2 = Point(x2, y2)
            dist1 = point1.distance(line)
            dist2 = point2.distance(line)

            # Check if the LineString segment is within tolerance of the line
            if (dist1 <= tolerance) and (dist2 <= tolerance):
                matching_lines = matching_lines._append({'geometry': line}, ignore_index=True)
                cost += row['ENDAFSTAND']
    return matching_lines, cost


def find_linestrings2(gdf, nodes, tolerance=10):
    matching_lines = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry', crs=gdf.crs)
    # Iterate through each LineString geometry in the GeoDataFrame
    for index, row in gdf.iterrows():
        line = row['geometry']

        count = 0
        for i in range(len(nodes)):
            x, y = parse_coordinate(nodes[i])
            point = Point(x, y)
            dist = point.distance(line)
            if dist <= tolerance:
                count += 1

            # Check if the LineString segment is within tolerance of the line
        if count > 1:
            matching_lines = matching_lines._append({'geometry': line}, ignore_index=True)

    return matching_lines


def find_node(gdf, x, y, Type, tolerance=10,):
    matching_lines = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry', crs=gdf.crs)

    for index, row in gdf.iterrows():
        line = row['geometry']

        point = Point(x, y)
        dist = point.distance(line)

        if (dist <= tolerance):
            nearest_point = line.interpolate(line.project(point))
            closest_vertex = min(line.coords, key=lambda coord: nearest_point.distance(Point(coord)))
            for i, coord in enumerate(line.coords):
                if closest_vertex == coord:
                    if Type == 'end':
                        new_line = LineString(line.coords[:i])
                        node = new_line.coords[0]
                    elif Type == 'start':
                        new_line = LineString(line.coords[i:])
                        node = new_line.coords[-1]
                    matching_lines = matching_lines._append({'geometry': new_line}, ignore_index=True)
                    break
            distance = new_line.length

    return matching_lines, distance, node


def plot_path(network_gdf, matching_lines_gdf, cost, network = True):
    fig, ax = plt.subplots(figsize=(8, 11))
    ax.grid(True)
    if network == True:
        network_gdf.plot(ax=ax, color='red', alpha=0.5)
    matching_lines_gdf.plot(ax=ax, color='deepskyblue', label='path', alpha=0.7)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f'Direction: {(cost / 1000):.2f} km')
    plt.show()


def nodes_within_distance(graph, start_node, max_distance):
    result = []
    counter = 0
    for index, node in enumerate(graph.nodes()):
        node_coordinates = tuple(map(float, node.strip('()').split(',')))
        direct_distance = ((node_coordinates[0] - start_node[0])**2 + (node_coordinates[1] - start_node[1])**2)**(0.5)
        if direct_distance > max_distance:
            continue

        try:

            distance = nx.shortest_path_length(graph, str(start_node), node,
                                                   weight='weight')
            # distance = nx.astar_path_length(graph, str(start_node), node,
            #                             heuristic=heuristic, weight='weight')
            if distance <= max_distance:
                result.append(node)
        except nx.NetworkXNoPath:
            counter +=1
            pass
    return result

def find_nearest_node_incidents(x, y, network_temp, tolerance=25):
    distance_total_line_store = []
    distance_to_line_store = []
    line_store = []
    RPE_store = []
    for Index, row in network_temp.iterrows():
        line = row['geometry']

        point = Point(x, y)
        dist = point.distance(line)
        if (dist <= tolerance):
            distance_total_line_store.append( row['ENDAFSTAND'])
            RPE_store.append(row['RPE_CODE'])
            distance_to_line_store.append(dist)
            line_store.append(line)
    if len(line_store) == 0:
        return {
        'Node': None,
        'Line': None,
        'RPE': None,
        'Total Distance to Line': None,
        'Distance to Incident': None
    }
    idx = distance_to_line_store.index(min(distance_to_line_store))
    nearest_node = line_store[idx].coords[-1]
    nearest_line = line_store[idx]
    nearest_RPE = RPE_store[idx]
    total_distance_to_nearest_line = distance_total_line_store[idx]
    distance_to_incident = ((nearest_node[0] - x) ** 2 + (nearest_node[1] - y) ** 2) ** 0.5

    return {
        'Node': nearest_node,
        'Line': nearest_line,
        'RPE': nearest_RPE,
        'Total Distance to Line': total_distance_to_nearest_line,
        'Distance to Incident': distance_to_incident
    }


