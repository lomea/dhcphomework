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

from pydhcplib.dhcp_packet import *
from pydhcplib.dhcp_network import *


netopt = {'client_listen_port':"68",
           'server_listen_port':"67",
           'listen_address':"0.0.0.0"}

class Server(DhcpServer):
    def __init__(self, options):
        DhcpServer.__init__(self,options["listen_address"],
                            options["client_listen_port"],
                            options["server_listen_port"])
        
    def HandleDhcpDiscover(self, packet):
        print packet.str()
        
        packet.SetOption("op",[2])
        packet.SetOption("dhcp_message_type",[2])
        packet.SetOption("yiaddr",[192,168,1,1])
        packet.SetOption("router",ipv4("192.168.0.1").list()+[6,4,2,1])
        packet.SetOption("subnet_mask",[255,255,255,0])
        packet.SetOption("server_identifier",[192,168,1,1])

        self.SendDhcpPacketTo(packet,"255.255.255.255",68)
    
    def HandleDhcpRequest(self, packet):
        print packet.str()
    
        packet.SetOption("op",[2])
        packet.SetOption("dhcp_message_type",[5])
        
        self.SendDhcpPacketTo(packet,"255.255.255.255",68)
    
    def HandleDhcpDecline(self, packet):
        print packet.str()
    def HandleDhcpRelease(self, packet):
        print packet.str()
    def HandleDhcpInform(self, packet):
        print packet.str()


server = Server(netopt)

while True :
    server.GetNextDhcpPacket()
