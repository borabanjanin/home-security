#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sqlite3 as sql

DATABASE = 'sensor.db'


def json_struct():
	data =  {
		"iden": 0,
		"armed": "false",
		"alarm": "false",
		"module_1": {
			"sensor_1":"light",
			"sensor_2":"sound",
			"sensor_3":"motion",
			"config_1":"255",
			"config_2":"255",
			"config_3":"255",
		}
	}
	
	#data = json.loads(data)
	return data

def create_module(iden, armed, alarm, sen1, sen2, sen3, config1, config2, config3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor() 
		query = "INSERT INTO Homesec VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (iden, armed, alarm, sen1, sen2, sen3, config1, config2, config3)
		cur.execute(query)

def create_table():
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()  
		cur.execute("DROP TABLE IF EXISTS Homesec")
		cur.execute("CREATE TABLE Homesec(iden TEXT, armed TEXT, alarm TEXT, sensor1 TEXT, sensor2 TEXT, sensor3 TEXT, config1 TEXT, config2 TEXT, config3 TEXT);")

def update_module(iden, armed, alarm, sen1, sen2, sen3, config1, config2, config3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("UPDATE Homesec SET armed=? WHERE iden=?",(armed, iden))
		cur.execute("UPDATE Homesec SET alarm=? WHERE iden=?",(alarm, iden))	
		cur.execute("UPDATE Homesec SET sensor1=? WHERE iden=?",(sen1, iden))
		cur.execute("UPDATE Homesec SET sensor2=? WHERE iden=?",(sen2, iden)) 
		cur.execute("UPDATE Homesec SET sensor3=? WHERE iden=?",(sen3, iden))
		cur.execute("UPDATE Homesec SET config1=? WHERE iden=?",(config1, iden))
		cur.execute("UPDATE Homesec SET config2=? WHERE iden=?",(config2, iden)) 
		cur.execute("UPDATE Homesec SET config3=? WHERE iden=?",(config3, iden))
		con.commit()

def user_server_update(iden, armed, alarm, config1, config2, config3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("UPDATE Homesec SET armed=? WHERE iden=?",(armed, iden))
		cur.execute("UPDATE Homesec SET alarm=? WHERE iden=?",(alarm, iden))	
		cur.execute("UPDATE Homesec SET armed=? WHERE iden=?",(config1, iden))
		cur.execute("UPDATE Homesec SET alarm=? WHERE iden=?",(config2, iden))	
		cur.execute("UPDATE Homesec SET armed=? WHERE iden=?",(config3, iden))
		con.commit()

def web_server_update(iden, sen1, sen2, sen3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("UPDATE Homesec SET sensor1=? WHERE iden=?",(sen1, iden))
		cur.execute("UPDATE Homesec SET sensor2=? WHERE iden=?",(sen2, iden)) 
		cur.execute("UPDATE Homesec SET sensor3=? WHERE iden=?",(sen3, iden))
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

def pull_iden(iden):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		query = "SELECT * FROM Homesec where iden = %s;" % iden 
		cur.execute(query)
		row = cur.fetchone()
		return row
	
def remove_table():
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE Homesec")

def test_database():
	create_table()
	create_module("0", "false", "false", "a", "b", "c","125")
	create_module("1", "true", "false", "x", "y", "z","125")
	update_module("0","true","true","d","e","f","125")
	row1 = pull_iden("0")
	row2 = pull_iden("1")
	rows = fetch_table()	
	if row1 != rows[0]:
		print "data mismatch"
	if row2 != rows[1]:
		print "data mismatch"
	 

if __name__ == "__main__":
	test_database()


