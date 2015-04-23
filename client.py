#!/usr/bin/python
#
# pydhcplib
# Copyright (C) 2008 Mathieu Ignacio -- mignacio@april.org
#
# This file is part of pydhcplib.
# Pydhcplib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import argparse, socket
import pydhcplib
import random

from pydhcplib.dhcp_file_io import *
from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *
from pydhcplib.type_strlist import strlist
from pydhcplib.type_ipv4 import ipv4
from uuid import getnode as get_mac

netopt = {'client_listen_port':68,
           'server_listen_port':67,
           'listen_address':"0.0.0.0"}

class Client(DhcpClient):
    def __init__(self, options):
        DhcpClient.__init__(self,options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"])
        
    def HandleDhcpOffer(self, packet):
        print packet.str()
    
        packet.SetOption("op",[1])
        packet.SetOption("dhcp_message_type",[3])
        
        self.SendDhcpPacketTo(packet,"255.255.255.255",67)
    
    def HandleDhcpAck(self, packet):
        print packet.str()
    
        exit()
    def HandleDhcpNack(self, packet):
        print packet.str()        

client = Client(netopt)
# Use BindToAddress if you want to emit/listen to an internet address (like 192.168.1.1)
# or BindToDevice if you want to emit/listen to a network device (like eth0)
client.BindToAddress()
#client.BindToDevice()

mac = str(hex(get_mac()))[2:]
mac = mac[:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]
decxid = random.randint(0,0xffffffff)
xid = []
for i in xrange(4):
    xid.insert(0, decxid & 0xff)
    decxid = decxid >> 8

packet = DhcpPacket()
packet.SetOption("op",[1])
packet.SetOption("dhcp_message_type",[1])
packet.SetOption("xid",xid)
packet.SetOption('chaddr',hwmac(mac).list()+ [0] * 10)

client.SendDhcpPacketTo(packet,"255.255.255.255",67)

while True :
    client.GetNextDhcpPacket()
