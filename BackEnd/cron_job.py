# -*- coding: utf-8 -*-

from BackEnd.models import *
from BackEnd.utils import *
import requests
import json

def cron_check_storage():
    nodeIds = StorageReport.objects.values_list('node_id').order_by('-id')
    nodeIdList = []
    for nodeId in nodeIds:
        nodeId = nodeId[0]
        if nodeId not in nodeIdList:
            nodeIdList.append(nodeId)

    for nodeId in nodeIdList:
        reqUrl = "http://localhost:5001/api/v0/ping?arg=" + nodeId + "&count=1"
        currentTime = getCurrentTime()
        storageCheckItem = StorageCheck()
        storageCheckItem.node_id = nodeId
        storageCheckItem.create_time = currentTime
        try:
            req = requests.get(reqUrl)
            response = req.text
            responseLastLine = response.splitlines()[-1]
            responseJson = json.loads(responseLastLine)
            if "Success" not in responseJson:
                storageCheckItem.ping_result = 0
            else:
                if responseJson["Success"] == True:
                    storageCheckItem.ping_result = 1
                else:
                    storageCheckItem.ping_result = 0
        except Exception as e:
            storageCheckItem.ping_result = -1
        storageCheckItem.save()