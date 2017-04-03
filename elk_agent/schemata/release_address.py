__author__ = 'kongseokhwan'

from prism.schemata import commons

RELEASE_ADDRESS_SCHEMA = {
    u'links': [{
        u'method': u'POST',
        u'href': u'/IpamDriver.ReleaseAddress',
        u'description': u'Release an ip address',
        u'rel': u'self',
        u'title': u'Release'
    }],
    u'title': u'Release an IP',
    u'required': [u'PoolID', u'Address'],
    u'definitions': {u'commons': {}},
    u'$schema': u'http://json-schema.org/draft-04/hyper-schema',
    u'type': u'object',
    u'properties': {
        u'PoolID': {
            u'description': u'neutron uuid of allocated subnetpool',
            u'$ref': u'#/definitions/commons/definitions/uuid'
        },
        u'Address': {
            u'description': u'Address in IP(v4 or v6) form',
            u'$ref': u'#/definitions/commons/definitions/ipv4_or_ipv6'
        }
    }

}

RELEASE_ADDRESS_SCHEMA[u'definitions'][u'commons'] = commons.COMMONS
