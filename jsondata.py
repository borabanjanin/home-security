#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sqlite3 as sql

DATABASE = 'sensor.db'


def start():
	data = ''' 
	{
		"id": 0,
		"armed": "false",
		"module_1": {
			"sensor_1":"none",
			"sensor_2":"none",
			"sensor_3":"none"
		}
	}
	'''
	data = json.loads(data)
	return data

def create_module(id, armed, sen1, sen2, sen3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor() 
		query = "INSERT INTO Homesec VALUES(%d, %d, '%s', '%s', '%s');" % (id, armed, sen1, sen2, sen3)
		cur.execute(query)

def create_table():
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()  
		cur.execute("DROP TABLE IF EXISTS Homesec")
		cur.execute("CREATE TABLE Homesec(id INT, armed INT, sensor1 TEXT, sensor2 TEXT, sensor3 TEXT);")

def update_module(id, armed, sen1, sen2, sen3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("UPDATE Homesec SET armed=? WHERE id=?",(armed, id))
		cur.execute("UPDATE Homesec SET sensor1=? WHERE id=?",(sen1, id))
		cur.execute("UPDATE Homesec SET sensor2=? WHERE id=?",(sen2, id)) 
		cur.execute("UPDATE Homesec SET sensor3=? WHERE id=?",(sen3, id))
		con.commit()

def fetch_table():
	con = sql.connect(DATABASE) 
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Homesec")
		rows = cur.fetchall()
		return rows

def stop():
	print "in progress"

def pull_id(id):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		query = "SELECT * FROM Homesec where id = %d;" % id 
		cur.execute(query)
		row = cur.fetchone()
		return row
	
def test_database():
	create_table()
	create_module(0, 0, "a", "b", "c")
	create_module(1, 1, "x", "y", "z")
	update_module(0,1,"d","e","f")
	row1 = pull_id(0)
	row2 = pull_id(1)
	rows = fetch_table()		
	if row1 != rows[0]:
		print "data mismatch"
	if row2 != rows[1]:
		print "data mismatch"
	 

if __name__ == "__main__":
	test_database()



