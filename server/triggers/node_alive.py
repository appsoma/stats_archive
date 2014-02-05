from ss_triggers import *
from trigger_helper import *

def node_alive():
	nodes = get_nodes()
	nodes_list = ["node-0", "node-1", "node-2", "utexas1", "utexas2", "einstein", "sidl"]
	for node in nodes:
		if node['name'] not in nodes_list:
			return

		node_data = latest_node_data( node['id'], "main_alive", 600 )

		#DHW Feb 5 2014. I commented this out so that we get alerts when there are no data at all
		#if len( node_data ) == 0:
		#	return
			
		alive = False
		for nd in node_data:
			if nd['value'] > 0:
				alive = True
				break

		if not alive:
			make_alert( node["name"] + "-main_alive", node["name"] + " hasn't responded for last 10 minutes", 2 )

triggers['node_alive'] = node_alive