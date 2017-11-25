import sqlite3
import re

# Sub-optimal to have the database path coded here.
# TODO: create configuration file
database = '../DotaPredictorDatabase/DotaPredictor.db'


def add(hero):
	print('Trying to add hero', hero.name)

	conn = sqlite3.connect(database)

	c = conn.cursor()

	c.execute('''
		SELECT * FROM Heroes 
		WHERE Id = (?)''', [hero.id])

	if(c.fetchone()):
		print('Hero already in database')
		return
	
	c.execute("INSERT INTO Heroes VALUES (?,?)", [hero.id, hero.name])

	conn.commit()
	conn.close()	

def getCount():
	allHeroes = []
	conn = sqlite3.connect(database)
	c = conn.cursor()
	c.execute("SELECT Count(*) FROM Heroes")

	rowCount = str(c.fetchone())

	conn.close()

	return int(re.sub("[^0-9]", "", rowCount))	