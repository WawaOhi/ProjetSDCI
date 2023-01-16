#!/usr/bin/python


from mininet import Containernet

# -->ajout docker aux adresses récupérées par init.sh


from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.tango import TangoLLCMEndpoint
import re

setLogLevel('info')

net = DCNetwork(monitor=False, enable_learning=True)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
server = net.addDocker('server', ip='10.0.0.1', dimage="node:container", environment={"iam": "Server"},
                       mem_limit='512m')
gi = net.addDocker('gi', ip='10.0.0.2', dimage="node:container", environment={"iam": "GatewayI"}, mem_limit='512m')
gf1 = net.addDocker('gf1', ip='10.0.0.3', dimage="node:container", environment={"iam": "GatewayF1"}, mem_limit='512m')
gf2 = net.addDocker('gf2', ip='10.0.0.4', dimage="node:container", environment={"iam": "GatewayF2"}, mem_limit='512m')
gf3 = net.addDocker('gf3', ip='10.0.0.5', dimage="node:container", environment={"iam": "GatewayF3"}, mem_limit='512m')
device1_1 = net.addDocker('device1_1', ip='10.0.0.6', dimage="node:container", environment={"iam": "Device1_1"},
                          mem_limit='512m')
device1_2 = net.addDocker('device1_2', ip='10.0.0.7', dimage="node:container", environment={"iam": "Device1_2"},
                          mem_limit='512m')
device1_3 = net.addDocker('device1_3', ip='10.0.0.8', dimage="node:container", environment={"iam": "Device1_3"},
                          mem_limit='512m')
device2_1 = net.addDocker('device2_1', ip='10.0.0.9', dimage="node:container", environment={"iam": "Device2_1"},
                          mem_limit='512m')
device3_1 = net.addDocker('device3_1', ip='10.0.0.10', dimage="node:container", environment={"iam": "Device3_1"},


                          mem_limit='512m')

#add datacenter
datacenter = net.addDatacenter("dc1")
#ajout  5GTANGO life cycle manager (optionnel)
llcm1 = TangoLLCMEndpoint("0.0.0.0", 5000, deploy_sap=False)
llcm1.connectDatacenter(dc1)
# run the dummy gatekeeper (in another thread, don't block)
llcm1.start()

# Fonction create_Device avec device1_1 premier device de la première gateway, device1_2 deuxième device de la première
# gateway etc
# def create_device(gta, n):
# separe = re.split('(\d+)',gta)
# for i in range(n):
#  nom = "Device" + separe[1] + (i+1)
#   ipaddress = '10.0.0.' + (6+i)
# y=i+1
#     = net.addDocker(nom, ip=ipaddress, dimage="node:container", environment={"iam":nom}, mem_limit='512m')
#   net.addLink(device, gta)


info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
s3 = net.addSwitch('s3')
info('*** Creating links\n')
net.addLink(server, s1)
net.addLink(gi, s1)
net.addLink(s1, s2)
net.addLink(s2, s3)
net.addLink(s3, s1)
net.addLink(s2, gf1)
net.addLink(s2, gf2)
net.addLink(s2, gf3)
net.addLink(device1_1, gf1)
net.addLink(device1_2, gf1)
net.addLink(device1_3, gf1)
net.addLink(device2_1, gf2)
net.addLink(device3_1, gf3)
net.addLink(dc1, s3) 

info('*** Starting network\n')

net.start()
net.CLI()
net.stop()

