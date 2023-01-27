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

#aller
curl -X POST -d '{
   	"dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
        "nw_src":"10.0.0.4",
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
		"nw_dst": "10.0.0.4",
        	"dl_type": 2048
    	},
   	"actions":[{"type": "SET_FIELD",
   	        "field": "ipv4_src",
   	        "value": "10.0.0.2"},
		{"type":"OUTPUT",
		"port":"NORMAL"}
    ]
 }' http://localhost:8080/stats/flowentry/add

 curl -X POST -d '{
   	"dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
        "nw_src":"10.0.0.5",
		"nw_dst": "10.0.0.21",
        	"dl_type": 2048
    	},
   	"actions":[{"type": "SET_FIELD",
   	        "field": "ipv4_dst",
   	        "value": "10.0.0.21"},
		{"type":"OUTPUT",
		"port":"NORMAL"}
    ]
 }' http://localhost:8080/stats/flowentry/add

  curl -X POST -d '{
   	"dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
        "nw_src":"10.0.0.21",
		"nw_dst": "10.0.0.5",
        	"dl_type": 2048
    	},
   	"actions":[{"type": "SET_FIELD",
   	        "field": "ipv4_src",
   	        "value": "10.0.0.2"},
		{"type":"OUTPUT",
		"port":"NORMAL"}
    ]
 }' http://localhost:8080/stats/flowentry/add


#how to differenciate gf1 / gf2 / gf3?? - is it possble to do it at the applicative layer
#coming from port 5030 = replace ip_src = ip_gf1
#coming from port 5031 = replace ip_src = ip_gf2
#coming from port 5032 = replace ip_src = ip_gf3

# make frames coming from vnf_ordo look like they're from Gf1/gf2/gf3
curl -X POST -d '{
   	 "dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
		"nw_src": "10.0.0.21",
		"in_port":5030,
        "dl_type": 2048
    	},
   	"actions":[{"type": "SET_FIELD",
   	        "field": "ipv4_src",
   	        "value": "10.0.0.3"},
		{"type":"OUTPUT",
		"port":"NORMAL"}
    ]
 }' http://localhost:8080/stats/flowentry/add


 curl -X POST -d '{
   	 "dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
		"nw_src": "10.0.0.21",
		"in_port":5031,
        "dl_type": 2048
    	},
   	"actions":[{"type": "SET_FIELD",
   	        "field": "ipv4_src",
   	        "value": "10.0.0.4"},
		{"type":"OUTPUT",
		"port":"NORMAL"}
    ]
 }' http://localhost:8080/stats/flowentry/add

 curl -X POST -d '{
   	 "dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
		"nw_src": "10.0.0.21",
		"in_port":5032
        "dl_type": 2048
    	},
   	"actions":[{"type": "SET_FIELD",
   	        "field": "ipv4_src",
   	        "value": "10.0.0.5"},
		{"type":"OUTPUT",
		"port":"NORMAL"}
    ]
 }' http://localhost:8080/stats/flowentry/add