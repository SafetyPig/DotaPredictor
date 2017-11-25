import dataManagement
from dataAccess import Games
from dataAccess import Heroes
from entities.Game import Game
from entities.PicksBans import PicksBans
from entities.Hero import Hero
import json

def main():
	print("Welcome to dota predictor.")

	print("Checking that all heroes are in database")
	heroes = dataManagement.getHeroes()

	if (len(heroes) != Heroes.getCount()):
		for hero in heroes:
			heroToAdd = Hero(hero['id'], hero['localized_name'])
			Heroes.add(heroToAdd)

	print('All heroes in database')			
	
	matches = dataManagement.getCaptainDraftMatches()
	
	for match in matches:		
		picksBans = match['picks_bans']		
		pickBanEntities = []
		for pickBan in picksBans:
			pickBanEntities.append(PicksBans(pickBan['is_pick'], pickBan['hero_id'], pickBan['team'], pickBan['order']))

		game = Game(match['match_id'], pickBanEntities, match['radiant_win'])		
		Games.AddGame(game)

if __name__ == "__main__":
    main()