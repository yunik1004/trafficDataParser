from datetime import datetime
import os
import sqlite3
import sys
import time
import xml.etree.ElementTree as ET
import requests
from utils import DatasetPath, getSettings


class Traffic:
    def __init__ (self, conn, apiURL):
        self.__conn = conn
        self.__apiURL = apiURL
        self.__graph_query = "INSERT INTO graph VALUES (?, ?, ?, ?)"
        self.__traffic_query = "INSERT INTO traffic VALUES (?, ?, ?, ?, ?, ?)"
    #enddef

    def req_traffic (self):
        try:
            response = requests.get(self.__apiURL)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        else:
            root = ET.fromstring(response.text)
        #endtry

        with self.__conn:
            cur = self.__conn.cursor()
            for data in root.findall('data'):
                try:
                    roadid = int(data.find('roadsectionid').text)
                    startnodeid = int(data.find('startnodeid').text)
                    endnodeid = int(data.find('endnodeid').text)
                    name = data.find('roadnametext').text
                    avgspeed = int(data.find('avgspeed').text)
                    traveltime = int(data.find('traveltime').text)
                    gendate = int(data.find('generatedate').text)
                except TypeError:
                    pass
                else:
                    try: # If there is additional edge, then append it.
                        cur.execute(self.__graph_query, (roadid, name, startnodeid, endnodeid))
                    except sqlite3.Error: # Do not insert same data
                        pass
                    #endtry

                    try: # Add new traffic data
                        cur.execute(self.__traffic_query, (roadid, startnodeid, endnodeid, avgspeed, traveltime, gendate))
                    except sqlite3.Error: # Do not insert same data
                        pass
                    #endtry
                #endtry
            #endfor
        #endwith
    #enddef
#endclass


if __name__ == "__main__":
    conf = getSettings()
    openapiSettings = conf['openapi']

    datasetPath = DatasetPath()
    resultDBPath = os.path.join(datasetPath, f"{openapiSettings['filename']}.sqlite3")

    # Query openapi road network traffic data
    apiURL = openapiSettings['URL'] + f"?&zoom=16&key={openapiSettings['key']}"

    conn = sqlite3.connect(resultDBPath)
    # If table does not exist, then create the table
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS graph (id INTEGER PRIMARY KEY, name TEXT, source INTEGER NOT NULL, target INTEGER NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS traffic (id INTEGER NOT NULL, source INTEGER NOT NULL, target INTEGER NOT NULL, avgspeed INTEGER NOT NULL, traveltime INTEGER, generatedate INTEGER NOT NULL, PRIMARY KEY (id, generatedate))")
    #endwith

    # Collect traffic data
    traffic = Traffic(conn, apiURL)
    while True:
        print(datetime.now())
        traffic.req_traffic()
        time.sleep(300)
    #endwhile

    conn.close()
#endif
