__author__ = 'kongseokhwan'

import requests
from pymongo import MongoClient

GET_NODES_URL = "/api/v1/nodes"

class K8sClient():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.mongo_client = None

        self.base_url = "http://"+self.ip+":8080"

    def _url(self, path):
        return self.base_url + path

    def get_nodes(self):
        self.mongo_client = MongoClient(self.ip, int(self.port))
        K8snetPrism_db = self.mongo_client.k8snetprism_database
        slave_col = K8snetPrism_db.slaves
        nodes = []

        resp = requests.get(self._url(GET_NODES_URL))
        resp_nodes = resp.json()['items']

        for node in resp_nodes  :
            if node['spec']['externalID'] != '127.0.0.1':
                nodes.append(node['spec']['externalID'])

        # TODO : MongoDB Update
        self.mongo_client.close()

        return nodes


