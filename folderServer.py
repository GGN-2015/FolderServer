import os
import json
from flask import Flask
import hashlib
import ggntar

app = Flask(__name__)
HOST        = "0.0.0.0"
PORT        = 15671
DIRNAME     = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(DIRNAME, "config.json")
CHARSET     = "utf-8"

# get config
def __getConfig(config=CONFIG_FILE):
    ans = {}
    with open(config, "r") as f:
        ans = json.load(f)
    return ans

# get string md5
def  __getStringMd5(s: str):
    hl = hashlib.md5()
    hl.update(s.encode(CHARSET))
    ans = hl.hexdigest()
    return ans.upper()

# check token
def __checkConfigList(token):
    config = __getConfig()
    if config.get(token) != None:
        return True
    else:
        md5List = config["MD5_TOKEN"]
        for file in md5List:
            if __getStringMd5(file) == token:
                return True
        return False

# get file in config
def __getFileInConfig(token):
    config = __getConfig()
    if config.get(token) != None:
        return config[token]
    else:
        md5List = config["MD5_TOKEN"]
        for file in md5List:
            if __getStringMd5(file) == token:
                return file
        assert False

# get file
@app.route("/file/ggntar.py")
def getAlgo():
    filename = os.path.join(DIRNAME, "ggntar.py")
    return open(filename).read()

# get file
@app.route("/api/<token>")
def getTar(token: str):
    if not __checkConfigList(token) or token == "MD5_TOKEN":
        return ""
    else:
        folder = __getFileInConfig(token)
        return ggntar.maketar(os.path.join(DIRNAME, folder))

# run app
if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
