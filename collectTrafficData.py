import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import requests


if __name__ == "__main__":
    nodes = pd.read_csv('Dataset/nodeData.csv', encoding='cp949')

    graph = nx.DiGraph()

    # Query openapi road network traffic data
    apiURL = "http://openapi.its.go.kr/dev/TrafficInfo.xml;jsessionid=533FDD030B9595A85D82E02634DEB80F" # Should be changed
    response = requests.get(apiURL)
    print("Status code : ", response.status_code)

    xmlData = response.text
    root = ET.fromstring(xmlData)

    for data in root.findall('data'):
        startnodeid = int(data.find('startnodeid').text)
        endnodeid = int(data.find('endnodeid').text)
        avgspeed = float(data.find('avgspeed').text)
        traveltime = int(data.find('traveltime').text)

        graph.add_edge(startnodeid, endnodeid, avgspeed=avgspeed, traveltime=traveltime)
    #endfor

    fig = plt.figure()
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=30)
    nx.draw_networkx_edges(graph, pos)

    plt.show()
#endif
