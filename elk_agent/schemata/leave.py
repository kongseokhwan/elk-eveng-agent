__author__ = 'kongseokhwan'

from prism.schemata import endpoint_delete


LEAVE_SCHEMA = endpoint_delete.ENDPOINT_DELETE_SCHEMA
LEAVE_SCHEMA[u'title'] = u'Leave endpoint'
LEAVE_SCHEMA[u'links'] = [{
    u'method': u'POST',
    u'href': u'/NetworkDriver.Leave',
    u'description': u'Unbinds the endpoint from the container.',
    u'rel': u'self',
    u'title': u'Leave'
}]
