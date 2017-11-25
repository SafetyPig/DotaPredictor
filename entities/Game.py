class Game:
	def __init__(self, id, picksBans, radiantVictory, gameMode):
		self.id = id
		self.picksBans = picksBans
		self.radiantVictory = radiantVictory
		self.gameMode = gameMode

	def __str__(self):
		return "ID: " + str(self.id) + " picksBans: " + str(self.picksBans) + " radiantVictory: " + str(self.radiantVictory) + " gameMode: " + self.gameMode 