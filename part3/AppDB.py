#
#	Simple MySQL DB Helper class
#	Chris De Pasquale 12/05/17
#

import MySQLConfig
import MySQLdb
import pandas as pd 

class AppDB:
	""" Local MySQL DB class

	attributes:
		dbusername
		dbpassword
		dbhostname
		dbname
	"""

	# Init class with supplied MySQL credentials/details
	def __init__( self ):
		self.dbUsername = MySQLConfig.username
		self.dbPassword = MySQLConfig.password
		self.dbHostname = MySQLConfig.hostname
		self.dbName 	= MySQLConfig.dbname

	# Run MySQL query, fetch results 
	def dbFetch( self, query ):
		db = MySQLdb.connect( host=self.dbHostname, user=self.dbUsername, passwd=self.dbPassword, db=self.dbName, charset='utf8' )
		cursor = db.cursor()
		cursor.execute( query )
		return cursor.fetchall()

	# Run MySQL query
	def dbRun(self, query):
		db = MySQLdb.connect( host=self.dbHostname, user=self.dbUsername, passwd=self.dbPassword, db=self.dbName, charset='utf8' )
		cursor = db.cursor()
		cursor.execute( query )

	# Run MySQL query, return cursor
	def dbFetchCursor( self, query ):
		db = MySQLdb.connect( host=self.dbHostname, user=self.dbUsername, passwd=self.dbPassword, db=self.dbName, charset='utf8' )
		cursor = db.cursor()
		cursor.execute( query )
		return cursor

	# Fetch data from sql query, return as pandas dataframe
	def dbPandasFetch( self, query ):
		connection = MySQLdb.connect( host=self.dbHostname, user=self.dbUsername, passwd=self.dbPassword, db=self.dbName, charset='utf8' )
		return pd.read_sql( query, connection )