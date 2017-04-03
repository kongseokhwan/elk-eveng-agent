__author__ = 'kongseokhwan'

import requests
ROUTER_ID = '0000-0000-0000-0000'

GET_NODES_URL = "/api/v1/nodes"
POST_ROUTER_INTERFACE_URL = "/1.0/openstack/routers/%s/ports" % ROUTER_ID
DELETE_ROUTER_INTERFACE_URL = "/1.0/openstack/routers/%s/ports/%s"

INTERFACE_ARG = {
    "intf_name" : None,
    "dpid": None,
    "port": None,
    "ip_address" : None,
    "network_cidr" : None,
    "type" :  None,
    "vlan_id" : None
}

POST_ROUTER_INTERFACE_ARG = {
    "interfaces": []
}

class PRISMClient():
    def __init__(self, ip):
        self.ip = ip
        self.base_url = "http://"+self.ip+":8080"
        self.default_vlan = 100
        self.intf_id_db = {}

    def _url(self, path):
        return self.base_url + path

    def post_gateway_interface(self, subnet, gateway_ip):
        self.default_vlan += 1

        '''
        TODO : KONG
        intf_name = 'pr-vlan' + str(self.default_vlan)
        INTERFACE_ARG['intf_name'] = intf_name
        INTERFACE_ARG['dpid'] = None
        INTERFACE_ARG['ip_address'] = gateway_ip
        INTERFACE_ARG['network_cidr'] = subnet
        INTERFACE_ARG['type'] = None
        INTERFACE_ARG['vlan_id'] = self.default_vlan
        POST_ROUTER_INTERFACE = {
            "interfaces": []
        }
        POST_ROUTER_INTERFACE['interfaces'].append(INTERFACE_ARG)
        intf_id = requests.post(POST_ROUTER_INTERFACE_URL, data = POST_ROUTER_INTERFACE)
        self.intf_id_db[id] = intf_id
        '''

        return {'id': self.default_vlan, 'vlan': self.default_vlan}

    def delete_gateway_interface(self, id):
        '''
        TODO : KONG
        DELETE_ROUTER_INTERFACE_URL = DELETE_ROUTER_INTERFACE_URL % (ROUTER_ID, id)
        intf_id = requests.delete(POST_ROUTER_INTERFACE_URL)
        del self.intf_id_db.[id]
        '''

        return {'id': id, 'vlan': id}

    def get_nodes(self):
        resp = requests.get(self._url(GET_NODES_URL))
        if resp.status_code != 201:
            return resp.json()

        if resp.status_code != 200:
            return resp.json()

        #TODO : Parse ust NODES info
        return resp.json()
