#These are file helper functions that are helpufl for translating structures
import json
import csv
import os



def read_dict_from_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data

def write_dict_to_json(big_dict, file_name):
    with open(file_name, 'w') as fp:
        json.dump(big_dict, fp)

def dict_to_array(dict):
    ret_arr = []
    for element in dict:
        ret_arr.append(dict[element])
    return ret_arr

def list_to_csv(csvlist, filename):
    with open(filename, 'w') as out:
        csv_out=csv.writer(out)
        #csv_out.writerow(['Segment ID'])
        for element in csvlist:
            csv_out.writerow(str(element))