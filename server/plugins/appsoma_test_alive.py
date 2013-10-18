try:
	from ss_plugin import *
	import urllib2

	def appsoma_test_alive_collector():
		try:
			with open( "appsoma.base_port" ) as f:
				port = int(f.read()) + 1
			response = urllib2.urlopen('https://localhost:' + str(port) + '/test_alive')
			html = response.read()
			return 1 if (html == "1") else 0
		except Exception as e:
			return 0

	collectors['appsoma_test_alive'] = appsoma_test_alive_collector
except Exception, e:
	print "Error importing appsoma_test_alive.py: " + str(e)