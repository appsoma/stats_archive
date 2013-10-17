try:
	from ss_plugin import *

	def appsoma_restart_annotator():
		try:
			with open( "appsoma.restart_info" ) as f:
				info = json.loads( f.read() )
			
			if info.get( "monitor_read" ):
				return []
			
			info["monitor_read"] = True
			with open( "appsoma.restart_info", "w" ) as f:
				f.write( json.dumps( info ) )

			return ["RESTART: " + info["reason"]] #Annotations return a list of all messages
		except Exception as e:
			return []

	annotators['appsoma_restart'] = appsoma_restart_annotator
except Exception, e:
	print "Error importing appsoma_restart.py: " + str(e)