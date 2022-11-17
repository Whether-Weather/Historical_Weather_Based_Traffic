import json
import test_if_tower_is_in as titin

def arr_to_dict(obj):
    features_array = obj['features']

    dict = {}
    

    count = 0
    for i in range(0, len(features_array)):
        try:
            dict[features_array[i]['properties']['seg_id']]['rain'].append(features_array[i]['properties']['rain'])
            dict[features_array[i]['properties']['seg_id']]['speed'].append(features_array[i]['properties']['speed'])
            dict[features_array[i]['properties']['seg_id']]['speed_ref'].append(features_array[i]['properties']['speed_ref'])
        except:
            rain = []
            speed = []
            speed_ref = []
            inner_dict = {'rain': rain, 'speed': speed, 'speed_ref': speed_ref}
            inner_dict['rain'].append(features_array[i]['properties']['rain'])
            inner_dict['speed'].append(features_array[i]['properties']['speed'])
            inner_dict['speed_ref'].append(features_array[i]['properties']['speed_ref'])
            dict[features_array[i]['properties']['seg_id']] =  inner_dict


    
    return dict



def main():
    obj = titin.get_dict_from_json('src/output_data/oct3/oct11_big_result.json')
    features_array = obj['features']
    seg_dict = arr_to_dict(obj)
    i = 0
    counter = 0
    while i < len(features_array):
        counter += 1
        if seg_dict[features_array[i]['properties']['seg_id']] != None:
            features_array[i]['properties']['rain'] = seg_dict[features_array[i]['properties']['seg_id']]['rain']
            features_array[i]['properties']['speed'] = seg_dict[features_array[i]['properties']['seg_id']]['speed']
            features_array[i]['properties']['speed_ref'] = seg_dict[features_array[i]['properties']['seg_id']]['speed_ref']
            seg_dict[features_array[i]['properties']['seg_id']] = None
            i += 1
        else:
            features_array.pop(i)
    obj['features'] = features_array
    with open('heatmap/oct11_test.json', 'w') as fp:
        json.dump(obj, fp)

if __name__ == "__main__":
    main()




# for j in range(0, len(seg_dict[features_array[i]['properties']['seg_id']])):
#             speed_arr = []
#             speed_ref_arr = []
#             rain_arr = []
#             if features_array[i]['properties']['seg_id'] == features_array[j]['properties']['seg_id'] and i != j:
#                 if features_array[i]['properties']['rain'] == features_array[j]['properties']['rain']:
#                     print(features_array[i]['properties']['rain'], features_array[j]['properties']['rain'])

#                 if isinstance(features_array[i]['properties']['rain'], int) or isinstance(features_array[i]['properties']['rain'], float):
#                     speed_arr.append(features_array[i]['properties']['speed'])
#                     speed_ref_arr.append(features_array[i]['properties']['speed_ref'])
#                     rain_arr.append(features_array[i]['properties']['rain'])

#                 elif isinstance(features_array[i]['properties']['rain'], list):
#                     speed_arr.extend(features_array[i]['properties']['speed'])
#                     speed_ref_arr.extend(features_array[i]['properties']['speed_ref'])
#                     rain_arr.extend(features_array[i]['properties']['rain'])
#                 else:
#                     print("error at :" + str(i))

#                 holder = features_array.pop(j)
                
#                 speed_arr.append(holder['properties']['speed'])
#                 speed_ref_arr.append(holder['properties']['speed_ref'])
#                 rain_arr.append(holder['properties']['rain'])
                
#                 features_array[i]['properties']['rain'] = rain_arr
#                 features_array[i]['properties']['speed'] = speed_arr
#                 features_array[i]['properties']['speed_ref'] = speed_ref_arr
#             else:
#                 j = j + 1