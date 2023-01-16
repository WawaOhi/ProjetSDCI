#!/bin/sh 

# Retrieve the json and store it in a json file
curl http://172.17.0.2:3000/getConf/$iam | jq '.'> $iam.json

# Extraction des différents fields de notre fichier json 
localIp=`cat $iam.json | jq -r '.localIp'`
localPort=`cat $iam.json | jq -r '.localPort'`
localName=`cat $iam.json | jq -r '.localName'`
codeURL=`cat $iam.json | jq -r '.codeURL'`
remotePort=`cat $iam.json | jq -r '.remotePort'`
sendPeriod=`cat $iam.json | jq -r '.sendPeriod'`
remoteIp=`cat $iam.json | jq -r '.remoteIp'`
remoteName=`cat $iam.json | jq -r '.remoteName'`

#Type de composant utiisé. 
type=`cat $iam.json | jq -r '.type'`

#récupération du fichier js grace à un wget
wget $codeURL

#En fonction du type, on execute la commande appropriée
case $type in
    gateway)
        node gateway.js --local_ip $localIp --local_port $localPort --local_name $localName --remote_ip $remoteIp --remote_port $remotePort --remote_name $remoteName
        ;;
    server)
        node server.js --local_ip $localIp --local_port $localPort --local_name $localName
        ;;
    device)
        node device.js --local_ip $localIp --local_port $localPort --local_name $localName --remote_ip $remoteIp --remote_port $remotePort --remote_name $remoteName --send_period $sendPeriod
        ;;
    *)
        node application.js --remote_ip $localIp --remote_port $remotePort --device_name $localName --send_period $sendPeriod
        ;;
esac

