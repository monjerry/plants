import psycopg2
from psycopg2.extras import RealDictCursor
class Connection:
	def __init__(self, host, dbname, user, password):

		conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, user, password)
	 
		# print the connection string we will use to connect
		print "Connecting to database\n	->%s" % (conn_string)
	 
		# get a connection, if a connect cannot be made an exception will be raised here
		self.conn = psycopg2.connect(conn_string)
	 
		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

	def execute(self, query):
		# execute our Query
		self.cursor.execute(query)
	 
		# retrieve the records from the database
		records = self.cursor.fetchall()
		return records

	def insert(self, query):
		self.cursor.execute(query)
		self.conn.commit()

