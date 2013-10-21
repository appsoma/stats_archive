try:
	from ss_plugin import *
	import ministats
	import logging

	def appsoma_memory_collector():
		try:
			stats = ministats.stats()
			return (stats['mem_total'] - stats['mem_used']) / (1024*1024)
		except Exception as e:
			logging.error( "Error using ministats to get memory" )
		return None

	collectors['appsoma_memory'] = appsoma_memory_collector
except Exception, e:
	print "Could not load appsoma_memory.py: " + str(e)