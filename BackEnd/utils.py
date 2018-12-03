import datetime
import random
import os
import shutil
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode
import base64

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
    digest.update(str(data).encode("utf8"))
    if signer.verify(digest, b64decode(signature)):
        return True
    return False

if __name__ == "__main__":
    import pymysql
    conn = pymysql.Connect(
        host='47.105.76.115',
        port=3306,
        user='root',
        passwd='pdl123456',
        db='HDFS_Web',
        charset='utf8'
    )

    # 获取游标
    cursor = conn.cursor()
    cursor.execute("select public_key from temporary_public_key where id=1")
    item = cursor.fetchone()
    pub_key = item[0]
    print(pub_key)
    # pub_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC7kw8r6tq43pwApYvkJ5laljaN9BZb21TAIfT/vexbobzH7Q8SUdP5uDPXEBKzOjx2L28y7Xs1d9v3tdPfKI2LR7PAzWBmDMn8riHrDDNpUpJnlAGUqJG9ooPn8j7YNpcxCa1iybOlc2kEhmJn5uwoanQq+CA6agNkqly2H4j6wIDAQAB"
    # pub_key = "CAASpgIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDAHCzXkhEKdsDJff57_dL8ypmsR01s4h837ZaZYdTDncVuOn24ekCwVeNu6CL-XNTWeyOfESv8ykzbEBVYUV_mubDIuKVFS4IyfHv8SMzj0cpIrpxSW1zqyF4iws6OahAUNTueClQFbU6gmeXZq7vuRb6SbXe5X2O-WAF-93YySCI4Ac1aG6QbgF5umlxJYn2Q6j5igKgaxm4Z9tVHTTXQkhrEY2lN_Zk4NjgrwmedDdtNe1EfHNE8psY2_M2v8YaK5COi-B_zJfKX2Qme0pjnSX_9qMvsNEe8WuAS7zVRlxwSKjcwqoFpDMEAy126GScAgoyeoNoOyUkKJpjx4hhlAgMBAAE="
    # pub_key = "CAASpgIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDAHCzXkhEKdsDJff57_dL8ypmsR01s4h837ZaZYdTDncVuOn24ekCwVeNu6CL-XNTWeyOfESv8ykzbEBVYUV_mubDIuKVFS4IyfHv8SMzj0cpIrpxSW1zqyF4iws6OahAUNTueClQFbU6gmeXZq7vuRb6SbXe5X2O-WAF-93YySCI4Ac1aG6QbgF5umlxJYn2Q6j5igKgaxm4Z9tVHTTXQkhrEY2lN_Zk4NjgrwmedDdtNe1EfHNE8psY2_M2v8YaK5COi-B_zJfKX2Qme0pjnSX_9qMvsNEe8WuAS7zVRlxwSKjcwqoFpDMEAy126GScAgoyeoNoOyUkKJpjx4hhlAgMBAAE="
    # pub_key = "1231231231231232132132131231232111111111111111111111111111111111111111111111111111132132131232132132132132132132132132132131232132131231232132132132132132132132132131321321312321321321321321321321321321321321321312312321321321321312321312321321312321321321321321321312321321321321321621784671328472148712487214832413878412874281794821804821804872188647216748128491848371847184314328413483294638370238"
    pub_key = base64.b64decode(pub_key)
    print(pub_key)
    # b64_str = base64.b64decode(pub_key)
    # print(len(b64_str))
    # key = str2key(pub_key)
    # print(key)
    verify_sign(pub_key, "1123123", "123123")