import pandas as pd
from shapely.geometry import Point, Polygon

#csv_out.writerow(['jdate','jseg_id', 'daily_speed', 'historical_speed', 'ref_speed', 'midpoint', 'envelope'])


def get_dict(csv_file):
    df = pd.read_csv(csv_file)
    envelope = df['envelope']
    midpoint = df['midpoint']

    return envelope

def is_it_inside(coordinates, polygon):
    point = Point(coordinates)
    polygon = Polygon(polygon)
    return polygon.contains(point)

def get_area(polygon):
    polygon = Polygon(polygon)
    return polygon.area



if __name__ == "__main__":
    # print(read_csv("joshsep8713 copy.csv"))
    poly = [
        [
            -118.14556798084655,
            48.87413928222519
        ],
        [
            -118.10832611082749,
            48.57407027078483
        ],
        [
            -117.87563420208026,
            48.73149018672055
        ],
        [
            -118.03432142080301,
            48.94708930243874
        ],
        [
            -118.14556798084655,
            48.87413928222519
        ]
    ]
    coordinate = [-123,60]
    print(is_it_inside(coordinate,poly))