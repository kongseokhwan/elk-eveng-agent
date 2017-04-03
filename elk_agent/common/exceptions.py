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


class prismException(Exception):
    """Default prism exception"""


class BindingFailure(prismException):
    """Exception represents the binding is failed.

    This exception is thrown when the executable script for the binding is
    failed and prism can't proceed further.
    """


class DuplicatedResourceException(prismException):
    """Exception represents there're multiple resources for the ID.

    This exception is thrown when you query the Neutron resouce associated with
    the ID and you get multiple resources.
    """


class NoResourceException(prismException):
    """Exception represents there's no resource for the given query.

    This exception is thrown when you query the Neutron resource associated
    with the given query and you get none of them actually.
    """


class VethCreatationFailure(prismException):
    """Exception represents the veth pair creation is failed.

    This exception is thrown when the veth pair is not created appropriately
    and prism can't proceed the binding further.
    """
