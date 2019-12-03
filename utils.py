import os
import sys
import zipfile
import requests
import yaml


# Download and extract the file
def download (url, filepath):
    if not os.path.isfile(filepath):
        with open(filepath, "wb") as file:
            response = requests.get(url)
            file.write(response.content)
        #endwith
    #endif
#enddef


# Extract the file
def extract (filepath, dirpath):
    if not os.path.isdir(dirpath):
        filezip = zipfile.ZipFile(filepath)
        filezip.extractall(dirpath)
        filezip.close()
    #endif
#enddef


# Path of the 'Dataset folder'
def DatasetPath ():
    datasetPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dataset")
    if not os.path.isdir(datasetPath):
        os.makedirs(datasetPath)
    #endif
    return datasetPath
#enddef


# Get settings in 'settings.yaml'
def getSettings ():
    settingsPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "settings.yaml")
    if not os.path.isfile(settingsPath):
        print("Make settings.yaml file in the config folder!!!")
        sys.exit(1)
    #endif

    with open(settingsPath, encoding="utf-8") as f:
        conf = yaml.safe_load(f)
    #endwith

    return conf
#enddef
