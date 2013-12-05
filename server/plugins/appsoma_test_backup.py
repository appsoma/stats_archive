try:
	from ss_plugin import *
	import logging
	import os.path, time

	def appsoma_test_backup_collector():
		try:
			backup_time = os.path.getmtime("/home/deploy/hsc_latest.sql.gz")
			hours = (time.time() - backup_time) / (60 * 60 * 24)
			if int(hours) <= 36:
				return 1
			else:
				return 0
		except Exception as e:
			logging.error( "Error checking database backup" )
			return 0

	collectors['appsoma_test_backup'] = appsoma_test_backup_collector
except Exception, e:
	print "Could not load appsoma_test_backup.py: " + str(e)
