curl -X POST -d '{
   	 "dpid": 2,
    	"cookie": 0,
    	"table_id": 0,
    	"priority": 1111,
    	"flags": 1,
    	"match":{
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

