
import constants.elk_sflow_constants as sflow_const

IP_DUP_TEMPLATE = 
{
    "aggs": {
        "time_range": {
            "date_range": {
                "field": "@timestamp",
                "ranges": [
                    { "to": "now" },
                    { "from": "now" }
                ]
            },
            "aggs": {
            	sflow_const.SRC_IP_KEY: {
                	"terms" : { "field" : sflow_const.SRC_IP_FIELD},
                  	"aggs" : {
                    	"src_mac" : { "terms" : { "field" : sflow_const.SRC_MAC_FIELD } }
                  	}
              	}
            }
      	}
    }
}
