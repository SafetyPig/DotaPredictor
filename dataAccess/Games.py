import sqlite3

# Sub-optimal to have the database path coded here.
# TODO: create configuration file
database = '../DotaPredictorDatabase/DotaPredictor'

def AddGame(game):
	
	print('Adding game', game)
	conn = sqlite3.connect(database)
	c = conn.cursor()

	c.execute("SELECT name FROM sqlite_master WHERE type='table';")
	print(c.fetchall())

	conn.close()
