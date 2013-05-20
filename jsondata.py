#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sqlite3 as sql

DATABASE = 'sensor.db'



def json_struct():
	data =  {
		"iden": "0",
		"armed": "False",
		"alarm": "False",
		"sensor_1":"Default",
		"sensor_2":"Default",
		"sensor_3":"Default",
		"sensor_4":"Default",
		"sensor_5":"Default",
		"sensor_6":"Default",
		"sensor_7":"Default",
		"sensor_8":"Default",
		"slot_1":"None",
		"slot_2":"None",
		"slot_3":"None",
	}
	#data = json.loads(data)
	return data


def create_module(iden, armed, alarm, sen1, sen2, sen3, sen4, sen5, sen6, sen7, sen8, slot1, slot2, slot3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor() 
		query = "INSERT INTO Homesec VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (iden, armed, alarm, sen1, sen2, sen3, sen4, sen5, sen6, sen7, sen8, slot1, slot2, slot3)
		cur.execute(query)

def create_table():
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()  
		cur.execute("DROP TABLE IF EXISTS Homesec")
		cur.execute("CREATE TABLE Homesec(iden TEXT, armed TEXT, alarm TEXT, sensor1 TEXT, sensor2 TEXT, sensor3 TEXT, sensor4 TEXT, sensor5 TEXT, sensor6 TEXT, sensor7 TEXT, sensor8 TEXT,slot1 TEXT, slot2 TEXT, slot3 TEXT);")

def create_user_table():
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()  
		cur.execute("DROP TABLE IF EXISTS UserData")
		cur.execute("CREATE TABLE UserData(number TEXT);")

def add_number(number):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO UserData VALUES('%s');" % ("+1" + number))
		con.commit()
	
def fetch_numbers():
	con = sql.connect(DATABASE) 
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM UserData")
		rows = []
		rows = cur.fetchall()
		for row in rows:		
			print "%s" % (row[0])
			
 		return rows


def update_module_pi(iden, alarm, slot1, slot2, slot3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("UPDATE Homesec SET alarm=? WHERE iden=?",(alarm, iden))	
		cur.execute("UPDATE Homesec SET slot1=? WHERE iden=?",(slot1, iden))
		cur.execute("UPDATE Homesec SET slot2=? WHERE iden=?",(slot2, iden)) 
		cur.execute("UPDATE Homesec SET slot3=? WHERE iden=?",(slot3, iden))
		con.commit()

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

def user_server_update(iden, armed, alarm):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
		cur.execute("UPDATE Homesec SET armed=? WHERE iden=?",(armed, iden))
		cur.execute("UPDATE Homesec SET alarm=? WHERE iden=?",(alarm, iden))	
		con.commit()

def user_server_config(iden, config1, config2, config3):
	con = sql.connect(DATABASE)
	with con:
		cur = con.cursor()
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
#	create_module("25", "False", "False", "Default", "Default", "Default", "Default", "Default", "Default", "Default", "Default", "None", "None", "None")
#	update_module_pi("25", "True", "Light", "Motion", "Sound")
#	rows = fetch_table()
#	print rows
#	row =	pull_iden("25")
#	print row[1]

if __name__ == "__main__":
	test_database()


