import sqlite3

# Sub-optimal to have the database path coded here.
# TODO: create configuration file
database = '../DotaPredictorDatabase/DotaPredictor.db'

def add(game):
	
	print('Adding game')
	conn = sqlite3.connect(database)
	c = conn.cursor()

	c.execute('''
		SELECT * FROM Games
		WHERE Id = (?)''', [game.id])

	if(c.fetchone()):
		print('Game already in database')
		return

	c.execute("INSERT INTO Games VALUES (?,?,?)", [game.id, game.radiantVictory, game.gameMode])
	gameId = c.lastrowid

	for pickBan in game.picksBans:
		c.execute("INSERT INTO PicksBans VALUES(?,?,?,?,?)",
			[pickBan.team, pickBan.isPick, pickBan.pickOrder, gameId, pickBan.heroId]
			)

	conn.commit()

	print("Added game to database")

	conn.close()

def getAll():
	conn = sqlite3.connect(database)
	c = conn.cursor()

	c.execute("SELECT * FROM Games")

	rows = c.fetchall()

	conn.close()

	return rows
