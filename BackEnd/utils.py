import datetime
import random
import os
import shutil
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode
import base64
import geoip2.database

def getCurrentTime():
    create_time = datetime.datetime.utcnow()
    return create_time


def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def mkdir(path):
    # new folder
    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)

    if not isExists:
        print(path+': create successfull')
        os.makedirs(path)
        return True
    else:
        print(path+': path already exist')
        return False


def createLocalRepository(repoInfo, userInfo):
    baseDir = "Repos"
    username = userInfo["username"]
    reponame = repoInfo["reponame"]

    dirPath = os.path.join(baseDir, username, reponame)

    if os.path.exists(dirPath):
        shutil.rmtree(dirPath)

    os.makedirs(dirPath)

    os.system("git init %s" % (dirPath)) # git init the path

    # hitPath = os.path.join(dirPath, ".hit")
    #
    # mkdir(hitPath)
    # configPath = os.path.join(hitPath, "config")
    # cf = configparser.ConfigParser()
    # cf.read(configPath)
    # cf.add_section("remote \"origin\"")
    # cf.set("remote \"origin\"", "repoName", reponame)
    # cf.set("remote \"origin\"", "userName", username)
    # cf.set("remote \"origin\"", "url", "http://" + contexts.globalVariables()["webUrl"] + "/" + username + "/" +reponame + ".hit")
    # with open(configPath, "w+") as f:
    #     cf.write(f)

    cwd = os.getcwd()

    # os.chdir(dirPath)
    # os.system("git add .")
    # os.system("git commit -m 'hit init'")
    # os.chdir(cwd)

    cloneRepoPath = dirPath + "_clone"
    os.system("git clone --bare %s %s" % (dirPath, cloneRepoPath))
    os.chdir(cloneRepoPath)
    os.system("git update-server-info")
    os.chdir(cwd)

    return dirPath, cloneRepoPath

# return IpfsHash if added completely
# else return None
def createIpfsRepository(repoInfo, userInfo):
    repoPath, cloneRepoPath = createLocalRepository(repoInfo, userInfo)
    addResponse = os.popen("ipfs add -rH " + cloneRepoPath).read()
    lastline = addResponse.splitlines()[-1].lower()
    if lastline != "added completely!":
        return None
    newRepoHash = addResponse.splitlines()[-2].split(" ")[1]
    shutil.rmtree(repoPath) # after added to ipfs net, remove the local repo
    shutil.rmtree(cloneRepoPath)
    return newRepoHash


# rsa sha256 verify signature
def verify_sign(pub_key, signature, data):
    # keyDER = b64decode(pub_key)
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(data.encode("utf8"))
    if signer.verify(digest, b64decode(signature)):
        return True
    return False

def getLocByIpList(ipList):
    try:
        result = []
        errors = []
        reader = geoip2.database.Reader("BackEnd/GeoLite2-City.mmdb")
        for ip in ipList:
            response = reader.city(ip)
            longitude = response.location.longitude
            latitude = response.location.latitude
            if longitude is None or latitude is None:
                errors.append(ip)
                continue
            result.append((longitude, latitude))
        return result, errors
    except Exception as e:
        print(e)
        return None, None

def getCityByIpList(ipList):
    try:
        resultMap = {}
        reader = geoip2.database.Reader("BackEnd/GeoLite2-City.mmdb")
        for ip in ipList:
            response = reader.city(ip)
            out = response.city.name
            if out is None:
                out = response.country.name
                if out is None:
                    out = response.continent.name
            if out is None:
                out = "No Name Place"
            resultMap.setdefault(out, [])
            if len(resultMap[out]) == 1:
                resultMap[out] = [(out+" 1", resultMap[out][0][1]), (out+" 2", ip)]
            elif len(resultMap[out]) > 1:
                print(len(resultMap[out]) + 1)
                print(out+" "+str(len(resultMap[out]) + 1))
                resultMap[out].append((out+" "+str(len(resultMap[out]) + 1), ip))
            else:
                resultMap[out].append((out, ip))
        return resultMap
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    print("test")
    print(getCityByIpList(['47.89.185.83']))