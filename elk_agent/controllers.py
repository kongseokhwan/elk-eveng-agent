# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# TODO
# node db validation needs
'''
{u'node': u'172.31.0.207', u'_id': ObjectId('5743ba662eecd04661cc4d78')}
{u'node': u'172.31.0.207', u'_id': ObjectId('5743ba662eecd04661cc4d79')}
'''
#
# need vlan pool management



import os


import jsonschema
import netaddr
from oslo_config import cfg

from prism import app
from prism.common import constants
from prism.common import exceptions
from prism.common.prism_client import PRISMClient
from prism import schemata
from prism import utils

import argparse
import ast
import atexit
import json
import os
import random
import re
import shlex
import subprocess
import sys

import ovs.dirs
import ovs.util
import ovs.daemon
import ovs.vlog

import flask
from flask import Flask, jsonify
from flask import request, abort
from pymongo import MongoClient
import consulate
from prism_kubernetes_agent import PrismKubernetesAgent

CONSUL_KV_NODE = "docker/nodes/"

app = Flask(__name__)
vlog = ovs.vlog.Vlog("ovn-docker-overlay-driver")

lport_db = {}
lhost_db = {}
net_db = {}
default_vlan = 100

opt_default_group = cfg.OptGroup(name='default', title='A default informations')
default_opts = [
        cfg.IntOpt('polling_interval', default='2',
                    help=('Define Agents polling interval')),
        cfg.StrOpt('ip', default='localhost',
                    help=('Define prism host ip address')),
        cfg.StrOpt('mode', default='master',
                    help=('Define prism kubernetes master/slave')),
        cfg.StrOpt('DOCKER_BRIDGE', default='docker0',
                    help=('Define docker bridge name')),
        cfg.StrOpt('PRISM_BRIDGE', default='br-pr',
                    help=('Define prism bridge name')),
        cfg.StrOpt('TUN_BRIDGE', default='br-tun',
                    help=('Define prism tunnel bridge name')),
        cfg.StrOpt('OPENFLOW_PROTOCOL', default='OpenFlow13',
                    help=('Define prism bridge openflow protocol')),
        cfg.StrOpt('DOCKER_BRIDGE_VETH', default='veth-docker0',
                    help=('Define docker bridge vif name')),
        cfg.StrOpt('PRISM_BRIDGE_VETH', default='veth-br-pr',
                    help=('Define prism bridge vif name')),
        cfg.StrOpt('PRISM_BRIDGE_VETH1', default='veth-br-pr1',
                    help=('Define prism bridge vif1 name')),
        cfg.StrOpt('TUN_BRIDGE_VETH', default='veth-br-tun',
                    help=('Define prism tunnel bridge vif name')),
        cfg.StrOpt('CONTROLLER_IP', default='127.0.0.1',
                    help=('Define prism controller ip')),
        cfg.StrOpt('CONTROLLER_PORT', default='6653',
                    help=('Define prism controller port')),
        cfg.StrOpt('DOCKER_OPTS', default='/etc/default/docker',
                    help=('Define docker option file')),
        cfg.StrOpt('LOCAL_NODE_IP', default='127.0.0.1',
                    help=('Define Local node datapath IP')),
        cfg.StrOpt('MASTER_NODE_IP', default='127.0.0.1',
                    help=('Define MASTER node datapath IP'))
]
CONF = cfg.CONF
CONF.register_group(opt_default_group)
CONF.register_opts(default_opts, opt_default_group)
CONF(default_config_files=['prism_kubernetes.conf'])


#prism_agent = PrismKubernetesAgent(CONF)
prism_nbapi_client = PRISMClient(CONF.default.CONTROLLER_IP)

mongo_client = MongoClient(CONF.default.MASTER_NODE_IP, 27017)
LibnetPrism_db = mongo_client.libnetprism_database

# Init DB Sync with MongoDB for vnet
vnet_col = LibnetPrism_db.vnets
for net in vnet_col.find():
    del net['_id']
    net_db[net['network']] = net
mongo_client.close()


def call_popen(cmd):
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = child.communicate()
    if child.returncode:
        raise RuntimeError("Fatal error executing %s" % (cmd))
    if len(output) == 0 or output[0] == None:
        output = ""
    else:
        output = output[0].strip()
    return output

def call_prog(prog, args_list):
    cmd = [prog, "--timeout=5", "-vconsole:off"] + args_list
    return call_popen(cmd)


