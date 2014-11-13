try:
	from ss_plugin import *
	import urllib2
	import base64
	import json
	import imp
	import websocket_client

	def appsoma_test_alive_collector():
		try:
			with open( "appsoma.port" ) as f:
				port = int(f.read()) + 1
			
			#ACB: Using websockets to check if it's alive
			try:
				ws = websocket_client.create_connection("wss://localhost:" + str(port-1), timeout=2, header=[ "Sec-WebSocket-Protocol: base64" ])
			except websocket_client.WebSocketTimeoutException:
				return 0
			if ws.send(base64.b64encode(json.dumps({ 'command':'rpc_alive' }))) <= 0:
				return 0
			recv = json.loads(base64.b64decode(ws.recv()))
			return 1 if (recv["command"] == "rpc_alive" and "error" not in recv) else 0
			
		except Exception as e:
			return 0

	collectors['appsoma_test_alive'] = appsoma_test_alive_collector
except Exception as e:
	print "Error importing appsoma_test_alive.py: " + str(e)
