import dataManagement
import dotaPredictor
from dataAccess import Games
from dataAccess import Heroes
from dataAccess import PicksBansAccess
from entities.Game import Game
from entities.PicksBans import PicksBans
from entities.Hero import Hero
import json

def getData():
	print("Welcome to dota predictor.")

	print("Checking that all heroes are in database")
	heroes = dataManagement.getHeroes()

	if (len(heroes) != Heroes.getCount()):
		for hero in heroes:
			heroToAdd = Hero(hero['id'], hero['localized_name'])
			Heroes.add(heroToAdd)

	print('All heroes in database')
	
	captainsModeMatches, allPickMatches = dataManagement.getCaptainsModeMatches()
	
	for match in captainsModeMatches:		
		picksBans = match['picks_bans']		
		pickBanEntities = []
		for pickBan in picksBans:
			pickBanEntities.append(PicksBans(pickBan['is_pick'], pickBan['hero_id'], pickBan['team'], pickBan['order']))

		game = Game(match['match_id'], pickBanEntities, match['radiant_win'], "CaptainsMode")		
		Games.add(game)

	for match in allPickMatches:
		pickBanEntities = []		
		for player in match['players']:
			team = 1
			if(str(player['player_slot'])[0] == "0"):
				team = 0

			pickBanEntities.append(PicksBans(1, player['hero_id'], team, -1))

		game = Game(match['match_id'], pickBanEntities, match['radiant_win'], "AllPick")		
		Games.add(game)

def main():
	#getData()

	allGames = Games.getAll()

	victories = []
	heroes = []
	for game in allGames:
		if game[1] == 1:
			victories.append([0,1])
		else:
			victories.append([1,0])

		heroes.append(PicksBansAccess.get_heroes_for_game(game[0]))

	learningVictories = []
	testVictories = []

	learningHeroes = []
	testHeroes = []

	for i in range(len(heroes)):
		if i%10 == 0:
			testVictories.append(victories[i])
			testHeroes.append(heroes[i])
		else:
			learningVictories.append(victories[i])
			learningHeroes.append(heroes[i])

	dotaPredictor.learnToPredictWinner(learningHeroes, learningVictories, testHeroes, testVictories)


if __name__ == "__main__":
    main()