import json


class ELK_Sflow_parser():
    def __init__(self, **kwargs):
        pass

    def elk_sflow_ip_dup_parser(data):
        docs = data
        buckets_list = docs["aggregations"]["time_range"]["buckets"]

        dup = False
        dup_ips = {}

        for bucket in buckets_list:
            src_ip_buckets = bucket["src_ip"]["buckets"]
            for src_ip_bucket in src_ip_buckets:
                src_ip = json.dump(src_ip_bucket["key"])
                dup_ips[src_ip] = []
                for src_mac_bucket in src_ip_bucket["src_mac"]["buckets"]:
                    dup_ips[src_ip].append(json.dump(src_mac_bucket["key"]))

        for k, v in dup_ips.items():
            if len(v) < 2: del dup_ips[k]
            # if len(dup_ip) == 1 :
            #    print dup_ip

        return dup_ips