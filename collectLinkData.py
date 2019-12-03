import os
import sqlite3
from pyproj import Proj, transform
import requests
import shapefile
from utils import download, extract, DatasetPath, getSettings


if __name__ == "__main__":
    conf = getSettings()
    openapiSettings = conf['nodelink']
    fileName = openapiSettings['filename']

    datasetPath = DatasetPath()
    downloadPath = os.path.join(datasetPath, f"{fileName}.zip")
    extractPath = os.path.join(datasetPath, f"{fileName}")
    resultPath = os.path.join(datasetPath, f"{fileName}.sqlite3")

    # Download Korea standard node link data
    nodeDataURL = openapiSettings['URL']
    download(nodeDataURL, downloadPath)
    extract(downloadPath, extractPath)

    # Read data
    shp_path_link = os.path.join(extractPath, "MOCT_LINK.shp")
    sf_link = shapefile.Reader(shp_path_link, encoding="cp949")

    ids = []
    names = []
    sources = []
    targets = []

    for record in sf_link.records():
        ids.append(record[0])
        names.append(record[7])
        sources.append(record[1])
        targets.append(record[2])
    #endfor

    conn = sqlite3.connect(resultPath)
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS link (id INTEGER PRIMARY KEY, name TEXT, source INTEGER NOT NULL, target INTEGER NOT NULL)")

        query = "INSERT INTO link VALUES (?, ?, ?, ?)"
        for i in range(len(ids)):
            cur.execute(query, (ids[i], names[i], sources[i], targets[i]))
        #endfor
    #endwith
    conn.close()
#endif
