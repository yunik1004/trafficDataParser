import os
import xml.etree.ElementTree as ET
import networkx as nx
import pandas as pd
import requests
import yaml


if __name__ == "__main__":
    currentDir = os.path.dirname(os.path.abspath(__file__))
    datasetPath = os.path.join(currentDir, "Dataset")
    if not os.path.exists(datasetPath):
        os.makedirs(datasetPath)
    #endif
    settingsPath = os.path.join(currentDir, "config", "settings.yaml")
    resultPath = os.path.join(datasetPath, "nodeLink.csv")

    with open(settingsPath) as f:
        conf = yaml.safe_load(f)
    #endwith
    authkey = conf['authKey']

    # Query openapi road network traffic data
    apiURL = "http://openapi.its.go.kr/api/NTrafficInfo?&zoom=16&key=" + str(authkey)
    response = requests.get(apiURL)

    xmlData = response.text
    root = ET.fromstring(xmlData)

    sources = []
    targets = []
    names = []
    avgspeeds = []
    traveltimes = []
    dates = []

    for data in root.findall('data'):
        try:
            startnodeid = int(data.find('startnodeid').text)
            endnodeid = int(data.find('endnodeid').text)
            name = data.find('roadnametext').text
            avgspeed = int(data.find('avgspeed').text)
            traveltime = int(data.find('traveltime').text)
            gendate = data.find('generatedate').text
        except TypeError:
            pass
        else:
            sources.append(startnodeid)
            targets.append(endnodeid)
            names.append(name)
            avgspeeds.append(avgspeed)
            traveltimes.append(traveltime)
            dates.append(gendate)
        #endtry
    #endfor

    df_link = pd.DataFrame({'source': sources, 'target': targets, 'name': names, 'avgspeed': avgspeeds, 'traveltime': traveltimes, 'generatedate': dates})
    df_link.to_csv(resultPath, encoding="cp949", index=False)
#endif
