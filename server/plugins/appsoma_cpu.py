try:
	from ss_plugin import *
	import ministats

	def appsoma_cpu_collector():
		return ministats.stats()['cpu']

	collectors['appsoma_cpu'] = appsoma_cpu_collector
except Exception, e:
	print "Could not load appsoma_cpu.py: " + str(e)