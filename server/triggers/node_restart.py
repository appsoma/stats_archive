from ss_triggers import *
from trigger_helper import *


def node_restart(cfg):
	nodes = get_nodes()
	for node in nodes:
		notes = latest_notes( node['id'], 600 )

		if len( notes ) == 0:
			return
			
		for nd in notes:
			note = nd['note']
			if "RESTART" in note:
				reason = note.lower()
				if "timeout" in reason or "error" in reason or "stop" in reason or "unknown" in reason:
					make_alert( node["name"] + "-node_restart", node["name"] + " restarted with reason: " + reason, 2 )	

triggers['node_restart'] = node_restart