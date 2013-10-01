import urllib, urllib2
import time
import json
import sys
import psutil
from datacollectors import *
collectors = ss_collect.collectors

def run():
	global cfg
	
	#OPEN CONFIGURATION FILE
	f = open( "node.cfg" )
	j = f.read()
	f.close()
	cfg = json.loads( j )
	
	server_reg()

	#Every interval send data
	while True:
		try:
			data = get_data()
			jre = do_post( "/data", { "name": cfg['name'], "time": int(time.time()), "data": json.dumps( data ) } )
			re = json.loads( jre )
			if "error" in re:
				print re['error']
				if( re['error'] == "NO_REG" ):
					server_reg()
			elif "success" in re:
				print "Successfully sent data"
			time.sleep( cfg['interval'] )
		except (urllib2.HTTPError, IOError) as e:
			print "Failed to send: " + str(e)
			time.sleep( cfg['interval'] )

def server_reg():
	while True:
		try:
			jre = do_post( "/register", { "name": cfg['name'] } )
			re = json.loads( jre )
			if "error" in re:
				if( re["error"] == "WRONG_SECRET" ):
					sys.exit( "Secret in node.cfg does not match server's secret" )
				print re['error']
				continue
			elif 'success' in re:
				print re['success']
				break
			else:
				print "Bad response from server"
		except (urllib2.HTTPError, IOError) as e:
			print "Failed to Connect, Will try again in 10 seconds: " + str(e)
			time.sleep( 10 )

def do_post( url, values ):
	global cfg
	values['secret'] = cfg['secret']
	url = cfg['server'] + url
	if( "://" not in url ):
		url = "http://" + url
	data = urllib.urlencode( values )
	req = urllib2.Request( url, data )
	response = urllib2.urlopen( req )
	return response.read()
	
def get_data():
	try:
		global cfg
		data = []
		for val in cfg['data']:
			data.append( {"name": val[0], "type": val[1], "data": (collectors[val[1]]() if len(val)==2 else collectors[val[1]](val[2])) } )
		return data
	except KeyError as e:
		sys.exit( "Incorrect data collector type in node.cfg: " + str(e) )
	
run()
	