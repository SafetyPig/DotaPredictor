import sqlite3

# Sub-optimal to have the database path coded here.
# TODO: create configuration file
database = '../DotaPredictorDatabase/DotaPredictor'

def addGame(game):
	
	print('Adding game', game)
	conn = sqlite3.connect(database)
	c = conn.cursor()

	c.execute("INSERT INTO Games VALUES (?)", game.radiant_victory)

	'''
	c.execute("INSERT INTO PicksBans VALUES(?,?,?,?,?)",
		game.picksBans.team,
		game.picksBans.isPick,
		game.picksBans.order,
		cursor.lastrowid,

		)
	'''

	print("added game to database")

	conn.close()



