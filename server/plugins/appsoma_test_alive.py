try:
	from ss_plugin import *
	import urllib2
	import base64
	import json
	#ACB: I'm importing the module in this way, because it can cause name problems with the websocket.py module used by the appsoma node
	import imp
	websocket = imp.load_source("websocket","/usr/local/lib/python2.7/dist-packages/websocket.py")

	def appsoma_test_alive_collector():
		try:
			with open( "appsoma.base_port" ) as f:
				port = int(f.read()) + 1
			
			#ACB: Using websockets to check if it's alive
			ws = websocket.create_connection("wss://localhost:" + str(port-1), header=[ "Sec-WebSocket-Protocol: base64" ])
			if ws.send(base64.b64encode(json.dumps({ 'command':'rpc_alive' }))) <= 0:
				return 0
			recv = json.loads(base64.b64decode(ws.recv()))
			return 1 if (recv["command"] == "rpc_alive" and "error" not in recv) else 0
			'''response = urllib2.urlopen('https://localhost:' + str(port) + '/test_alive')
			html = response.read()
			return 1 if (html == "1") else 0'''
			
		except Exception as e:
			return 0

	collectors['appsoma_test_alive'] = appsoma_test_alive_collector
except Exception, e:
	print "Error importing appsoma_test_alive.py: " + str(e)
