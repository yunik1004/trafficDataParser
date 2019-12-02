import os
import sqlite3
import sys
import xml.etree.ElementTree as ET
import requests
import yaml


if __name__ == "__main__":
    currentDir = os.path.dirname(os.path.abspath(__file__))
    datasetPath = os.path.join(currentDir, "Dataset")
    if not os.path.exists(datasetPath):
        os.makedirs(datasetPath)
    #endif
    settingsPath = os.path.join(currentDir, "config", "settings.yaml")
    resultDBPath = os.path.join(datasetPath, "traffic.db")

    with open(settingsPath) as f:
        conf = yaml.safe_load(f)
    #endwith
    authkey = conf['authKey']

    # Query openapi road network traffic data
    apiURL = f"http://openapi.its.go.kr/api/NTrafficInfo?&zoom=16&key={authkey}"

    try:
        response = requests.get(apiURL)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    else:
        root = ET.fromstring(response.text)
    #endtry

    conn = sqlite3.connect(resultDBPath)
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS traffic (id INT, name STRING, source INT, target INT, avgspeed INT, traveltime INT, generatedate INT, PRIMARY KEY (id, generatedate))")

        query = "INSERT INTO traffic VALUES (?, ?, ?, ?, ?, ?, ?)"

        for data in root.findall('data'):
            try:
                roadid = int(data.find('roadsectionid').text)
                startnodeid = int(data.find('startnodeid').text)
                endnodeid = int(data.find('endnodeid').text)
                name = data.find('roadnametext').text
                avgspeed = int(data.find('avgspeed').text)
                traveltime = int(data.find('traveltime').text)
                gendate = data.find('generatedate').text
                cur.execute(query, (roadid, startnodeid, endnodeid, name, avgspeed, traveltime, gendate))
            except TypeError:
                pass
            except sqlite3.Error: # Do not insert same data
                pass
            #endtry
        #endfor
    #endwith
#endif
