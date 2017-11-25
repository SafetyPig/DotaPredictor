import sqlite3

database = '../DotaPredictorDatabase/DotaPredictor.db'

def get_heroes_for_game(game_id):
	conn = sqlite3.connect(database)
	c = conn.cursor()

	c.execute('''
		SELECT * FROM PicksBans
		WHERE GameId = (?) 
		''', [game_id])

	rows = c.fetchall()

	heroes = []

	for row in rows:
		heroes.append(row[4])

	conn.close()

	return heroes