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
    resultPath = os.path.join(datasetPath, f"{fileName}.db")

    # Download Korea standard node link data
    nodeDataURL = openapiSettings['URL']
    download(nodeDataURL, downloadPath)
    extract(downloadPath, extractPath)

    # Read data
    shp_path_node = os.path.join(extractPath, "MOCT_NODE.shp")
    sf_node = shapefile.Reader(shp_path_node, encoding="cp949")
    #shp_path_link = os.path.join(extractPath, "MOCT_LINK.shp")
    #sf_link = shapefile.Reader(shp_path_link, encoding="cp949")

    ids = []
    names = []
    latitude = []
    longitude = []

    for record in sf_node.records():
        ids.append(record[0])
        names.append(record[2])
    #endfor

    inProj = Proj(init = 'epsg:5186')
    outProj = Proj(init = 'epsg:4326')

    for feature in sf_node.shapes():
        x, y = feature.points[0][0], feature.points[0][1]
        nx, ny = transform(inProj, outProj, x, y)
        latitude.append(ny)
        longitude.append(nx)
    #endfor

    conn = sqlite3.connect(resultPath)
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS node (id INTEGER PRIMARY KEY, name TEXT, latitude REAL NOT NULL, longitude REAL NOT NULL)")

        query = "INSERT INTO node VALUES (?, ?, ?, ?)"
        for i in range(len(ids)):
            cur.execute(query, (ids[i], names[i], latitude[i], longitude[i]))
        #endfor
    #endwith
    conn.close()
#endif
