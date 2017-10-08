import datetime
import time
import requests
import json

apiKey = '8FC93B2942ADBE03C97ADAC3C126C615'

def getLatestMatchId():
	url = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1'	
	parameters = {	  
	  "key": apiKey,	  
	  "matches_requested" : '1',
	  "format": 'json'
	}

	print("Getting the latest match id.")
	response = requests.get(url, params=parameters)

	print(response)
	
	data = json.loads(response.text)

	return data['result']['matches'][0]['match_id']
	
def getLatestCaptainDraftMatches(amount, matchId, captainsDraftMatches):
	url = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1'	
	parameters = {	  
	  "key": apiKey,
	  "game_mode": '2',
	  "skill": '3',
	  "min_players": '10',
	  "matches_requested" : amount,
	  "format": 'json',
	  "start_at_match_id": matchId
	}

	print('Getting 100 matches.')
	try:
		response = requests.get(url, params=parameters)
	except requests.exceptions.ConnectionError as e:
		print("Error", e)
		return
	print(response)
	
	try:
		data = json.loads(response.text)
	except ValueError as e:
		print("Error", e)
		return

	matches = data['result']['matches']
	
	lastMatchId = 0
	for match in matches:
		url = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1'	
		parameters = {	  
		  "key": apiKey,
		  "match_id": match['match_id']
		}

		print('Getting match with ID', match['match_id'])
		response = requests.get(url, params=parameters)
		print(response)

		matchDetails = json.loads(response.text)
		
		if matchDetails['result']['game_mode'] == 2:			
			print('Found one')			
			captainsDraftMatches.append(matchDetails['result'])	

		lastMatchId = matchDetails['result']['match_id']


	return captainsDraftMatches, lastMatchId

def getCaptainDraftMatches():
	captainDraftMatches = []
	matchId = getLatestMatchId()
	
	fetchTimes = 4
	for x in range(0, fetchTimes):
		matchId = getLatestCaptainDraftMatches(100, matchId, captainDraftMatches)
		if(x < fetchTimes):
			print("Sleep ten seconds.")
			time.sleep(10)	

	return captainDraftMatches

