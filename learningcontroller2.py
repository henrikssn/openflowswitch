# Tutorial Controller
# Starts as a hub, and your job is to turn this into a learning switch.

import logging

from nox.lib.core import *
import nox.lib.openflow as openflow
from nox.lib.packet.ethernet import ethernet
from nox.lib.packet.packet_utils import mac_to_str, mac_to_int

log = logging.getLogger('nox.coreapps.tutorial.pytutorial')


class pytutorial(Component):

    def __init__(self, ctxt):
        Component.__init__(self, ctxt)
        # Use this table to store MAC addresses in the format of your choice;
        # Functions already imported, including mac_to_str, and mac_to_int,
        # should prove useful for converting the byte array provided by NOX
        # for packet MAC destination fields.
        # This table is initialized to empty when your module starts up.
        self.mac_table = {} # key: MAC addr; value: port

    def learn_and_forward(self, dpid, inport, packet, buf, bufid):
        """Learn MAC src port mapping, then flood or send unicast."""
        
        # Create table for this switch (dpid) if none exist
	if not (dpid in self.mac_table):
		self.mac_table[dpid] = {}
	
	mac_to_port = self.mac_table[dpid]


	mac_to_port[mac_to_int(packet.src)] = inport
        if mac_to_int(packet.dst) in mac_to_port:
            	# Send unicast packet to known output port
            	#self.send_openflow(dpid, bufid, buf, mac_to_port[mac_to_int(packet.dst)], inport)
		log.debug("send to known port %s", mac_to_str(packet.dst))
		# Later, only after learning controller works: 
		# push down flow entry and remove the send_openflow command above.
        	attrs = {}
		attrs[core.IN_PORT] = inport
		attrs[core.DL_DST] = packet.dst
		actions = [[openflow.OFPAT_OUTPUT, [0, mac_to_port[mac_to_int(packet.dst)]]]]
		self.install_datapath_flow(dpid, attrs, 0, 0, actions, bufid, openflow.OFP_DEFAULT_PRIORITY, inport, packet)
        else:
            	#flood packet out everything but the input port
            	self.send_openflow(dpid, bufid, buf, openflow.OFPP_FLOOD, inport)
		log.debug("send to all ports")

    def packet_in_callback(self, dpid, inport, reason, len, bufid, packet):
        """Packet-in handler""" 
        if not packet.parsed:
            log.debug('Ignoring incomplete packet')
        else:
            self.learn_and_forward(dpid, inport, packet, packet.arr, bufid)    

        return CONTINUE

    def install(self):
        self.register_for_packet_in(self.packet_in_callback)
    
    def getInterface(self):
        return str(pytutorial)

def getFactory():
    class Factory:
        def instance(self, ctxt):
            return pytutorial(ctxt)

    return Factory()
