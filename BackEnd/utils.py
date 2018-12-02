import datetime
import random
import os
import shutil
import pytz
import configparser
import HDFS_Web.contexts as contexts

def getCurrentTime():
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S', tzinfo=pytz.UTC)
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