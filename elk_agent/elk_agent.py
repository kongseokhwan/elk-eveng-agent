__author__ = 'kongseokhwan'

import argparse
import ast
import atexit
import json
import os
import random
import re
import shlex
import subprocess
import time
import util
import sys
import signal
import requests
import json
import json
import elasticsearch
from datetime import datetime

from common import base_polling
from oslo_log import log as logging
from oslo_config import cfg


LOG = logging.getLogger(__name__)
DOCKER_OPTS = "DOCKER_OPTS=\"--mtu=8951 --bip=%s/24\""
SHELL_EXTRACT_IP = "ifconfig %s | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"

class ELKAgent():
    def __init__(self, CONF):
        self.conf = CONF
        self.polling_interval = self.conf.default.polling_interval

        self.sflow_index = self.conf.default.sflow_index
        self.sflow_type = self.conf.default.sflow_type
        self.elk_addr = self.conf.default.elk_addr

        self.iter_num = 0
        self.run_daemon_loop = True

    def ip_dup_check():
        es_client = elasticsearch.Elasticsearch(self.elk_addr)
        docs = es_client.search(self.sflow_index, self.sflow_type, data)
        buckets_list = docs["aggregations"]["time_range"]["buckets"]

        dup = False
        dup_ips = {}

        for bucket in buckets_list :
            src_ip_buckets = bucket["src_ip"]["buckets"]
            for src_ip_bucket in src_ip_buckets :
                src_ip = dump(src_ip_bucket["key"])
                dup_ips[src_ip] = []
                for src_mac_bucket in  src_ip_bucket["src_mac"]["buckets"]:
                    dup_ips[src_ip].append(dump(src_mac_bucket["key"]))

        for k,v in dup_ips.items() :
            if len(v) < 2 : del dup_ips[k]
            #if len(dup_ip) == 1 :
            #    print dup_ip

        print dup_ips       


    def call_popen(self, cmd):
        child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output = child.communicate()
        if child.returncode:
            raise RuntimeError("Fatal error executing %s" % (cmd))
        if len(output) == 0 or output[0] == None:
            output = ""
        else:
            output = output[0].strip()
        return output

    def call_prog(self, prog, args_list):
        cmd = [prog, "--timeout=5", "-vconsole:off"] + args_list
        return self.call_popen(cmd)

    def agent_loop(self, polling_manager=None):
        polling_manager = base_polling.BasePollingManager()
        while self.run_daemon_loop:
            start = time.time()
            LOG.debug("PRISM Iptables slave_agent_loop - iteration:%d started",
                      self.iter_num)

            self.loop_count_and_wait(start)


    def loop_count_and_wait(self, start_time):
        # sleep till end of polling interval
        elapsed = time.time() - start_time

        if elapsed < self.polling_interval:
            time.sleep(self.polling_interval - elapsed)

        self.iter_num = self.iter_num + 1

    def daemon_loop(self):
        self.agent_loop()
        
    def _handle_sigterm(self):
        self.run_daemon_loop = False

def main():
    # Configuration Mapper
    opt_default_group = cfg.OptGroup(name='default', title='A default informations')
    default_opts = [
        cfg.IntOpt('polling_interval', default='60',
                    help=('Define Agents polling interval')),
        cfg.StrOpt('sflow_index', default='sflow-*',
                    help=('Define Elastic Search Index Name')),
        cfg.StrOpt('sflow_type', default='logs',
                    help=('Define Elastic Search Type Name')),
        cfg.StrOpt('elk_addr', default='10.1.190.31:9200',
                    help=('Define Elastic Search Engine IP Address'))       
    ]
    CONF = cfg.CONF
    CONF.register_group(opt_default_group)
    CONF.register_opts(default_opts, opt_default_group)
    CONF(default_config_files=['elk_agent.conf'])

    try:
        # Regsiter Agent
        agent = ELKAgent(CONF)
    except RuntimeError as e:
        LOG.error("%s PRISM ELK Agent terminated!", e)
        sys.exit(1)

    # Register SIGTERM action
    signal.signal(signal.SIGTERM, agent._handle_sigterm)

    # Start everything.
    agent.daemon_loop()

if __name__ == '__main__':
    main()