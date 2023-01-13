#!/bin/sh 

if [ -z "$1" ]; then 
	echo "Erreur : aucun nom de fichier n'à été donné en entrée."
	exit 1
fi

# Retrieve the json and store it in a json file
curl lelienversleserver/$iam> $iam.json


case $iam in 
	"Server")
		# Extraction des différents fields de notre fichier json
		localPort =$(jq -r '.localPort' $iam.json)
		localName =$(jq -r '.localName' $iam.json)
		codeURL =$(jq -r '.codeURL' $iam.json)
		export localPort
		export localName
		export codeURL
		;;
	"Application")
		remotePort =$(jq -r '.remotePort' $iam.json)
		codeURL =$(jq -r '.codeURL' $iam.json)
		deviceName =$(jq -r '.deviceName' $iam.json)
		sendPeriod =$(jq -r '.sendPeriod' $iam.json)
		export remotePort
		export codeURL
		export deviceName
		export sendPeriod
		;;
	"Device")
		localPort =$(jq -r '.localPort' $iam.json)
                localName =$(jq -r '.localName' $iam.json)
                remoteIp =$(jq -r '.remoteIp' $iam.json)
                remotePort =$(jq -r '.remotePort' $iam.json)
		remoteName =$(jq -r '.remoteName' $iam.json)
                codeURL =$(jq -r '.codeURL' $iam.json)
		sendPeriod =$(jq -r '.sendPeriod' $iam.json)
		export localPort
		export localName
		export remoteIp
		export remotePort
		export remoteName
		export codeURL
		export sendPeriod
		;;
	*)
		# Extraction des différents fields de notre fichier json
                localPort =$(jq -r '.localPort' $iam.json)
                localName =$(jq -r '.localName' $iam.json)
                remoteIp =$(jq -r '.remoteIp' $iam.json)
		remotePort =$(jq -r '.remotePort' $iam.json)
                remoteName =$(jq -r '.remoteName' $iam.json)
                codeURL =$(jq -r '.codeURL' $iam.json)
		export localPort
		export localName
		export remoteIp
		export remotePort
		export remoteName
		export sendPeriod
		;;
esac

