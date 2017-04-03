#!/bin/bash
curl -d '{"nested_net":'$1', "gw_ip":'$2', "action":'$3'}' -H "Content-Type: application/json" http://127.0.0.1:8182/v1.0/k8s/route
