__author__ = 'kongseokhwan'
from prism.schemata import commons

REQUEST_ADDRESS_SCHEMA = {
    u'links': [{
        u'method': u'POST',
        u'href': u'/IpamDriver.RequestAddress',
        u'description': u'Allocate an ip addresses',
        u'rel': u'self',
        u'title': u'Create'
    }],
    u'title': u'Create an IP',
    u'required': [u'PoolID', u'Address', u'Options'],
    u'definitions': {u'commons': {}},
    u'$schema': u'http://json-schema.org/draft-04/hyper-schema',
    u'type': u'object',
    u'properties': {
        u'PoolID': {
            u'description': u'neutron uuid of allocated subnetpool',
            u'$ref': u'#/definitions/commons/definitions/uuid'
        },
        u'Address': {
            u'description': u'Prefered address in regular IP form.',
            u'example': u'10.0.0.1',
            u'$ref': u'#/definitions/commons/definitions/ipv4_or_ipv6'
        },
        u'Options': {
            u'type': [u'object', u'null'],
            u'description': u'Options',
            u'example': {}
        }
    }

}

REQUEST_ADDRESS_SCHEMA[u'definitions'][u'commons'] = commons.COMMONS
