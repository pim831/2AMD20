import sys
from string import ascii_uppercase

import requests
import pandas as pd
from tqdm import tqdm
import csv



def retreive_postal_info(postal_numeral, postal_alphabetical):
    cookies = {
        'ASP.NET_SessionId': 'lqtd13empghiykqr0y5d0myd',
        'mijnenexis#lang': 'nl-NL',
        'SC_ANALYTICS_GLOBAL_COOKIE': '2f424b4427af42f289bf9250d350b19d|True',
        'CookieConsent': '{stamp:%27cDoFS0VrBXqmU9pdAenqbZcgpEeEvqs8o76uCpCq0KTuLUak0laKBg==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cver:3%2Cutc:1653033768043%2Cregion:%27nl%27}',
        '_hjMinimizedPolls': '463146',
        '_gcl_au': '1.1.522557800.1653033868',
        '_gid': 'GA1.2.1480369833.1653033868',
        '_fbp': 'fb.1.1653033867991.260846467',
        '_clck': 'qvf2fw|1|f1m|0',
        '_hjFirstSeen': '1',
        '_hjSession_780186': 'eyJpZCI6IjQxYzBlZjYyLTI4ZjYtNGM1Zi05NjMxLTNiNWQ0YWFmNDNiMyIsImNyZWF0ZWQiOjE2NTMwMzM4NjgxNDcsImluU2FtcGxlIjp0cnVlfQ==',
        '_hjIncludedInSessionSample': '1',
        '_hjIncludedInPageviewSample': '1',
        '_hjAbsoluteSessionInProgress': '0',
        '_hjSessionUser_780186': 'eyJpZCI6IjdiODFiMDg1LWEzNzktNTYzZS1iZjJjLWZkOGFhNWJmN2RkZiIsImNyZWF0ZWQiOjE2NTMwMzM4Njc5NDQsImV4aXN0aW5nIjp0cnVlfQ==',
        '_hjSessionRejected': '1',
        '_ga_PR52LQXDN2': 'GS1.1.1653034034.1.1.1653034272.0',
        '_ga': 'GA1.2.1414192433.1653033868',
        '_clsk': '72wq7t|1653035300012|14|1|www.clarity.ms/eus-f/collect',
    }

    headers = {
        'authority': 'www.enexis.nl',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'nl-NL,nl;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'ASP.NET_SessionId=lqtd13empghiykqr0y5d0myd; mijnenexis#lang=nl-NL; SC_ANALYTICS_GLOBAL_COOKIE=2f424b4427af42f289bf9250d350b19d|True; CookieConsent={stamp:%27cDoFS0VrBXqmU9pdAenqbZcgpEeEvqs8o76uCpCq0KTuLUak0laKBg==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cver:3%2Cutc:1653033768043%2Cregion:%27nl%27}; _hjMinimizedPolls=463146; _gcl_au=1.1.522557800.1653033868; _gid=GA1.2.1480369833.1653033868; _fbp=fb.1.1653033867991.260846467; _clck=qvf2fw|1|f1m|0; _hjFirstSeen=1; _hjSession_780186=eyJpZCI6IjQxYzBlZjYyLTI4ZjYtNGM1Zi05NjMxLTNiNWQ0YWFmNDNiMyIsImNyZWF0ZWQiOjE2NTMwMzM4NjgxNDcsImluU2FtcGxlIjp0cnVlfQ==; _hjIncludedInSessionSample=1; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; _hjSessionUser_780186=eyJpZCI6IjdiODFiMDg1LWEzNzktNTYzZS1iZjJjLWZkOGFhNWJmN2RkZiIsImNyZWF0ZWQiOjE2NTMwMzM4Njc5NDQsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionRejected=1; _ga_PR52LQXDN2=GS1.1.1653034034.1.1.1653034272.0; _ga=GA1.2.1414192433.1653033868; _clsk=72wq7t|1653035300012|14|1|www.clarity.ms/eus-f/collect',
        'referer': 'https://www.enexis.nl/zakelijk/aansluitingen/elektriciteit-terugleveren/beperkte-capaciteit-op-het-elektriciteitsnet?postalcode='+ postal_numeral +'+'+ postal_alphabetical,
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    params = {
        'placeholderName': 'jss-main',
        'item': 'e0d89a65-2fbf-4997-9651-1f829f00eaa3',
        'sc_lang': 'nl-NL',
        'sc_apikey': '{F3F21460-1BBF-4835-BE58-2D7CF98D0D62}',
        'isHybridPlaceholder': 'true',
        'hasHybridSsr': 'false',
        'hybridLocation': '/zakelijk/aansluitingen/elektriciteit-terugleveren/beperkte-capaciteit-op-het-elektriciteitsnet?postalcode='+ postal_numeral +'+'+ postal_alphabetical,
    }

    response = requests.get('https://www.enexis.nl/sitecore/api/layout/placeholder/jss', params=params, cookies=cookies, headers=headers)
    info = response.text

    if "Dit gebied kleurt " not in info:
        return [(postal_numeral + postal_alphabetical), "No Info", "No Info"]
    color_split = info.split('Dit gebied kleurt ')[1]
    color = color_split.split(' ')[0]
    
    station_split = info.split('Dit gebied word voorzien vanuit het station","description":"')[1]
    station = station_split.split('"')[0]
    return [(postal_numeral + postal_alphabetical), color, station]

from string import ascii_uppercase

codes = [1394,1396,2165,3925,4213,7439,9479,9564,9749]

with open('postal_codes.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        for i in range(int(row[0]), int(row[1])):
            codes.append(i)


results = pd.DataFrame(columns= ['Postal_Code', "Color", "Station"])
iteration = 0
for j in tqdm(codes):
    # postal_num = '{:d}'.format(i).zfill(4)
    results.loc[len(results.index)] = retreive_postal_info(str(j), "AA")
    iteration += 1
    if (iteration % 1000) == 999:
        results.to_csv("Enexis_net" + str(iteration) + ".csv")




results.to_csv("Enexis_net.csv")
# print(response.text)
