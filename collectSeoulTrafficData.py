from datetime import datetime
import os
from shutil import copyfile
import sqlite3
import sys
import time
import requests
import xml.etree.ElementTree as ET
from utils import DatasetPath, getSettings


class SeoulTraffic:
    def __init__ (self, conn, apiURL):
        self.__conn = conn
        self.__apiURL = apiURL
        self.__time_query = "INSERT INTO time(dateidx) VALUES (?)"
        self.__traffic_query = ""
        self.__timeIndex = 0

        # Implement dictionary with same service ID {serviceid: [linkid, linkid, linkid]}
        self.__linkDict = dict()
        with self.__conn:
            cur = self.__conn.cursor()
            cur.execute("SELECT * FROM link")
            rows = cur.fetchall()
            for row in rows:
                if row[1] in self.__linkDict:
                    self.__linkDict[row[1]].append(row[0])
                else:
                    self.__linkDict[row[1]] = [row[0]]
                #endif
            #endfor
        #endwith
    #enddef

    def req_traffic (self):
        with self.__conn:
            cur = self.__conn.cursor()
            try:
                cur.execute(self.__time_query, (self.__timeIndex, ))
            except sqlite3.Error: # Do not insert same data
                print("You should not append the data into the DB")
                sys.exit(1)
            #endtry
        #endwith

        # TODO: implement request
        results = []
        for key in self.__linkDict:
            res = self.__getTraffic(key)
        #endfor
        print(datetime.now())

        self.__timeIndex += 1
    #enddef

    def __getTraffic (self, serviceid):
        try:
            response = requests.get(self.__apiURL + str(serviceid))
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        else:
            try:
                root = ET.fromstring(response.text)
            except:
                print(response.text)
                return None
            #endtry
            code = root.find('RESULT').find('CODE').text
            if code == "INFO-200":
                print(f"Serviceid {serviceid} not found")
                return None
            elif code != "INFO-000":
                print(code)
                sys.exit(1)
            #endif
        #endtry
        data = root.find('row')

        speed = data.find('prcs_spd').text
        travel_time = data.find('prcs_trv_time').text

        return (speed, travel_time)
    #enddef
#endclass


if __name__ == "__main__":
    conf = getSettings()
    seoulTrafficSettings = conf['seoultraffic']

    datasetPath = DatasetPath()
    nodelinkPath = os.path.join(datasetPath, f"{conf['seoulnodelink']['filename']}.sqlite3")
    resultDBPath = os.path.join(datasetPath, f"{seoulTrafficSettings['filename']}.sqlite3")

    if not os.path.isfile(resultDBPath):
        copyfile(nodelinkPath, resultDBPath)
    #endif

    apiURL = seoulTrafficSettings['URL'] + f"/{seoulTrafficSettings['key']}/xml/TrafficInfo/1/1/"
    conn = sqlite3.connect(resultDBPath)
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS traffic (id INTEGER NOT NULL, source INTEGER NOT NULL, target INTEGER NOT NULL, avgspeed INTEGER NOT NULL, traveltime INTEGER, dateidx INTEGER NOT NULL, PRIMARY KEY (id, dateidx))")
        cur.execute("CREATE TABLE IF NOT EXISTS time (dateidx INTEGER PRIMARY KEY, generatedate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)")
    #endwith

    sTraffic = SeoulTraffic(conn, apiURL)
    while True:
        print(datetime.now())
        sTraffic.req_traffic()
        time.sleep(300)
    #endwhile
    conn.close()
#endif
