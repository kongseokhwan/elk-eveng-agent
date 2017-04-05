
import elk_sflow_constants 

IP_DUP_SCHEMA = 
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

