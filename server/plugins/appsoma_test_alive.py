try:
	from ss_plugin import *
	import urllib2

	def appsoma_test_alive_collector():
		response = urllib2.urlopen('https://localhost:5001/test_alive')
		html = response.read()
		return 1 if (html == "1") else 0

	collectors['appsoma_test_alive'] = appsoma_test_alive_collector
except Exception, e:
	print "Error importing appsoma_test_alive.py: " + str(e)