# trafficDataParser

trafficDataParser collects the real-time traffic data in Korea.
Every data which this project uses can be found at the following links:

- Nodelink info: <http://nodelink.its.go.kr/data/data01.aspx>
- Traffic info: <http://openapi.its.go.kr/portal/dev/dev3.do>
- Seoul node info: <https://data.seoul.go.kr/dataList/datasetView.do?infId=OA-15061&srvType=F&serviceKind=1>
- Seoul traffic info: <http://data.seoul.go.kr/dataList/datasetView.do?infId=OA-13310&srvType=A&serviceKind=1&currentPageNo=1>

## Getting Started

### Dependencies

- Python >= 3.7

### Install libraries

You have to install all libraries written in 'requirements.txt'

### Download data file

You have to download the '서울특별시 교통소통 표준링크 매핑정보' from the following link:

- Seoul dataset: <https://data.seoul.go.kr/dataList/datasetView.do?infId=OA-15061&srvType=F&serviceKind=1>

### Configure the settings

You have to generate 'settings.yaml' file in 'config' folder, and fill-in the 'key'.
You can get the authorization key of openapi from the following link:

- openapi: <http://openapi.its.go.kr>
- Seoul openapi: <http://data.seoul.go.kr/together/guide/useGuide.do>

## Execute the program

### Collect the node information

Run the following script:

```shell
python collectNodeData.py
```

And then, you can find the output 'nodeData.csv' in the 'Dataset' folder.

### Collect the traffic information

Run the following script:

```shell
python collectTrafficData.py
```

And then, you can find the output 'nodeLink.csv' in the 'Dataset' folder.