def ovs_vsctl(*args):
    return call_prog("ovs-vsctl", list(args))

def prism_get_vlan(nid):
    mongo_client = MongoClient(CONF.default.MASTER_NODE_IP, 27017)
    LibnetPrism_db = mongo_client.libnetprism_database
    slave_col = LibnetPrism_db.vnets
    net_cur = slave_col.find({"network": str(nid)})
    for doc in net_cur:
        net = doc
    mongo_client.close()

    #return net_db[nid]
    return net


def prism_create_net(nid, subnet, gateway_ip):
    resp = prism_nbapi_client.post_gateway_interface(subnet, gateway_ip)
    vnet = {
        'vlan_tag': resp['vlan'],
        'id': resp['id'],
        'subnet': subnet,
        'network': nid,
        'gateway_ip': gateway_ip }
    net_db[nid] = vnet
    return vnet


def prism_delete_net(nid):
    net = net_db[nid]
    # TODO : Update prism API
    # resp = prism_nbapi_client.delete_gateway_interface(nid, net['subnet'], net['gateway_ip'])
    del net_db[nid]


def prism_delete_port(eid):
    del net_db[eid]


def prism_host_register_db(remote_ip):
    mongo_client = MongoClient(CONF.default.MASTER_NODE_IP, 27017)
    LibnetPrism_db = mongo_client.libnetprism_database
    slave_col = LibnetPrism_db.slaves
    slave_col.insert_one({"node": str(remote_ip)})
    mongo_client.close()

def prism_host_unregister_db(remote_ip):
    mongo_client = MongoClient(CONF.default.MASTER_NODE_IP, 27017)
    LibnetPrism_db = mongo_client.libnetprism_database
    slave_col = LibnetPrism_db.slaves
    slave_col.remove({"node": str(remote_ip)})
    mongo_client.close()

def prism_host_registered(remote_ip):
    mongo_client = MongoClient(CONF.default.MASTER_NODE_IP, 27017)
    LibnetPrism_db = mongo_client.libnetprism_database
    slave_col = LibnetPrism_db.slaves
    if slave_col.find({"node": str(remote_ip)}) is None:
        mongo_client.close()
        return False
    else:
        mongo_client.close()
        return True

def prism_db_init_sync():
    mongo_client = MongoClient(CONF.default.MASTER_NODE_IP, 27017)
    LibnetPrism_db = mongo_client.libnetprism_database
    slave_col = LibnetPrism_db.slaves

    consul = consulate.Consul()
    node_keys = consul.kv.find(CONSUL_KV_NODE)

    slave_col.drop()
    slave_col = LibnetPrism_db.slaves
    for node in node_keys:
        # TODO: parse node docker/nodes/192.168.1.8:2376
        node_ip = str(node).split('/')[2]
        if node_ip != CONF.default.MASTER_NODE_IP+':2376':
            slave_col.insert_one({"node": str(node_ip.split(':')[0])})
    mongo_client.close()

'''
def prism_activate():
    prism_prepare()
'''

@app.route('/Plugin.Activate', methods=['POST'])
def plugin_activate():
    if CONF.default.mode == 'master':
        prism_db_init_sync()
    return flask.jsonify({"Implements": ["NetworkDriver"]})


@app.route('/NetworkDriver.GetCapabilities', methods=['POST'])
def plugin_scope():
    return flask.jsonify({"Scope": "global"})

@app.route('/NetworkDriver.DiscoverNew', methods=['POST'])
def network_driver_discover_new():
    """The callback function for the DiscoverNew notification.
    The DiscoverNew notification includes the type of the
    resource that has been newly discovered and possibly other
    information associated with the resource.
    See the following link for more details about the spec:
      https://github.com/docker/libnetwork/blob/master/docs/remote.md#discovernew-notification  # noqa
    """
    if CONF.default.mode == 'slave':
        return jsonify(constants.SCHEMA['SUCCESS'])

    data = json.loads(request.data)
    remote_ip = data['DiscoveryData']['Address']

    if remote_ip == CONF.default.MASTER_NODE_IP:
        return jsonify(constants.SCHEMA['SUCCESS'])

    if remote_ip is not prism_host_registered(remote_ip):
        print ('Discover new : ' + remote_ip)
        prism_host_register_db(remote_ip)

    return jsonify(constants.SCHEMA['SUCCESS'])


