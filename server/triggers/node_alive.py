from ss_triggers import *
from trigger_helper import *


def check_outage_close(node, time, server):
	last_outage = latest_node_outage(node)
	if last_outage is not None and last_outage['stop_time'] is None:
		print ("Outage over on node", node['name'], "@", time)
		stop_outage(last_outage['id'], node, time)
		report_outage(node['name'], last_outage['start_time'], time, server)


def check_outage_open(node, time):
	last_outage = latest_node_outage(node)
	if last_outage is None or last_outage['stop_time'] is not None:
		print ("Outage started on", node['name'], "@", time)
		start_outage(node, time)


def node_alive(cfg):
	nodes = get_nodes()
	nodes_list = ["node-0", "node-1", "node-2", "google-0", "google-1", "google-2", "google-3", "utexas1", "utexas2"]
	for node in nodes:
		node_data = latest_node_data(node['id'], "main_alive", 600)
		if len(node_data) == 0:
			#If we haven't seen anything in 2 weeks, don't alert
			if len(latest_node_data(node['id'], "main_alive", 1209600)) == 0:
				continue	
		alive = False
		try:
			for nd in node_data:
				if nd['value'] > 0:
					alive = True
					check_outage_close(node, nd['time'], cfg.get('appsoma_server', 'https://appsoma.com'))
					break
				else:
					check_outage_open(node, nd['time'])
					break
		except Exception as e:
			print("bad manage outage", e)

		if node['name'] in nodes_list and not alive:
			node_outage = latest_node_outage(node)
			
			if node_outage is not None:
				duration = nd['time'] - node_outage['start_time']
				mins = int(duration / 60)
				secs = duration % 60
				time = "%d minutes, %d seconds" % (mins, secs) if mins > 0 else "%d seconds" % secs
				make_alert(node["name"] + "-main_alive", node["name"] + " hasn't responded for " + time, 2)

triggers['node_alive'] = node_alive
