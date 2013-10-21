try:
	from ss_plugin import *
	import ministats
	import logging

	def appsoma_disk_collector():
		try:
			stats = ministats.stats()
			return (stats['disk_total'] - stats['disk_used']) / (1024*1024)
		except Exception as e:
			logging.error( "Error using ministats to get disk" )
		return None

	collectors['appsoma_disk'] = appsoma_disk_collector
except Exception, e:
	print "Could not load appsoma_disk.py: " + str(e)