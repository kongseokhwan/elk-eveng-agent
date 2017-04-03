#!/usr/bin/env bash
#
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

ELKAGENT_HOME=${ELKAGENT_HOME:-.}
ELKAGENT_JSON_FILENAME=ELKAGENT.json
ELKAGENT_DEFAULT_JSON=${ELKAGENT_HOME}/etc/${ELKAGENT_JSON_FILENAME}
# See libnetwork's plugin discovery mechanism:
#   https://github.com/docker/docker/blob/c4d45b6a29a91f2fb5d7a51ac36572f2a9b295c6/docs/extend/plugin_api.md#plugin-discovery
ELKAGENT_JSON_DIR=${ELKAGENT_JSON_DIR:-/usr/lib/docker/plugins/ELKAGENT}
ELKAGENT_JSON=${ELKAGENT_JSON_DIR}/${ELKAGENT_JSON_FILENAME}

if [[ ! -d "${ELKAGENT_JSON_DIR}" ]]; then
    echo -n "${ELKAGENT_JSON_DIR} directory is missing. Creating it... "
    sudo mkdir -p ${ELKAGENT_JSON_DIR}
    echo "Done"
fi

if [[ ! -f "${ELKAGENT_JSON}" ]]; then
    echo -n "${ELKAGENT_JSON} is missing. Copyting the default one... "
    sudo cp ${ELKAGENT_DEFAULT_JSON} ${ELKAGENT_JSON}
    echo "Done"
fi

PYTHONPATH=${ELKAGENT_HOME} python ${ELKAGENT_HOME}/scripts/run_server.py
S