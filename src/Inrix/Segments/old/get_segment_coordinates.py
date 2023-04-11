#Inrix segment call!
#made to be used to get segments
#can maybe extend functionality

import requests

def get_coordinates(seg_id):
    url = 'https://analytics-segments-api.qa.inrix.com/v3/publicsegments/details/2201/XD/' + str(seg_id)
   # url = 'https://analytics-segments-api.qa.inrix.com/v3/publicsegments/details/2201/XD/448849642'
    headers = {'Authorization': 'a3poajUyeXF6MHwyQ3l3V0pXNmpoNGhZWUpMdDRnOHI5MmxxNHlTbko2UDh4TldIcmtq'}
    #eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBSb2xlIjozLCJhcHBJZCI6ImFjMTg1YjA5LTJlMzMtNDRiMS1iMjNhLTVjNWM3ZGMyNDRlZSIsImV4cGlyeSI6IjIwMjItMDktMDlUMjI6NTA6NTMuOTI2ODA2MVoiLCJleHAiOjE2NjI3NjM4NTMsInJvbGUiOiJzZXJ2aWNlIiwiZGV2ZWxvcGVySWQiOiJhMjg2N2NmNC0xZDZkLTQ3NWMtYjNiOS0xOTA4NWE0Y2Y1NjYifQ.sPfthKMANJyi1SVY9T_QjdRVCxRWtSFU9a-A09WclQ8'}
    try:
        response = requests.get(url, headers=headers).json()
    except:
        response = None
        print(seg_id)
    return response

def midpoint(x1, y1, x2, y2):
    x = (x1 + x2)/2
    y = (y1 + y2)/2
    return float("{:.5f}".format(x)), float("{:.5f}".format(y))

def get_midpoint(response):
    y1 = response['startLatitude']
    x1 = response['startLongitude']
    y2 = response['endLatitude']
    x2 = response['endLongitude']
    return midpoint(x1,y1,x2,y2)

def get_envelopeString(response):
    return response['envelopeString']

if __name__ == '__main__':
    y = {}

    segment = 441531093
    x = get_coordinates(segment)
    
    print(x)
    # print(y[segment]['envelopeString'])
    # print(get_midpoint(x))
