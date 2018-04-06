import json
import requests
from collections import Counter


header = {
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNWM3ZTI3MC0xYTA4LTAxMzYtYzU5NC0yZmZkMzhmZDU3ZmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIyODI3NDI1LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InN0YXRjb2FjaCIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.t2xB1pM0PFrhX0hA8ihQEV4X5swRPLO-HaKPLq7Xicg",
    "Accept": "application/vnd.api+json"
}


def get_matches(player):
    url = "https://api.playbattlegrounds.com/shards/pc-na/players?filter[playerNames]=" + player
    rgm = requests.get(url, headers=header)
    rgmj = rgm.json()
    matches = []
    for match in rgmj['data'][0]['relationships']['matches']['data']:
        matches.append(match['id'])
    return matches


def get_match_tele(name, game):
    url = "https://api.playbattlegrounds.com/shards/pc-na/matches/" + get_matches(name)[game]
    rgt = requests.get(url, headers=header)
    rgtj = rgt.json()
    telemetry = ""
    for asset in rgtj["included"]:
        if asset["type"] == "asset":
            telemetry = asset["attributes"]["URL"]
            print("telemetry link: " + asset["attributes"]["URL"])
    return telemetry

def get_match_details(name, game):
    url = "https://api.playbattlegrounds.com/shards/pc-na/matches/" + get_matches(name)[game]
    rgd = requests.get(url, headers=header)
    rgdj = rgd.json()
    for asset in rgdj["included"]:
        if asset["type"] == "participant" and asset["attributes"]["stats"]["name"] == name:
            for k, v in asset["attributes"]["stats"].items():
                print(k, ":", v)


def get_players(name, game):
    json_data = get_match_tele(get_matches(name)[game])
    r = requests.get(json_data, headers=header)
    rj = r.json()
    player_dict = []
    for line in rj:
        for e in line:
            if e == 'character':
                # print line[e]['name']
                player_dict.append(line[e]['name'])
    player_dict = set(player_dict)
    print (len(player_dict))
    for name in player_dict:
        print(name)

    return player_dict


def get_player_kills(name, game):
    url = "https://api.playbattlegrounds.com/shards/pc-na/matches/" + get_matches(name)[game]
    r = requests.get(url, headers=header)
    rj = r.json()
    total_kills = []
    for asset in rj["included"]:
        if asset["type"] == "participant" and asset["attributes"]["stats"]["name"] == name:
            print(asset["attributes"]["stats"]["kills"])


def get_weapons_picked_up(player):
    with open('pc-telemetry.json') as json_data:
        d = json.loads(json_data)
        weapons = []
        for line in d:
            if line['_T'] == 'LogItemPickup' and line['item']['category'] == 'Weapon' and line['character']['name'] == player:
                weapons.append(line['item']['itemId'])
    print(Counter(weapons))

def get_weapon_kills():
    with open('pc-telemetry.json') as json_data:
        d = json.load(json_data)
        weapon_kills = []
        for line in d:
            if line['_T'] == 'LogPlayerKill':
                weapon_kills.append(line['damageCauserName'])
    print(Counter(weapon_kills))

def get_kill_distances():
    with open('pc-telemetry.json') as json_data:
        d = json.load(json_data)
        kill_distances = []
        for line in d:
            if line['_T'] == 'LogPlayerKill':
                kill_distances.append(line['distance'])
    return kill_distances


#get_players("Regnory", 1)
#get_player_kills("Regnory", 4)

#get_match_details("Depown", 0)
get_player_kills("shroud", 10)


#print(max(get_kill_distances()))

#get_player_kills('sxdasd')
#get_weapons_picked_up('DT_Wolf_')
#get_weapon_kills()
