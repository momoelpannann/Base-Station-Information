import json
import sys
import random
import math
from collections import defaultdict


def load_json(filename):
    """
    This functin loads and returns data from a JSON file
    """
    with open(filename, 'r') as file:
        return json.load(file)


def display_menu():
    """
    This function displays the menu options to the user.
    """
    print("1. Display Global Statistics")
    print("2. Display Base Station Statistics")
    print("3. Check Coverage")
    print("4. Exit")


def calculate_global_statistics(data):
    """
    This function calculates the global statistics of the network coverage.
    It returns a dictionary containing various statistics.
    """
    #Total number of base stations
    total_base_stations = len(data['baseStations'])
    # Total number of antennas
    total_antennas = sum(len(bs['ants']) for bs in data['baseStations'])
    # total number of antennas per base station
    antennas_per_base_station = [len(bs['ants']) for bs in data['baseStations']]

    # max, min and average number of antennas per base station
    max_antennas = max(antennas_per_base_station)
    min_antennas = min(antennas_per_base_station)
    avg_antennas = sum(antennas_per_base_station) / total_base_stations

# Dictionary to count how many antennas cover each point
    points_covered_by_antenna = defaultdict(int)

#Finding total number of points covered in the area
    min_lat, max_lat = data['min_lat'], data['max_lat']
    min_lon, max_lon = data['min_lon'], data['max_lon']
    step = data['step']
#Finding total numebr of steps for longitude and latitude then finding total amount of points
    lat_steps = int(round((max_lat - min_lat) / step)) + 1
    lon_steps = int(round((max_lon - min_lon) / step)) + 1
    total_points = lat_steps * lon_steps
#count how many antennas cover each point
    for bs in data['baseStations']:
        for ant in bs['ants']:
            for pt in ant['pts']:
                point = (pt[0], pt[1])
                points_covered_by_antenna[point] += 1

#Finding number of points covering one antenna, more than one antenna and no antennas
    exactly_one_antenna = sum(1 for v in points_covered_by_antenna.values() if v == 1)
    more_than_one_antenna = sum(1 for v in points_covered_by_antenna.values() if v > 1)
    no_antennas = total_points - len(points_covered_by_antenna)
#Finding the maximum number of antennas covering one point and the average number of antennas covering one point
    max_antennas_one_point = max(points_covered_by_antenna.values(), default=0)
    avg_antennas_per_point = sum(points_covered_by_antenna.values()) / len(points_covered_by_antenna) if points_covered_by_antenna else 0
#Calculaitng the percentage of covered area
    percentage_covered_area = (len(points_covered_by_antenna) / total_points) * 100

#finding base station and antenna covering the maximum of points
    max_covering_bs_ant = max(
        ((bs['id'], ant['id'], len(ant['pts'])) for bs in data['baseStations'] for ant in bs['ants']),
        key=lambda x: x[2], default=(None, None, 0)
    )

#return a dictionary of all the statistics
    stats = {
        'total_base_stations': total_base_stations,
        'total_antennas': total_antennas,
        'max_ants': max_antennas,
        'min_ants': min_antennas,
        'avg_ants': avg_antennas,
        'exactly_one_antenna': exactly_one_antenna,
        'more_than_one_antenna': more_than_one_antenna,
        'no_antenna_coverage': no_antennas,
        'max_antennas_one_point': max_antennas_one_point,
        'avg_antennas_per_point': avg_antennas_per_point,
        'percentage_covered_area': percentage_covered_area,
        'max_covering_bs_ant': max_covering_bs_ant
    }

    return stats

def display_global_statistics(stats):
    """
        This function displays the statistics for a specific base station.
    """
    print(f"Total number of base stations = {stats['total_base_stations']}")
    print(f"Total number of antennas = {stats['total_antennas']}")
    print(f"Max, min, and average of antennas per base station = {stats['max_ants']}, {stats['min_ants']}, {stats['avg_ants']:.2f}")
    print(f"Total number of points covered by exactly one antenna = {stats['exactly_one_antenna']}")
    print(f"Total number of points covered by more than one antenna = {stats['more_than_one_antenna']}")
    print(f"Total number of points not covered by any antenna = {stats['no_antenna_coverage']}")
    print(f"Maximum number of antennas that cover one point = {stats['max_antennas_one_point']}")
    print(f"Average number of antennas covering a point = {stats['avg_antennas_per_point']:.2f}")
    print(f"Percentage of the covered area = {stats['percentage_covered_area']:.2f}%")
    print(f"ID of the base station and antenna covering the maximum number of points = {stats['max_covering_bs_ant'][0]}, {stats['max_covering_bs_ant'][1]}")



