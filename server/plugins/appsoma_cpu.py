try:
	from ss_plugin import *
	import ministats
	import logging

	def appsoma_cpu_collector():
		try:
			return ministats.stats()['cpu']
		except Exception as e:
			logging.error( "Error using ministats to get cpu" )
		return None

	collectors['appsoma_cpu'] = appsoma_cpu_collector
except Exception, e:
	print "Could not load appsoma_cpu.py: " + str(e)