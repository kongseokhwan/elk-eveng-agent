__author__ = 'kongseokhwan'
from prism.schemata import commons

RELEASE_POOL_SCHEMA = {
    u'links': [{
        u'method': u'POST',
        u'href': u'/IpamDriver.ReleasePool',
        u'description': u'Release an ip pool',
        u'rel': u'self',
        u'title': u'Release'
    }],
    u'title': u'Release an IP pool',
    u'required': [u'PoolID'],
    u'definitions': {u'commons': {}},
    u'$schema': u'http://json-schema.org/draft-04/hyper-schema',
    u'type': u'object',
    u'properties': {
        u'PoolID': {
            u'description': u'neutron ID of allocated subnetpool',
            u'$ref': u'#/definitions/commons/definitions/uuid'
        }
    }
}

RELEASE_POOL_SCHEMA[u'definitions'][u'commons'] = commons.COMMONS


