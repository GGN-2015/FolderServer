import pathlib
import base64
import os
import sys

CHARSET = "utf-8"
DIRNAME = os.path.dirname(__file__)

# get relative path list for all file in folder
def __getFilesInFolder(folder:str) -> list:
    path = pathlib.Path(folder)
    ans = [str(f.relative_to(folder)) for f in path.rglob("*") if f.is_file()]
    ans.sort()
    return ans

# get base64 from str
def __getBase64FromStr(s: str) -> str:
    data = base64.b64encode(s.encode(CHARSET))
    return data.decode('ascii')

# decode base64 from bytes
def __decodeBase64FromBytes(b: str) -> bytes:
    data = base64.b64decode(b.encode('ascii'))
    return data

# get base64 from file
def __getBase64FromFile(file:str) -> str:
    f = open(file, "rb")
    data = base64.b64encode(f.read())
    return data.decode('ascii')

# get base64 pair for file
def __getBasePair(file:str, filepath:str):
    return __getBase64FromStr(file) + "$" + __getBase64FromFile(filepath)

# make a ggn tar
def maketar(folder:str) -> str:
    assert os.path.isdir(folder)
    ans = []
    for file in __getFilesInFolder(folder):
        filepath = os.path.join(folder, file)
        ans.append(__getBasePair(file, filepath))
    return ";".join(ans)

# get folder name
def __getFolderNameFromInFileName(infile):
    lis = infile.split('.')
    if len(lis) > 1 and lis[-1] == "ggntar":
        name = infile[:-len(".ggntar")]
    else:
        assert False # must .ggntar
    return name

# make a folder
def unziptar(tar: str, folder: str):
    if folder != "" and folder != ".":
        os.makedirs(folder)
    for subtar in tar.split(';'):
        if subtar.find('$') == -1:
            print("warning: unavailable structure")
            continue
        name, subtar = subtar.split('$', 1)
        name = __decodeBase64FromBytes(name).decode(CHARSET)
        filename = os.path.join(folder, name)
        dir = os.path.dirname(filename)
        if not os.path.exists(dir) and dir != "":
            os.makedirs(dir)
        print("generating: " + filename)
        with open(filename, "wb") as f:
            f.write(__decodeBase64FromBytes(subtar))

# cli
if __name__ == "__main__":
    mode = sys.argv[1]
    assert mode in ["zip", "unzip"] # zip or unzip
    if mode == "unzip":
        infile = sys.argv[2]
        tar    = open(infile).read()
        folder = __getFolderNameFromInFileName(infile)
        unziptar(tar, folder)
    elif mode == "zip":
        folder  = sys.argv[2]
        outfile = sys.argv[3]
        with open(outfile, "w") as f:
            f.write(maketar(folder))
    else:
        print("usage: python ggntar.py unzip <infile>")
        print("       python ggntar.py   zip <folder> <outfile>")
        assert False
