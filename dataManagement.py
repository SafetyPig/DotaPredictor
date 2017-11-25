import datetime
import time
import requests
import json

apiKey = open('/home/hannu/steamApiKey.txt', 'r').read().strip()

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
	try:
		data = json.loads(response.text)
	except json.decoder.JSONDecodeError as e:
		print("Error", e)
		return

	latestMatchId = data['result']['matches'][0]['match_id']
	print("Latest match ID: " + repr(latestMatchId))
	print(data)
	return latestMatchId
	
def getLatestcaptainsModeMatches(amount, matchId, captainsModeMatches, rankedAllPickMatches):
	url = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1'	
	parameters = {	  
	  "key": apiKey,
	  #"game_mode": '2', TODO: For some reason this filter does not work.
	  "skill": '3',
	  "min_players": '10',
	  "matches_requested" : amount,
	  "format": 'json',
	  "start_at_match_id": matchId
	}

	print('Getting ' + str(amount) +  ' matches.')
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

		response = requests.get(url, params=parameters)

		matchDetails = json.loads(response.text)
			
		if('picks_bans' in matchDetails['result']):
			print("==")
			print(matchDetails['result']['picks_bans'])
			print(matchDetails['result']['game_mode'])
			print(matchDetails['result']['lobby_type'])		
			print("==")

		if matchDetails['result']['game_mode'] == 2:			
			print('Found one the captains mode match. PARTY!')			
			captainsModeMatches.append(matchDetails['result'])	


		if matchDetails['result']['game_mode'] == 22:			
			print('Found an all pick match.')			
			rankedAllPickMatches.append(matchDetails['result'])

		lastMatchId = matchDetails['result']['match_id']


	return lastMatchId

def getCaptainsModeMatches():
	captainsModeMatches = []
	rankedAllPickMatches = []
	matchId = 3581327768
	
	fetchTimes = 100
	for x in range(0, fetchTimes):
		matchId = getLatestcaptainsModeMatches(100, matchId, captainsModeMatches, rankedAllPickMatches)
		if(x < fetchTimes):
			print("Sleep ten seconds.")
			print("Latest match ID", matchId)
			print(x)
			time.sleep(10)

	return captainsModeMatches, rankedAllPickMatches

def getHeroes():
	url = 'http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1'	
	parameters = { 
	  "key": apiKey,
	  "format": 'json',
	  "language": 'english'
	}

	print("Getting all the heros")

	response = requests.get(url, params=parameters)

	print(response)
	try:
		data = json.loads(response.text)
	except json.decoder.JSONDecodeError as e:
		print("Error", e)
		return

	listOfHeroes = data['result']['heroes']
	return listOfHeroes