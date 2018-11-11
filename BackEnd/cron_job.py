# -*- coding: utf-8 -*-

from BackEnd.models import *
from BackEnd.utils import *
from urllib.request import Request, urlopen

def cron_check_storage():
    nodeIds = StorageReport.objects.values_list('node_id').order_by('-id')
    nodeIdList = []
    for nodeId in nodeIds:
        nodeId = nodeId[0]
        if nodeId not in nodeIdList:
            nodeIdList.append(nodeId)

    for nodeId in nodeIdList:
        reqUrl = "http://localhost:5001/api/v0/ping?arg=" + nodeId + "&count=1"
        req = Request(reqUrl)
        currentTime = getCurrentTime()
        storageCheckItem = StorageCheck()
        storageCheckItem.node_id = nodeId
        storageCheckItem.create_time = currentTime
        try:
            response = urlopen(req)
            if response.status == 200:
                storageCheckItem.ping_result = True
            else:
                storageCheckItem.ping_result = False
        except Exception as e:
            storageCheckItem.ping_result = False
        storageCheckItem.save()