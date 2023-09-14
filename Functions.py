import os 
import requests 
from discord.ext import commands, tasks
import discord 
import json, random, asyncio
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord import app_commands
from riotwatcher import LolWatcher, ApiError

load_dotenv()
TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
GUILD_ID = int(os.getenv('GUILD_TOKEN'))
CHANNEL_ID = int(os.getenv('CHANNEL_TOKEN'))
API_KEY = os.getenv('API_KEY')

intents=discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

lol_watcher = LolWatcher(API_KEY)

my_region = 'na1'

# def masteryPoints():
#     points_id = []
#     championid = []
#     mastery = lol_watcher.champion_mastery.by_summoner(my_region, 'u8yzPFakLPjWuY5M8f4PwRPaoYpk49Z1uYrgy1enU3XBbQmP4Q1ljqd7Nw')
#     for index in (range(len(mastery))):
#         points_id.append(mastery[index]['championPoints'])
#         championid.append(mastery[index]['championId'])
#     top3 = sorted(zip(points_id, championid), reverse=True)[:3]
#     for x,y in top3:
#       return y
    
#     # 'https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json'
# masteryPoints()




# def champions_name():
#     ids = masteryPoints()
#     championurl = 'https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json'
#     parse_json = json.loads(requests.get(championurl).text)
#     print(parse_json['key'])

# # def champion_name():

# champions_name()
def get_summoner_id(summoner_name):
    api_key = API_KEY
    api_url= "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    api_url = api_url + summoner_name +'?api_key=' + api_key
    response_API = requests.get(api_url)
    data = response_API.text
    parse_json = json.loads(data)    
    summoner_id = parse_json['id']
    print(summoner_id)
    return summoner_id

def get_puuid(summoner_name):
    api_key = API_KEY
    api_url= "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    api_url = api_url + summoner_name +'?api_key=' + api_key
    parse_json = json.loads(requests.get(api_url).text)
    puuid = parse_json['puuid']
    print(puuid)
    return puuid

def get_matchList(puuid):
    api_key = API_KEY
    api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/'
    api_url = api_url + puuid + '/ids?start=0&count=20&api_key=' + api_key
    print(api_url)
    parse_json = json.loads(requests.get(api_url).text)
    value = parse_json.pop(len(parse_json)-1)
    return value

def get_matchData(matchid):
    api_key = API_KEY
    api_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/' + matchid + '?api_key=' + api_key
    parse_json = json.loads(requests.get(api_url).text)
    matchdata = parse_json['info']['participants'][0]
    print(matchdata)
    return matchdata


def goldpermin():
    data = get_matchData(get_matchList(get_puuid('Noor')))
    print(data['goldEarned'])
    return data['goldEarned']

goldpermin()
# get_matchData(get_matchList(get_puuid('Noor')))

def get_rank(summoner_id):
    api_key = API_KEY
    api_url2 = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"
    api_url2 = api_url2 + summoner_id +'?api_key=' + api_key
    response_API = requests.get(api_url2)
    data = response_API.text
    parse_json = json.loads(data)    
    summoner_rank = ''
    summoner_tier = ''

    value = 0
    for index in range(len(parse_json)):
        for key in parse_json[index]:
            # print(index, key, parse_json[index][key])
            if parse_json[index][key] == 'RANKED_SOLO_5x5':
                value = index
                print(value)
    entry = parse_json[value]

    if 'tier' in entry:
        print("Ranked")
    else:
        return "UNRANKED"
    
    summoner_rank = entry['tier']
    summoner_tier = entry['rank']


    print(summoner_tier + " " +  summoner_rank)
    ret_value = summoner_rank + " " + summoner_tier 
    return ret_value
    
def get_flex_rank(summoner_id):
    api_key = API_KEY
    api_url2 = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"
    api_url2 = api_url2 + summoner_id +'?api_key=' + api_key
    response_API = requests.get(api_url2)
    data = response_API.text
    parse_json = json.loads(data)    
    summoner_rank = ''
    summoner_tier = ''

    value = 0
    for index in range(len(parse_json)):
        for key in parse_json[index]:
            # print(index, key, parse_json[index][key])
            if parse_json[index][key] == 'RANKED_FLEX_SR':
                value = index
                print(value)
    entry = parse_json[value]

    if 'tier' in entry:
        print("Ranked")
    else:
        return "UNRANKED"
    
    summoner_rank = entry['tier']
    summoner_tier = entry['rank']


    print(summoner_tier + " " +  summoner_rank)
    ret_value = summoner_rank + " " + summoner_tier 
    return ret_value

def get_level(summoner_name):
    api_key = API_KEY
    api_url= "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    api_url = api_url + summoner_name +'?api_key=' + api_key
    response_API = requests.get(api_url)
    data = response_API.text
    parse_json = json.loads(data)    
    summoner_id = parse_json['summonerLevel']
    return summoner_id


def get_patch_number():
    ddragon_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    reponse_ddragon = requests.get(ddragon_url)
    ddragon_json = json.loads(reponse_ddragon.text) 
    patch_number = ddragon_json[0]
    return (patch_number)

def get_pfp_id(summoner_name):
    api_key = API_KEY
    api_url= "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    api_url = api_url + summoner_name +'?api_key=' + api_key
    response_API = requests.get(api_url)
    parse_json = json.loads(response_API.text)
    pfp_id = parse_json['profileIconId']
    return pfp_id

