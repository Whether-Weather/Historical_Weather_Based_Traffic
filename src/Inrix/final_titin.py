import test_if_tower_is_in as titin
import json
import pandas as pd


def get_geojson():
    all_data = titin.get_dict_from_json('src/output_data/oct11_all_data.json')
    seg_geometries = titin.get_dict_from_json('src/data/inrix/big_run/sep28_all_segments_dict.json')

    big_dict = {'type': 'FeatureCollection'}
    features_array = []
    count = 0
    z = 0
    for element in all_data:
        properties_dict = {}
        features_dict = {'type': 'Feature'}
        try:
            speed = str(all_data[element]['speed'])
            if "nan" in speed or "NaN" in speed or "Nan" in speed:
                z += 1
                properties_dict['speed'] = -1
            else:
                properties_dict['speed'] = all_data[element]['speed']
        except:
            properties_dict['speed'] = -2
        try:
            properties_dict['speed_ref'] = all_data[element]['speed_ref']
            properties_dict['rain'] = all_data[element]['rain']
            properties_dict['closest_weather_station'] = all_data[element]['closest_weather_station']
        except:
            properties_dict['speed_ref'] = -2
            properties_dict['rain'] = -2
            properties_dict['closest_weather_station'] = -2
        properties_dict['seg_id'] = element.split(",")[0]
        
        features_dict['geometry'] = json.loads(seg_geometries[properties_dict['seg_id']]['envelopeString'])
        features_dict['properties'] = properties_dict
        features_array.append(features_dict)
        count += 1

    big_dict['features'] = features_array
    print(z)
    #string to json?
    with open('src/output_data/oct3/oct11_big_result.json', 'w') as fp:
        json.dump(big_dict, fp)

#10635 in other?
#10220 "NaN"'s all in speed
def clean_json_file():
    obj = titin.get_dict_from_json('src/output_data/oct3/oct11_big_result.json')
    features_array = obj['features']
    
    count = 0
    for i in range(0, len(features_array)):
        x = json.dumps(features_array[i])
        speed = json.dumps(features_array[i]['properties']['speed'])
        if "nan" in speed or "NaN" in speed or "Nan" in speed:
            features_array[i]['properties']['speed'] = -1
            count += 1

    obj['features'] = features_array

    c = 0
    features_array = obj['features']
    for i in range(0, len(features_array)):
        x = json.dumps(features_array[i])
        if "nan" in x or "NaN" in x or "Nan" in x:
            print(i)
        elif '-1' in x:
            c += 1

   
    with open('src/output_data/oct3/oct3_big_result_no_NAN.json', 'w') as fp:
        json.dump(obj, fp)


    print(str(count))




def validate_json():
    obj = titin.get_dict_from_json('src/output_data/oct3/oct3_big_result_no_NAN.json')
    features_array = obj['features']
    new_array = []
    for i in range(0, 1000000):
        new_array.append(features_array[i])

    obj['features'] = new_array
    with open('heatmap/oct3_test.json', 'w') as fp:
        json.dump(obj, fp)

#461366789,2020-11-03


if __name__ == "__main__":
    clean_json_file()
    #print(len(titin.get_dict_from_json('src/output_data/oct3/oct3_test.json')['features']))


    # x = titin.get_dict_from_json('src/output_data/oct3/oct3_big_result.json')
    # xstr = json.dumps(x)
    # if "undefined" in xstr:
    #     xstr = xstr.replace("undefined" , 0)
    # a = json.loads(xstr)
    # with open('src/output_data/oct3/oct3_big_result_undef.json', 'w') as fp:
    #     json.dump(a, fp)

    # y = titin.get_dict_from_json('src/output_data/oct3/oct3inv_big_result_2.json')
    # z = titin.get_dict_from_json('src/output_data/big_result copy.json')
    # print("hello")