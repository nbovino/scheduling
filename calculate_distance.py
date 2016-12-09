from datetime import datetime
import googlemaps
import distance_matrix
import json

api_key = "AIzaSyC7ttZ4dsn3mxtSQCpiY5PXSPZR_8C-d-c"


def get_address(question_num):
    return input("Put in address " + str(question_num) + " : ")


def get_distance(ad_one, ad_two):
    gmaps = googlemaps.Client(key=api_key)
    return distance_matrix.distance_matrix(gmaps, ad_one, ad_two, units='imperial')


def set_json_file(data):
    with open('responses.json') as data_file:
        json.dump(data, data_file)


def get_json_file():
    with open('responses.json') as data_file:
        return json.load(data_file)


def main():
    # addresses = []
    # num = 1
    # while num < 3:
    #     addresses.append(get_address(num))
    #     num += 1
    # Pre-populated trial data
    data = get_distance('923 Lemon st. Johnstown, PA 15902', '125 Donahoe Rd. Greensburg, PA')
    # data = get_distance(addresses[0], addresses[1])
    print(data["rows"][0]["elements"][0]["duration"]["value"])


if __name__ == "__main__":
    main()
