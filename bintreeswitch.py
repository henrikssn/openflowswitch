from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr
import pox.openflow.discovery

log = core.getLogger()
pox.openflow.discovery.launch()

class RegisterSwitch(object):
    def __init__ (self):
        core.openflow.addListeners(self)
	core.openflow_discovery.addListenerByName("LinkEvent", self._handle_LinkEvent)
        self.connections = set()
        self.hostlist = dict()
        def load_hostlist():
	    f = open("hostlist.csv", "r")
	    count = 0
	    for line in f:
		count += 1
	    f.close()
            f = open("hostlist.csv", "r")
            for line in f:
                s = line.split(",")
                self.hostlist[(s[0], int(s[1])-count)] = int(s[2])
	    f.close()
        load_hostlist()
        log.debug(self.hostlist)

    def installFlows(self):	
	# delete all flows
	msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
	for conn in self.connections:
	    conn.send(msg)

	# for all host, ensure that every switch can forward packet to the host
	for host in self.hostlist:
	    # install flow on the switch that is connected to the host
	    self.setFlow(host[0], self.hostlist[host], host[1])
	
	    # get a list of all switches, flag is set to 0=not visited
	    # start at the switch that is connected to the host, set it to 1=last visited
	    # search all neighbours of the last visited nodes
	    # pick a random path, install flow on the neighbour nodes
	    # last visited nodes are set to 2=finished
	    # neighbour nodes are set to 1=last visited
	    # continue
	    switches = self.getSwitchList()
	    switches[host[1]] = 1
	    is_finished = False

	    log.debug(core.openflow_discovery.adjacency)

	    while not is_finished:
		# search neighbours of last visited nodes
		newlinks = dict()
		for s in switches:
		    if switches[s] == 0:
			log.debug("Switch in state 0: "+str(s))
			for l in core.openflow_discovery.adjacency:
			    if l.dpid1 == s and switches[l.dpid2] == 1:
				if not s in newlinks:
				    newlinks[s] = []
				newlinks[s].append(l)
		# set all last visited nodes to finished
		for s in switches:
		    if switches[s] == 1:
			switches[s] = 2
		# check if there is a new neighbour
		if len(newlinks) == 0:
		    is_finished = True
		# establish flows, set switches to last visited
		for n in newlinks:
		    # pick first link, change this to random later
		    self.setFlow(host[0], newlinks[n][0].port1, n)
		    switches[n] = 1
		log.debug("While: " + str(switches))
        log.debug("Flows installed")

    def setFlow(self, ip, outport, dpid):
	msg = of.ofp_flow_mod(action=of.ofp_action_output(port=outport),match=of.ofp_match(dl_type=0x800,nw_dst=ip))		
	self.getConnection(dpid).send(msg)
	log.debug("Install flow: "+ip+" on switch"+str(dpid)+" on port "+str(outport))

    def getSwitchList(self):
	switches = dict()
	for conn in self.connections:
	    switches[conn.dpid] = 0
	return switches

    def getConnection(self, dpid):
	for conn in self.connections:
	    if dpid == conn.dpid:
		return conn
	log.debug("Connection with dpid "+str(dpid)+" not found!")
	raise Exception("No connection with dpid "+str(dpid))

    def _handle_ConnectionUp (self, event):
        self.connections.add(event.connection)
        #self.installFlows()
        log.debug("Switch %s has come up.", dpid_to_str(event.dpid))

    def _handle_PacketIn (self, event):
	msg = of.ofp_packet_out(data = event.ofp)
        #msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg)
        log.debug(event)

    def _handle_LinkEvent (self, event):
	self.installFlows()
	log.debug("Handle LinkEvent")

def launch (disable_flood = False):
    core.registerNew(RegisterSwitch)
    log.debug("Switch started.")

msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)

for connection in core.openflow.connections: # _connections.values() before betta
  connection.send(msg)
  log.debug("Clearing all flows from %s." % (dpidToStr(connection.dpid),))
