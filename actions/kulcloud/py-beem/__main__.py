import requests
import json
from requests.auth import HTTPBasicAuth

# wsk -i action invoke beem --blocking --result --param device_name "se_prism" 
# --param controller "35.187.147.69:7171" --param acl_number "11" --param match_order "deny" --param src_host "1.0.0.11" 
# --param src_mask "0.0.0.255" --param protocol "ip" --param dst_host "" --param dst_mask ""


def beem(params):
    """
    @brief      { acl api client module }
    
    @param      params['device_name']                string: one of them (acl, reboot)
    @param      params['acl_number']                string: one of them (acl, reboot)
    @param      params['match_order']                string: device ip
    @param      params['src_host']            string: source ip
    @param      params['src_mask']       string: source netmask
    @param      params['protocol']          string: protocol
    @param      params['dst_host']            string: destination ip  
    @param      params['dst_mask']       string: destination netmask 

    
    @return     { "message": "string" }
    """

    controller = params['controller']
    device_name = params['device_name']
    acl_number = params['acl_number']
    match_order = params['match_order']
    src_host = params['src_host']
    src_wildcard = params['src_mask']
    protocol = params['protocol']
    dst_host = params['dst_host']
    dst_wildcard = params['dst_mask']     

    body = {
        "acl_number": acl_number,
        "match_order": match_order,
        "src_host": src_host,
        "src_mask": src_wildcard,
        "protocol": protocol,
        "dst_host": dst_host,
        "dst_mask": dst_wildcard
    }

    try:
        r = requests.post("http://"+controller+"/1.0/"+device_name+"/qos/ipv4", 
            data=json.dumps(body), auth=HTTPBasicAuth(USER, PW))
    except
        RuntimeError as e:
        LOG.error("%s SMTP Agent terminated!", e)
        return params

    return params
