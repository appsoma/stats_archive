from ss_triggers import *
from trigger_helper import *

def appsoma_disk_full():
	nodes = get_nodes()
	nodes_list = ["appsoma.com", "zabbix.appsoma.com"]
	for node in nodes:
		if node['name'] not in nodes_list:
			return

		appsoma_data = latest_node_data( node['id'], "Disk_Information", 600 )
		
		def check_full( data, name ):
			full = False
			for d in data:
				for disk in d['value']:
					if d['value'][disk]['percent'] > 90:
						full = disk
						break
			if full:
				make_alert( name + "-full-disk", full + " is over 90 percent full", 2 )

		check_full( appsoma_data, "appsoma.com" )

triggers['appsoma_disk_full'] = appsoma_disk_full