@app.route('/NetworkDriver.DiscoverDelete', methods=['POST'])
def network_driver_discover_delete():
    """The callback function for the DiscoverDelete notification.
    The DiscoverDelete notification includes the type of the
    resource that has been deleted and possibly other
    information associated with the resource.
    See the following link for more details about the spec:
      https://github.com/docker/libnetwork/blob/master/docs/remote.md#discoverdelete-notification  # noqa
    """
    if CONF.default.mode == 'slave':
        return jsonify(constants.SCHEMA['SUCCESS'])
    data = json.loads(request.data)
    remote_ip = data['DiscoveryData']['Address']

    #if remote_ip is prism_host_registered(remote_ip):
    print ('Discover Delete : ' + remote_ip)
    prism_host_unregister_db(remote_ip)

    return jsonify(constants.SCHEMA['SUCCESS'])

@app.route('/NetworkDriver.CreateNetwork', methods=['POST'])
def network_driver_create_network():
    if not request.data:
        abort(400)

    data = json.loads(request.data)

    # NetworkID will have docker generated network uuid and it
    # becomes 'name' in a OVN Logical switch record.
    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    # Limit subnet handling to ipv4 till ipv6 usecase is clear.
    ipv4_data = data.get("IPv4Data", "")
    if not ipv4_data:
        error = "create_network: No ipv4 subnet provided"
        return jsonify({'Err': error})

    subnet = ipv4_data[0].get("Pool", "")
    if not subnet:
        error = "create_network: no subnet in ipv4 data from libnetwork"
        return jsonify({'Err': error})

    gateway_ip = ipv4_data[0].get("Gateway", "").rsplit('/', 1)[0]
    if not gateway_ip:
        error = "create_network: no gateway in ipv4 data from libnetwork"
        return jsonify({'Err': error})

    try:
        # TODO : Call PRISM Interface_add
        # return : vlan, subnet, gateway_ip
        vnet = prism_create_net(nid, subnet, gateway_ip)
        mongo_client = MongoClient(CONF.default.MASTER_NODE_IP, 27017)
        LibnetPrism_db = mongo_client.libnetprism_database
        vnet_col = LibnetPrism_db.vnets
        vnet_col.insert_one(vnet)
        mongo_client.close()

    except Exception as e:
        error = "create_network: lswitch-add %s" % (str(e))
        return jsonify({'Err': error})

    return jsonify({})

@app.route('/NetworkDriver.DeleteNetwork', methods=['POST'])
def network_driver_delete_network():
    if not request.data:
        abort(400)

    data = json.loads(request.data)

    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    try:
        prism_delete_net(nid)
        mongo_client = MongoClient(CONF.default.MASTER_NODE_IP, 27017)
        LibnetPrism_db = mongo_client.libnetprism_database
        vnet_col = LibnetPrism_db.vnets
        vnet_col.remove({"network": nid})
        mongo_client.close()
    except Exception as e:
        error = "delete_network: lswitch-del %s" % (str(e))
        return jsonify({'Err': error})

    return jsonify({})


@app.route('/NetworkDriver.CreateEndpoint', methods=['POST'])
def network_driver_create_endpoint():
    if not request.data:
        abort(400)

    data = json.loads(request.data)
    nid = data.get("NetworkID", "")
    error = None
    if not nid:
        abort(400)

    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)

    interface = data.get("Interface", "")
    if not interface:
        error = "create_endpoint: no interfaces structure supplied by " \
                "libnetwork"
        return jsonify({'Err': error})

    ip_address_and_mask = interface.get("Address", "")
    if not ip_address_and_mask:
        error = "create_endpoint: ip address not provided by libnetwork"
        return jsonify({'Err': error})

    ip_address = ip_address_and_mask.rsplit('/', 1)[0]
    mac_address_input = interface.get("MacAddress", "")
    mac_address_output = ""

    vlan_tag = prism_get_vlan(nid)['vlan_tag']

    if not mac_address_input:
        mac_address = "02:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255),
                                                       random.randint(0, 255),
                                                       random.randint(0, 255),
                                                       random.randint(0, 255),
                                                       random.randint(0, 255))
    else:
        mac_address = mac_address_input

    # Only return a mac address if one did not come as request.
    mac_address_output = ""
    if not mac_address_input:
        mac_address_output = mac_address

    # TODO : port set vtag. vtag returned from PRISM using NID
    lport_db[eid] = {'mac_address': mac_address, 'ip_address': ip_address,
                     'error': error, 'vlan_tag': vlan_tag}
    return jsonify({"Interface": {"Address": "", "AddressIPv6": "",
                                  "MacAddress": mac_address_output }})

