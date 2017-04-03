__author__ = 'kongseokhwan'

import requests
from pymongo import MongoClient

class LibPrismDBClient():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.mongo_client = None

    def get_nodes(self):
        self.mongo_client = MongoClient(self.ip, int(self.port))
        LibnetPrism_db = self.mongo_client.libnetprism_database
        slave_col = LibnetPrism_db.slaves
        nodes = []

        for node in slave_col.find():
            del node['_id']
            nodes.append(node['node'])
        self.mongo_client.close()

        return nodes