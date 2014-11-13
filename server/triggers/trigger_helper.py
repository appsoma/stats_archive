import sqlite3
import time
import json
import urllib
import urllib2


def get_nodes():
	conn = sqlite3.connect("db.db", timeout=1)
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	rows = db.execute('SELECT id,name from nodes').fetchall()
	conn.close()
	nodes = []
	for row in rows:
		nodes.append( { "id": row['id'], "name": row['name'] } )
	return nodes


def latest_node_data(node, name, time_span):
	conn = sqlite3.connect("db.db", timeout=1)
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	time_ago = time.time() - time_span
	rows = db.execute('SELECT value, time from data where node=? AND name=? AND time >= ? ORDER BY time DESC', (node, name, time_ago)).fetchall()
	conn.close()
	data = []
	for row in rows:
		data.append( { "time": row['time'], "value": json.loads( row['value'] ) } )
	return data


def latest_node_outage(node):
	conn = sqlite3.connect("db.db", timeout=1)
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	data = None
	try:
		row =  db.execute('SELECT id, node, start_time, stop_time FROM outages WHERE node=%d ORDER BY start_time DESC LIMIT 1' % (node['id'])).fetchall()
		if row is not None and len(row) > 0:
			data = { 'id': row[0][0], 'node_id': row[0][1], 'start_time': row[0][2], 'stop_time': row[0][3]}
	except Exception as e:
		print "Error getting outage", e
		data = None
	finally:
		conn.close()
	return data


def start_outage(node, time):
	conn = sqlite3.connect("db.db", timeout=1)
	db = conn.cursor()
	try:
		rows = db.execute('INSERT INTO outages (node, start_time) VALUES (?, ?)', (node['id'], time))
	except Exception as e:
		print e
	conn.commit()
	conn.close()


def stop_outage(id, node, time):
	conn = sqlite3.connect("db.db", timeout=1)
	db = conn.cursor()
	rows = db.execute('UPDATE outages set stop_time=? WHERE id=?', (time, id))
	conn.commit()
	conn.close()


def latest_notes(node, time_span):
	conn = sqlite3.connect("db.db", timeout=1)
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	time_ago = time.time() - time_span
	rows = db.execute('SELECT note, time from notes where node=? AND time >= ?', (node,time_ago) ).fetchall()
	conn.close()
	data = []
	for row in rows:
		data.append( { "time": row['time'], "note": row['note'] } )
	return data


def report_outage(node, start, stop, server):

	params = {'name': node, 'start_time': start, 'stop_time': stop, 'duration': stop - start}
	url = server + "/log/outage?" + urllib.urlencode(params)
	print "Would report: ", url
	return
	try:
		print ("Reporting", url)
		urllib2.urlopen(url, timeout=10)

	except Exception as e:
		print ("Error reporting outage", e.args)


def make_alert( name, value, level ):
	conn = sqlite3.connect("db.db", timeout=1)
	db = conn.cursor()
	rows = db.execute('INSERT INTO alerts (name,value,level,time,sentmail) VALUES (?,?,?,?,?)', (name,value,level,time.time(),0) )
	conn.commit()
	conn.close()	