@app.route('/NetworkDriver.EndpointOperInfo', methods=['POST'])
def network_driver_endpoint_operational_info():
    if not request.data:
        abort(400)

    data = json.loads(request.data)

    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)

    try:
        (mac_address, ip_address, error) = get_logical_port_addresses(eid)
        if error:
            jsonify({'Err': error})
    except Exception as e:
        error = "show_endpoint: get Logical_port addresses. (%s)" % (str(e))
        return jsonify({'Err': error})

    veth_outside = eid[0:9]
    return jsonify({"Value": {"ip_address": ip_address,
                              "mac_address": mac_address,
                              "veth_outside": veth_outside }})

@app.route('/NetworkDriver.DeleteEndpoint', methods=['POST'])
def network_driver_delete_endpoint():
    if not request.data:
        abort(400)

    data = json.loads(request.data)

    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)

    try:
        # TODO : port dettach
        # eid is port name
        prism_delete_port(eid)
    except Exception as e:
        error = "delete_endpoint: lport-del %s" % (str(e))
        return jsonify({'Err': error})

    return jsonify({})

@app.route('/NetworkDriver.Join', methods=['POST'])
def network_driver_join():
    if not request.data:
        abort(400)

    data = json.loads(request.data)

    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)

    sboxkey = data.get("SandboxKey", "")
    if not sboxkey:
        abort(400)

    # sboxkey is of the form: /var/run/docker/netns/CONTAINER_ID
    vm_id = sboxkey.rsplit('/')[-1]

    try:
        #(mac_address, ip_address, error) = get_logical_port_addresses(eid)
        mac_address = lport_db[eid]['mac_address']
        ip_address = lport_db[eid]['ip_address']
        error = lport_db[eid]['error']
        vlan_tag = lport_db[eid]['vlan_tag']
        if error:
            jsonify({'Err': error})
    except Exception as e:
        error = "network_join: %s" % (str(e))
        return jsonify({'Err': error})

    #veth_outside = eid[0:15]
    #veth_inside = eid[0:13] + "_c"
    veth_outside = eid[0:9]
    veth_inside = eid[0:8] + "c"
    command = "ip link add %s type veth peer name %s" % (veth_inside, veth_outside)
    try:
        call_popen(shlex.split(command))
    except Exception as e:
        error = "network_join: failed to create veth pair (%s)" % (str(e))
        return jsonify({'Err': error})

    command = "ip link set dev %s address %s" \
              % (veth_inside, mac_address)

    try:
        call_popen(shlex.split(command))
    except Exception as e:
        error = "network_join: failed to set veth mac address (%s)" % (str(e))
        return jsonify({'Err': error})

    command = "ip link set %s up" % (veth_outside)

    try:
        call_popen(shlex.split(command))
    except Exception as e:
        error = "network_join: failed to up the veth interface (%s)" % (str(e))
        return jsonify({'Err': error})

    try:
        ovs_vsctl("add-port", CONF.default.DOCKER_BRIDGE, veth_outside)
        ovs_vsctl("set", "Port", veth_outside, "tag="+str(vlan_tag))
        ovs_vsctl("set", "interface", veth_outside,
                  "external_ids:attached-mac=" + mac_address,
                  "external_ids:iface-id=" + eid,
                  "external_ids:vm-id=" + vm_id,
                  "external_ids:iface-status=active")
    except Exception as e:
        error = "network_join: failed to create a port (%s)" % (str(e))
        return jsonify({'Err': error})

    return jsonify({"InterfaceName": {"SrcName": veth_inside,
                                      "DstPrefix": "eth"},
                    "Gateway": "",
                    "GatewayIPv6": ""})

@app.route('/NetworkDriver.Leave', methods=['POST'])
def network_driver_leave():
    if not request.data:
        abort(400)

    data = json.loads(request.data)

    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)

    veth_outside = eid[0:9]
    command = "ip link delete %s" % (veth_outside)
    try:
        call_popen(shlex.split(command))
    except Exception as e:
        error = "network_leave: failed to delete veth pair (%s)" % (str(e))
        return jsonify({'Err': error})

    try:
        ovs_vsctl("--if-exists", "del-port", veth_outside)
    except Exception as e:
        error = "network_leave: failed to delete port (%s)" % (str(e))
        return jsonify({'Err': error})

    return jsonify({})
