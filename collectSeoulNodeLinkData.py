import os
import sqlite3
import requests
import xlrd
from utils import DatasetPath, getSettings


if __name__ == "__main__":
    conf = getSettings()
    seoulSettings = conf['seoulnodelink']
    mappingFilename = seoulSettings['mappingfilename']
    fileName = seoulSettings['filename']

    datasetPath = DatasetPath()
    mappingFilePath = os.path.join(datasetPath, mappingFilename)
    resultFilePath = os.path.join(datasetPath, f"{fileName}.sqlite3")

    # Parsing the mapping file
    wb = xlrd.open_workbook(mappingFilePath)
    ws = wb.sheet_by_index(0)

    ids = list(map(int, ws.col_values(2)[1:]))
    serviceids = list(map(int, ws.col_values(0)[1:]))
    rows = []

    wb.release_resources()

    nodelinkPath = os.path.join(datasetPath, f"{conf['nodelink']['filename']}.sqlite3")
    conn_nodelink = sqlite3.connect(nodelinkPath)
    with conn_nodelink:
        cur = conn_nodelink.cursor()
        query = "SELECT * FROM link WHERE id=?"
        for i in range(len(ids)):
            cur.execute(query, (ids[i], ))
            row = cur.fetchone()
            if row:
                rows.append((serviceids[i], row))
            #endif
        #endfor
    #endwith
    conn_nodelink.close()

    conn_seoul_nodelink = sqlite3.connect(resultFilePath)
    with conn_seoul_nodelink:
        cur = conn_seoul_nodelink.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS link (id INTEGER PRIMARY KEY, serviceid INTEGER NOT NULL, name TEXT, source INTEGER NOT NULL, target INTEGER NOT NULL)")

        query = "INSERT INTO link VALUES (?, ?, ?, ?, ?)"
        for row in rows:
            try:
                cur.execute(query, (row[1][0], row[0], row[1][1], row[1][2], row[1][3]))
            except sqlite3.Error: # Do not insert same data
                pass
            #endtry
        #endfor
    #endwith
    conn_seoul_nodelink.close()
#endif
