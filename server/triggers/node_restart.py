from ss_triggers import *
from trigger_helper import *

def node_restart():
	nodes = get_nodes()
	for node in nodes:
		notes = latest_notes( node['id'], 600 )

		if len( notes ) == 0:
			return
			
		for nd in node_data:
			note = nd['note']
			if "RESTART" in note:
				reason = note.split( ": " )[1].lower()
				if reason == "timeout" or reason == "error" or reason == "stop" or reason == "unknown":
					make_alert( node["name"] + "-node_restart", node["name"] + " restarted with reason: " + reason, 2 )	

triggers['node_restart'] = node_restart