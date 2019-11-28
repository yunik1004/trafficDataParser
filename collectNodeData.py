import os
import sys
import zipfile
import pandas as pd
from pyproj import Proj, transform
import requests
import shapefile


# Download and extract the file
def download (url, filepath):
    if not os.path.isfile(filepath):
        with open(filepath, "wb") as file:
            response = requests.get(url)
            file.write(response.content)
        #endwith
        filezip = zipfile.ZipFile(filepath)
        filezip.extractall(os.path.dirname(filepath))
    #endif
#enddef


if __name__ == "__main__":
    datasetPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dataset")

    # Download Korea standard node link data
    nodeDataURL = "http://nodelink.its.go.kr/Common/download.aspx?mapPath=/FileData/Pds&fileName=[2019-09-20]%20%EC%A0%84%EA%B5%AD%ED%91%9C%EC%A4%80%EB%85%B8%EB%93%9C%EB%A7%81%ED%81%AC.zip"
    download(nodeDataURL, os.path.join(datasetPath, "nodelink.zip"))

    # Read data
    shp_path_node = os.path.join(datasetPath, "MOCT_NODE.shp")
    sf_node = shapefile.Reader(shp_path_node, encoding="cp949")
    #shp_path_link = os.path.join(datasetPath, "MOCT_LINK.shp")
    #sf_link = shapefile.Reader(shp_path_link, encoding="cp949")

    ids = []
    names = []

    for record in sf_node.records():
        ids.append(record[0])
        names.append(record[2])
    #endfor

    inProj = Proj(init = 'epsg:5186')
    outProj = Proj(init = 'epsg:4326')

    latitude = []
    longitude = []

    for idx, feature in enumerate(sf_node.shapes()):
        x, y = feature.points[0][0], feature.points[0][1]
        nx, ny = transform(inProj, outProj, x, y)
        latitude.append(ny)
        longitude.append(nx)
    #endfor

    df_node = pd.DataFrame({'id': ids, 'name': names, 'latitude': latitude, 'longitude': longitude})
    df_node.to_csv(os.path.join(datasetPath, "nodeData.csv"))
#endif
