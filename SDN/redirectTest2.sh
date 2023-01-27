#!/bin/bash

#reroute frames coming from gf1 / gf2 / gf3 to vnf_adapt
#aller
curl -X POST -d '{
   	"dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
        "nw_src":"10.0.0.3",
		"nw_dst": "10.0.0.2",
        	"dl_type": 2048
    	},
   	"actions":[{"type": "SET_FIELD",
   	        "field": "ipv4_dst",
   	        "value": "10.0.0.21"},
		{"type":"OUTPUT",
		"port":"NORMAL"}
    ]
 }' http://localhost:8080/stats/flowentry/add
#retour
 curl -X POST -d '{
   	"dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
        "nw_src":"10.0.0.21",
		"nw_dst": "10.0.0.3",
        	"dl_type": 2048
    	},
   	"actions":[{"type": "SET_FIELD",
   	        "field": "ipv4_src",
   	        "value": "10.0.0.2"},
		{"type":"OUTPUT",
		"port":"NORMAL"}
    ]
 }' http://localhost:8080/stats/flowentry/add