import requests
import json

class beem_agent():
    def __init__(self):        
        this.headers = {'Content-type': 'application/json'}

    
    def beem_post(self, url, data):
        data_json = json.dumps(data)
        try:
            response = requests.post(url, data=data_json, headers=this.headers)
            return response.json()
        except Exception:
            return {'message': 'fail'}

    def beem_acl(self):
        # TODO
    
    def beem_reboot(self):
        # TODO


def beem(params):
    """
    @brief      { slack client module }
    
    @param      params['action']                string: one of them (acl, reboot)
    @param      params['device']                string: device ip
    @param      params['acl_src_ip']            string: source ip
    @param      params['acl_src_netmask']       string: source netmask
    @param      params['acl_protocol']          string: protocol
    @param      params['acl_dst_ip']            string: destination ip  
    @param      params['acl_dst_netmask']       string: destination netmask 

    
    @return     { "message": "string" }
    """
    slack_token = params['token']
    sc = SlackClient(slack_token)
    sc.api_call(
	    "chat.postMessage",
	    #channel="#alert",
	    channel=params['channel'],
	    #text="Hello from Python! :tada:"
	    text=params['message']
    )
    return {"message": params['message']}
