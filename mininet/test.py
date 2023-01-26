#!/usr/bin/python

# ajout docker aux adresses recuperees par init.sh


#from mininet.node import Controller
#from mininet.cli import CLI
#from mininet.link import TCLink
from mininet.log import info, setLogLevel
import logging

from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.tango import TangoLLCMEndpoint
import re
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint

logging.basicConfig(level=logging.DEBUG)
setLogLevel('info')

logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('5gtango.llcm').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.helper').setLevel(logging.DEBUG)

def create_topology():
  net = DCNetwork(monitor=False, enable_learning=True)

  #add datacenter
  dc1 = net.addDatacenter("dc1")

  # add OpenStack-like APIs to the emulated DC
  api1 = OpenstackApiEndpoint("0.0.0.0", 6001)
  api1.connect_datacenter(dc1)
  api1.start()
  api1.connect_dc_network(net)

  # add the command line interface endpoint to the emulated DC (REST API)
  rapi1 = RestApiEndpoint("0.0.0.0", 5001)
  rapi1.connectDCNetwork(net)
  rapi1.connectDatacenter(dc1)
  rapi1.start()

  #ajout  5GTANGO life cycle manager (optionnel) 
  #llcm1 = TangoLLCMEndpoint("0.0.0.0", 5000, deploy_sap=False)
  #llcm1.connectDatacenter(dc1)
  # run the dummy gatekeeper (in another thread, don't block)
  #llcm1.start()

  info('*** Adding docker containers\n')
  server = net.addDocker('server', ip='10.0.0.1', dimage="node:container", environment={"iam": "Server"}, mem_limit='512m')
  gi = net.addDocker('gi', ip='10.0.0.2', dimage="node:container", environment={"iam": "GatewayI"}, mem_limit='512m')
  gf1 = net.addDocker('gf1', ip='10.0.0.3', dimage="node:container", environment={"iam": "GatewayF1"}, mem_limit='512m')
  gf2 = net.addDocker('gf2', ip='10.0.0.4', dimage="node:container", environment={"iam": "GatewayF2"}, mem_limit='512m')
  gf3 = net.addDocker('gf3', ip='10.0.0.5', dimage="node:container", environment={"iam": "GatewayF3"}, mem_limit='512m')
  device1_1 = net.addDocker('device1_1', ip='10.0.0.6', dimage="node:container", environment={"iam": "Device1_1"}, mem_limit='512m')
  device1_2 = net.addDocker('device1_2', ip='10.0.0.7', dimage="node:container", environment={"iam": "Device1_2"}, mem_limit='512m')
  device1_3 = net.addDocker('device1_3', ip='10.0.0.8', dimage="node:container", environment={"iam": "Device1_3"}, mem_limit='512m')
  device2_1 = net.addDocker('device2_1', ip='10.0.0.9', dimage="node:container", environment={"iam": "Device2_1"}, mem_limit='512m')
  device3_1 = net.addDocker('device3_1', ip='10.0.0.10', dimage="node:container", environment={"iam": "Device3_1"}, mem_limit='512m')



# Fonction create_Device avec device1_1 premier device de la premiere gateway, device1_2 deuxieme device de la premiere
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
  s4 = net.addSwitch('s4')
  s5 = net.addSwitch('s5')

  info('*** Creating links\n')
  net.addLink(server, s1)

  net.addLink(s1, s2)
  net.addLink(s2, gi)
  net.addLink(s2, dc1) 

  net.addLink(s2, s3)
  net.addLink(s2, s4)
  net.addLink(s2, s5)
  
  net.addLink(s3, gf1)
  net.addLink(s3, device1_1)
  net.addLink(s3, device1_2)
  net.addLink(s3, device1_3)
  
  net.addLink(s4, gf2)
  net.addLink(s4, device2_1)
  
  net.addLink(s5, gf3)
  net.addLink(s5, device3_1)

  info('*** Starting network\n')

  net.start()
  net.CLI()

  net.ping([GF1, GI])
  net.ping([GF2, GI])
  net.ping([GF3, GI])
  net.ping([Serv, GI])

  net.stop()


def main() :
  create_topology()


if __name__ == '__main__':
  main()
