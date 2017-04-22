import triggers.common.Openwhisk.schema.EVENT_URL
import json
import schema.ELK_EVENT_CONSTANTS as ELK_EVENT_CONSTANTS


class elk_event_mapper():
    def __init__(self):
        self.make_event_map_table()

    def make_event_map_table(self, event):
        self.switcher = {
            ELK_EVENT_CONSTANTS.SWITCH_CONN_EVENT: self._switch_conn_event,
            ELK_EVENT_CONSTANTS.SWITCH_DISCONN_EVENT: self._switch_disconn_event,
            ELK_EVENT_CONSTANTS.PORT_CONN_EVENT: self._port_conn_event,
            ELK_EVENT_CONSTANTS.PORT_DISCONN_EVENT: self._port_disconn_event,
            ELK_EVENT_CONSTANTS.IP_DUP_EVENT: self._ip_dup_event,
            ELK_EVENT_CONSTANTS.TRAFFIC_OVERSUBSCRIPTION_EVENT: self._traffic_oversubscription_event,
            ELK_EVENT_CONSTANTS.TRAFFIC_DDOS_ATTACK_EVENT: self._ddos_attach_event
        }

    def make_elk_msg(self, event, msg):
        func = self.switcher.get(event)
        message = func(msg)
        return json.dumps(message)

    def _switch_conn_event(self, msg):
        data = {"event_type": "SWITCH_CONN_EVENT",
                "message": msg}
        return data

    def _switch_disconn_event(self, msg):
        data = {"event_type": "SWITCH_DISCONN_EVENT",
                "message": msg}
        return data

    def _port_conn_event(self, msg):
        data = {"event_type": "PORT_CONN_EVENT",
                "message": msg}
        return data

    def _port_disconn_event(self, msg):
        data = {"event_type": "PORT_DISCONN_EVENT",
                "message": msg}
        return data

    def _ip_dup_event(self, msg):
        data = {"event_type": "IP_DUP_EVENT",
                "message": msg}
        return data

    def _traffic_oversubscription_event(self, msg):
        data = {"event_type": "TRAFFIC_OVERSUBSCRIPTION_EVENT",
                "message": msg}
        return data

    def _ddos_attach_event(self, msg):
        data = {"event_type": "TRAFFIC_DDOS_ATTACK_EVENT",
                "message": msg}
        return data
