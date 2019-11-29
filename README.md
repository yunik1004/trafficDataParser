# trafficDataParser

trafficDataParser collects the real-time traffic data in Korea.
Every data which this project uses can be found at the following links:

- Node info: <http://nodelink.its.go.kr/data/data01.aspx>
- Traffic info: <http://openapi.its.go.kr/portal/dev/dev3.do>

## Getting Started

### Dependencies

- Python >= 3.7

### Install libraries

You have to install all libraries written in 'requirements.txt'

### Configure the settings

You have to generate 'settings.yaml' file in 'config' folder, and fill-in the 'authKey'.
You can get the authorization key of openapi from the following link:

- openapi: <http://openapi.its.go.kr>

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
