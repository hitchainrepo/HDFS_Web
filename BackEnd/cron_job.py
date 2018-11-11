# -*- coding: utf-8 -*-

from BackEnd.models import *
from BackEnd.utils import *
import requests

def cron_check_storage():
    nodeIds = StorageReport.objects.values_list('node_id').order_by('-id')
    nodeIdList = []
    for nodeId in nodeIds:
        nodeId = nodeId[0]
        if nodeId not in nodeIdList:
            nodeIdList.append(nodeId)

    for nodeId in nodeIdList:
        reqUrl = "http://localhost:5001/api/v0/ping?arg=" + nodeId + "&count=1"
        responseResult = requests.get(reqUrl)
        responseStatus = responseResult.status_code
        currentTime = getCurrentTime()
        storageCheckItem = StorageCheck()
        storageCheckItem.node_id = nodeId
        storageCheckItem.create_time = currentTime
        if responseStatus == 200:
            # check success
            storageCheckItem.ping_result = True
        else:
            # check failed
            storageCheckItem.ping_result = False
        storageCheckItem.save()