import dataManagement
from dataAccess import Games
from entities.Game import Game
from entities.PicksBans import PicksBans
import json

def main():
	print("Welcome to dota predictor.")

	matches = dataManagement.getCaptainDraftMatches()
	
	for match in matches:		
		picksBans = match['picks_bans']		
		pickBanEntities = []
		for pickBan in picksBans:
			pickBanEntities.append(PicksBans(pickBan['is_pick'], pickBan['hero_id'], pickBan['team'], pickBan['order']))

		game = Game(match['match_id'], pickBanEntities)		
		Games.AddGame(game)

if __name__ == "__main__":
    main()