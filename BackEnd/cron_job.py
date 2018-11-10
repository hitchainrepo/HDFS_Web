# -*- coding: utf-8 -*-

from BackEnd.models import *
from BackEnd.utils import *

def cron_check_storage():
    nodeIds = StorageReport.objects.values_list('node_id').order_by('-id')
    nodeIdList = []
    for nodeId in nodeIds:
        nodeId = nodeId[0]
        if nodeId not in nodeIdList:
            nodeIdList.append(nodeId)

    for nodeId in nodeIdList:
