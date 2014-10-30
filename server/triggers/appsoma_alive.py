from ss_triggers import *
from trigger_helper import *


def appsoma_alive(cfg):
	nodes = get_nodes()
	nodes_list = ["zabbix.appsoma.com"]
	for node in nodes:
		if node['name'] not in nodes_list:
			return

		appsoma_data = latest_node_data( node['id'], "Appsoma_Response_Time", 600 )
		docker1_data = latest_node_data( node['id'], "Docker_Registry_5000", 600 )
#		docker2_data = latest_node_data( node['id'], "Docker_Registry_5001", 600 )
		
		def check_alive( data, name ):
			alive = False
			for d in data:
				if d['value'] > 0:
					alive = True
					break
			if not alive:
				make_alert( name + "-alive", name + " hasn't responded for last 10 minutes", 2 )

		check_alive( appsoma_data, "appsoma.com" )
		check_alive( docker1_data, "docker-registry.appsoma.com:5000" )
#		check_alive( docker2_data, "docker-registry.appsoma.com:5001" )

triggers['appsoma_alive'] = appsoma_alive