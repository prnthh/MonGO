#!/usr/bin/python
from pymongo import MongoClient
import ast
import sys, getopt


def interpret():
	while 1:
		com = raw_input(">>").split(' ', 1)
		if len(com)>1:
			com, arg = com
		else:
			arg = None
			com = com[0]
		com = com.lower()
		if com == "insert":
			insert(arg)
		elif com == "help":
			helper(arg)
		elif com == "find":
			find(arg)
		elif com == "findall":
			findall()
		elif com == "count":
			count(arg)
		elif com == "db":
			db(arg)
		elif com == "":
			pass
		elif com == "exit":
			sys.exit()
		else:
			helper(None)

def insert(arg):
	if arg:
		post = ast.literal_eval(arg)
	else:
		print "Insert key:value pairs. Press enter to insert."
		post = dict()
		while 1:
			key = raw_input('key:')
			if key=='':
				break
			else:
				post[key] = input("value:")
	try:
		client[dbname].posts.insert(post)	
	except Exception:
		pass
	print post


def find(arg):
	posts = client[dbname].posts
	if arg:
		print posts.find_one(ast.literal_eval(arg))
	else:
		print posts.find_one()

def findall():
	p = client[dbname].posts.find();
	for i in p:
		print i

def count(arg):
	if arg:
		print client[dbname].posts.find(ast.literal_eval(arg)).count()
	else:
		print client[dbname].posts.count()

def db(arg):
	if arg:
		global dbname
		dbname = arg
		print "DB name set to '%s'" % dbname
	else:
		print "Error: specify database name."

def helper(arg):
	helps = {"db <dbname>":"Specify the db being accessed.", "count [json]":"Counts the number of documents in a db.\nWith an argument, returns the number of matching documents.", "findall":"Returns all documents in the current db.", "find [json]":"Finds and returns all documents containing the given key-value pair.\nWithout arguments, it returns the first document in the db.", "insert [json data]":"Inserts a json document into the db.\nWithout the arguments, it enters an interactive prompt to create documents.", "help":"Displays this helpfile.", "exit":"Exits the MonGo shell."}
	if arg in helps:
		print arg
		print helps[arg],"\n"
	else:
		for i in helps:
			print i
			print helps[i],"\n"
		
ip = "localhost"
port = 27017
dbname = "test"

if __name__=="__main__":
#opts, args = getopt.getopt(argv)
	print "MonGO version 0.0.1 developed by Pranith Hengavalli"
	ip = raw_input("Enter IP address[default:localhost]: ")
	if ip=="":
		ip = "localhost"
	port = int(raw_input("Enter port[default:27017]: ") or 27017)
	print "Connecting to %s:%s" % (ip, port)
	client = MongoClient(ip, port)
	print "Success. "
	interpret()

""" To include these functions within your own scripts,
1. import mongo
2. mongo.client = mongo.MongoClient(<ip>, <port>)
3. mongo.insert("<args>")
"""

