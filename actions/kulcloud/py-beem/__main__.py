import requests
import json
from requests.auth import HTTPBasicAuth

def beem(params):
    """
    @brief      { acl api client module }
    
    @param      params['device_name']                string: one of them (acl, reboot)
    @param      params['acl_number']                string: one of them (acl, reboot)
    @param      params['match_order']                string: device ip
    @param      params['src_host']            string: source ip
    @param      params['src_wildcard']       string: source netmask
    @param      params['protocol']          string: protocol
    @param      params['dst_host']            string: destination ip  
    @param      params['dst_wildcard']       string: destination netmask 

    
    @return     { "message": "string" }
    """

    controller = params['controller']
    device_name = params['device_name']
    acl_number = params['acl_number']
    match_order = params['match_order']
    src_host = params['src_host']
    src_wildcard = params['src_wildcard']
    protocol = params['protocol']
    dst_host = params['dst_host']
    dst_wildcard = params['dst_wildcard']     

    body = {
        "acl_number": acl_number,
        "match_order": match_order,
        "src_host": src_host,
        "src_wildcard": src_wildcard,
        "protocol": protocol,
        "dst_host": dst_host,
        "dst_wildcard": dst_wildcard
    }

    try:
        r = requests.post("http://"+controller+"/1.0/"+device_name+"/qos/ipv4", 
            data=json.dumps(body), auth=HTTPBasicAuth(USER, PW))
    except
        RuntimeError as e:
        LOG.error("%s SMTP Agent terminated!", e)
        return {
            "acl_number": acl_number,
            "match_order": match_order,
            "src_host": src_host,
            "src_wildcard": src_wildcard,
            "protocol": protocol,
            "dst_host": dst_host,
            "dst_wildcard": dst_wildcard,
            "message": "ACL Send Error"
        }

    return {
            "acl_number": acl_number,
            "match_order": match_order,
            "src_host": src_host,
            "src_wildcard": src_wildcard,
            "protocol": protocol,
            "dst_host": dst_host,
            "dst_wildcard": dst_wildcard,
            "message": "ACL Send Suceess"
        }
