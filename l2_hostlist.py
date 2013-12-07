from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr

log = core.getLogger()

class RegisterSwitch(object):
    def __init__ (self):
        core.openflow.addListeners(self)
        self.connections = set()
        self.hostlist = dict()
        def load_hostlist():
            f = open("hostlist.csv", "r")
            for line in f:
                s = line.split(",")
                self.hostlist[(s[0], s[1])] = int(s[2])
        load_hostlist()
        log.debug(self.hostlist)

    def installFlows(self):
        for conn in self.connections:
            log.debug(dpid_to_str(conn.dpid))
            msg = of.ofp_flow_mod(action=of.ofp_action_output(port=2),
                  match=of.ofp_match(dl_type=0x800, nw_dst="10.0.0.2"))
            conn.send(msg)
            msg = of.ofp_flow_mod(action=of.ofp_action_output(port=1),
                  match=of.ofp_match(dl_type=0x800, nw_dst="10.0.0.1"))
            conn.send(msg)
        log.debug("Flows installed")

    def _handle_ConnectionUp (self, event):
        self.connections.add(event.connection)
        self.installFlows()
        log.debug("Switch %s has come up.", dpid_to_str(event.dpid))
    def _handle_PacketIn (self, event):
        msg = of.ofp_packet_out(data = event.ofp)
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg)
        log.debug(event)

def launch (disable_flood = False):
    core.registerNew(RegisterSwitch)
    log.debug("Switch started.")

msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)

for connection in core.openflow.connections: # _connections.values() before betta
  connection.send(msg)
  log.debug("Clearing all flows from %s." % (dpidToStr(connection.dpid),))
