import requests

sdn_req_payload_1 = {
    "dpid": 2,
    "cookie": 0,
    "table_id": 0,
    "priority": 1111,
    "flags": 1,
    "match": {
        "nw_src": "10.0.0.3",
        "nw_dst": "10.0.0.2",
        "dl_type": 2048
    },
    "actions": [{"type": "SET_FIELD",
                 "field": "ipv4_dst",
                 "value": "10.0.0.21"},
                {"type": "OUTPUT",
                 "port": "NORMAL"}
                ]
}
# RETOUR
sdn_req_payload_2 = {
    "dpid": 2,
    "cookie": 0,
    "table_id": 0,
    "priority": 1111,
    "flags": 1,
    "match": {
        "nw_src": "10.0.0.21",
        "nw_dst": "10.0.0.3",
        "dl_type": 2048
    },
    "actions": [{"type": "SET_FIELD",
                 "field": "ipv4_src",
                 "value": "10.0.0.2"},
                {"type": "OUTPUT",
                 "port": "NORMAL"}
                ]
}
# ALLER
sdn_req_payload_3 = {
    "dpid": 2,
    "cookie": 0,
    "table_id": 0,
    "priority": 1111,
    "flags": 1,
    "match": {
        "nw_src": "10.0.0.4",
        "nw_dst": "10.0.0.2",
        "dl_type": 2048
    },
    "actions": [{"type": "SET_FIELD",
                 "field": "ipv4_dst",
                 "value": "10.0.0.21"},
                {"type": "OUTPUT",
                 "port": "NORMAL"}
                ]
}
# RETOUR
sdn_req_payload_4 = {
    "dpid": 2,
    "cookie": 0,
    "table_id": 0,
    "priority": 1111,
    "flags": 1,
    "match": {
        "nw_src": "10.0.0.21",
        "nw_dst": "10.0.0.4",
        "dl_type": 2048
    },
    "actions": [{"type": "SET_FIELD",
                 "field": "ipv4_src",
                 "value": "10.0.0.2"},
                {"type": "OUTPUT",
                 "port": "NORMAL"}
                ]
}

sdn_req_payload_5 = {
    "dpid": 2,
    "cookie": 0,
    "table_id": 0,
    "priority": 1111,
    "flags": 1,
    "match": {
        "nw_src": "10.0.0.5",
        "nw_dst": "10.0.0.21",
        "dl_type": 2048
    },
    "actions": [{"type": "SET_FIELD",
                 "field": "ipv4_dst",
                 "value": "10.0.0.21"},
                {"type": "OUTPUT",
                 "port": "NORMAL"}
                ]
}
sdn_req_payload_6 = {
    "dpid": 2,
    "cookie": 0,
    "table_id": 0,
    "priority": 1111,
    "flags": 1,
    "match": {
        "nw_src": "10.0.0.21",
        "nw_dst": "10.0.0.5",
        "dl_type": 2048
    },
    "actions": [{"type": "SET_FIELD",
                 "field": "ipv4_src",
                 "value": "10.0.0.2"},
                {"type": "OUTPUT",
                 "port": "NORMAL"}
                ]
}

url = 'http://localhost:8080/stats/flowentry/add'


def send_payload_to_sdn(payload):
    r = requests.post(url, payload)


def redirect_traffic():
    print('TODO Redirect Traffic')
    return 0


def undo_redirect_traffic():
    print('TODO Go back to normal traffic')
    return 0


response = requests.post('http://localhost:8080/stats/flowentry/add', headers=headers, data=data)
