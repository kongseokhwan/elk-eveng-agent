import sys
from slackclient import SlackClient

def slack(params):
    #slack_token = 'xoxb-172489925216-RKpT9uxHd3zaplQkIwdkn4YU'
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
