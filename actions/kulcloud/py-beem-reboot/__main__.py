import requests
import json
from requests.auth import HTTPBasicAuth

# wsk -i action invoke beem --blocking --result --param device_name "se_prism" 
# --param controller "35.187.147.69:7171" 


def beem(params):
    """
    @brief      { acl api client module }
    
    @param      params['device_name']                string: one of them (acl, reboot)
    @param      params['controller']                string: one of them (acl, reboot)   

    """

    controller = params['controller']
    device_name = params['device_name']
    
    body = {        
    }

    try:
        r = requests.post("http://"+controller+"/1.0/"+device_name+"/system/reboot", 
            data=json.dumps(body), auth=HTTPBasicAuth(USER, PW))
    except
        RuntimeError as e:
        LOG.error("%s Controller Switch Reboot Error", e)
        return params

    return params