def calculate_base_station_statistics(data, base_station_id=None):
    """
        This function calculates the statistics for a specific base station.
        It returns a dictionary containing the calculated statistics.
        It calculates everything in the same manner as the global statistics function
    """
   #finding ID of base station, if none found then pick a random one
    if base_station_id is None:
        base_station = random.choice(data['baseStations'])
    else:
        base_station = next((bs for bs in data['baseStations'] if bs['id'] == base_station_id), None)
        if base_station is None:
            return None

    total_antennas = len(base_station['ants'])
    points_covered_by_antenna = defaultdict(int)

    min_lat, max_lat = data['min_lat'], data['max_lat']
    min_lon, max_lon = data['min_lon'], data['max_lon']
    step = data['step']
    lat_steps = int(round((max_lat - min_lat) / step)) + 1
    lon_steps = int(round((max_lon - min_lon) / step)) + 1
    total_points = lat_steps * lon_steps

    for ant in base_station['ants']:
        for pt in ant['pts']:
            point = (pt[0], pt[1])
            points_covered_by_antenna[point] += 1

    exactly_one_antenna = sum(1 for v in points_covered_by_antenna.values() if v == 1)
    more_than_one_antenna = sum(1 for v in points_covered_by_antenna.values() if v > 1)
    no_antenna_coverage = total_points - len(points_covered_by_antenna)
    max_antennas_one_point = max(points_covered_by_antenna.values(), default=0)
    avg_antennas_per_point = sum(points_covered_by_antenna.values()) / len(points_covered_by_antenna) if points_covered_by_antenna else 0
    percentage_covered_area = (len(points_covered_by_antenna) / total_points) * 100

    max_covering_ant = max(((ant['id'], len(ant['pts'])) for ant in base_station['ants']), key=lambda x: x[1], default=(None, 0))

    stats = {
        'total_antennas': total_antennas,
        'exactly_one_antenna': exactly_one_antenna,
        'more_than_one_antenna': more_than_one_antenna,
        'no_antenna_coverage': no_antenna_coverage,
        'max_antennas_one_point': max_antennas_one_point,
        'avg_antennas_per_point': avg_antennas_per_point,
        'percentage_covered_area': percentage_covered_area,
        'max_covering_ant': max_covering_ant
    }

    return stats

def display_base_station_statistics(stats):
    """
    This function displays the statistics about the specific base station
    """
    print(f"Total number of antennas = {stats['total_antennas']}")
    print(f"Total number of points covered by exactly one antenna = {stats['exactly_one_antenna']}")
    print(f"Total number of points covered by more than one antenna = {stats['more_than_one_antenna']}")
    print(f"Total number of points not covered by any antenna = {stats['no_antenna_coverage']}")
    print(f"Maximum number of antennas that cover one point = {stats['max_antennas_one_point']}")
    print(f"Average number of antennas covering a point = {stats['avg_antennas_per_point']:.2f}")
    print(f"Percentage of the covered area = {stats['percentage_covered_area']:.2f}%")
    print(f"ID of the antenna covering the maximum number of points = {stats['max_covering_ant'][0]}")



def check_coverage(data, lat, lon):
    """
       This function checks and displays coverage information for a given coordinate.
       It returns the nearest base station and antenna if the point is not covered.
     """
    covered = False # Flag to check if point is covered
    antennas_covering_point = [] #list to store antennas

#cehcking if point is covered by any antenna
    for bs in data['baseStations']:
        for ant in bs['ants']:
            for pt in ant['pts']:
                if pt[0] == lat and pt[1] == lon:
                    antennas_covering_point.append((bs['id'], ant['id'], pt[2]))
                    covered = True

    if not covered:
        nearest_distance = float('inf') #initiiaze to infinity
        nearest_bs_ant = None

        #calculating nearest antenna to given point
        for bs in data['baseStations']:
            for ant in bs['ants']:
                for pt in ant['pts']:
                    distance = math.sqrt((pt[0] - lat) ** 2 + (pt[1] - lon) ** 2)
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_bs_ant = (bs['id'], ant['id'], pt[0], pt[1])
                        if nearest_bs_ant:
                            return nearest_bs_ant, antennas_covering_point

                    return None, antennas_covering_point


def main():
    """
    The main function that runs the program.
    It handles user inputs and displays the appropriate statistics or coverage information.
    """
    # Check if the correct number of command line arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python3 <your_code.py> <test_file.json>")
        return

    # Load the JSON file specified by the command line argument
    filename = sys.argv[1]
    data = load_json(filename)

    while True:
        # Display the menu options to the user
        display_menu()

        # Get the user's choice from the menu
        choice = input("Enter your choice: ")

        if choice == '1':
            # If the user selects option 1, calculate and display global statistics
            stats = calculate_global_statistics(data)
            display_global_statistics(stats)
        elif choice == '2':
            # If the user selects option 2, provide sub-options for base station statistics
            sub_choice = input("Enter sub-option (2.1 for random station, 2.2 to choose by ID): ")
            if sub_choice == '2.1':
                # If the user selects sub-option 2.1, calculate and display statistics for a random base station
                stats = calculate_base_station_statistics(data)
                if stats:
                    display_base_station_statistics(stats)
                else:
                    print("No base stations found.")
            elif sub_choice == '2.2':
                # If the user selects sub-option 2.2, prompt for a specific base station ID and display its statistics
                base_station_id = int(input("Enter base station ID: "))
                stats = calculate_base_station_statistics(data, base_station_id)
                if stats:
                    display_base_station_statistics(stats)
                else:
                    print("Base station not found.")
            else:
                # Handle invalid sub-options
                print("Invalid sub-option.")
        elif choice == '3':
            # If the user selects option 3, prompt for coordinates and check coverage
            lat = float(input("Enter latitude: "))
            lon = float(input("Enter longitude: "))
            nearest_bs_ant, antennas_covering_point = check_coverage(data, lat, lon)
            if antennas_covering_point:
                # If the point is covered, display the antennas covering the point
                print(f"Antennas covering point ({lat}, {lon}): {antennas_covering_point}")
            else:
                # If the point is not covered, display the nearest antenna
                print(f"No coverage found at point ({lat}, {lon})")
                if nearest_bs_ant:
                    print(
                        f"Nearest antenna is from base station {nearest_bs_ant[0]} with antenna ID {nearest_bs_ant[1]} at ({nearest_bs_ant[2]}, {nearest_bs_ant[3]})")
        elif choice == '4':
            # If the user selects option 4, exit the program
            break
        else:
            # Handle invalid menu choices
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()