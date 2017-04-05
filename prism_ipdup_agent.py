__author__ = 'kongseokhwan'

import iptc
from common import base_polling
import time
from oslo_log import log as logging
from oslo_config import cfg
import util
#import mlapi
import sys
import signal

from common import elk_api_body as elk_data
from common.elk_sflow_parser import ELK_Sflow_parser as elk_sflow_p

from notifier.openwhisk_notifier import OPENWHISK_notifier
import elasticsearch


LOG = logging.getLogger(__name__)

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
        data = elk_data.IP_DUP_SCHEMA
        docs = es_client.search(self.sflow_index, self.sflow_type, data)

        dup_ips = elk_sflow_p.elk_sflow_ip_dup_parser(docs)

        if len(dup_ips) > 0 : 
            #OPENWHISK_notifier.ip_dup_notify(dup_ips)
            print (dup_ips)
            LOG.error("IP_DUPLICATION : %s", dup_ips)

    def agent_loop(self, polling_manager=None):
        polling_manager = base_polling.BasePollingManager()
        sync = True
        while self.run_daemon_loop:
            start = time.time()
            LOG.debug("PRISM IPdup_check_agent_loop - iteration:%d started",
                      self.iter_num)
            self.ip_dup_check()
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