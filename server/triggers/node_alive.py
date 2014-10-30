from ss_triggers import *
from trigger_helper import *


def check_outage_close(node, time, server):
	last_outage = latest_node_outage(node)
	if last_outage is not None and last_outage['stop_time'] is None:
		print ("Outage over", last_outage['id'])
		stop_outage(last_outage['id'], node, time)
		report_outage(node['name'], last_outage['start_time'], time, server)


def check_outage_open(node, time):
	last_outage = latest_node_outage(node)
	if last_outage is None or last_outage['stop_time'] is not None:
		print ("Outage started")
		start_outage(node, time)


def node_alive(cfg):
	print ("Check alive")
	nodes = get_nodes()
	nodes_list = ["node-0", "node-1", "node-2", "google-0", "google-1", "google-2", "google-3", "utexas1", "utexas2"]
	for node in nodes:
		node_outage = latest_node_outage(node)
		if node_outage is not None and 'stop_time' is None:
			window = 20
		else:
			window = 120
		node_data = latest_node_data(node['id'], "main_alive", window)
		if len(node_data) == 0:
			#If we haven't seen anything in 2 weeks, don't alert
			if len(latest_node_data(node['id'], "main_alive", 1209600)) == 0:
				return
		alive = False
		for nd in node_data:
			if nd['value'] > 0:
				alive = True
				check_outage_close(node, nd['time'], cfg.get('appsoma_server', 'https://appsoma.com'))
				break
			else:
				check_outage_open(node, nd['time'])
		if node['name'] not in nodes_list:
			return
		elif not alive:
			make_alert(node["name"] + "-main_alive", node["name"] + " hasn't responded for last 10 minutes", 2)

triggers['node_alive'] = node_alive