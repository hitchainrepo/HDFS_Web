#-*- coding: utf-8 -*-
import requests
import json

nodeIds = ["QmTXvThuPMHgQyALXVKQYkeaFeMEdA9sQKK6CSqo1Qa7yy"]
for nodeId in nodeIds:
    reqUrl = "http://localhost:5001/api/v0/ping?arg=" + nodeId + "&count=1"
    try:
        req = requests.get(reqUrl)
        response = req.text
        responseLastLine = response.splitlines()[-1]
        responseJson = json.loads(responseLastLine)
        if "Success" not in responseJson:
            ping_result = 0
        else:
            if responseJson["Success"] == True:
                ping_result = 1
            else:
                ping_result = 0
    except Exception as e:
        ping_result = -1