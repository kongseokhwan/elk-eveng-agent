#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Routines for configuring prism
"""

import os

from oslo_config import cfg

from prism import i18n

_ = i18n._

core_opts = [
    cfg.StrOpt('pybasedir',
               default=os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../../')),
               help=_('Directory where prism python module is installed.')),
    cfg.StrOpt('bindir',
               default='$pybasedir/usr/libexec/prism',
               help=_('Directory for prism vif binding executables.')),
    cfg.StrOpt('prism_uri',
               default='http://127.0.0.1:2377',
               help=_('prism URL for accessing prism through json rpc.')),
    cfg.StrOpt('capability_scope',
               default='global',
               choices=['local', 'global'],
               help=_('prism plugin scope reported to libnetwork.')),
]
CONF = cfg.CONF
CONF.register_opts(core_opts)

