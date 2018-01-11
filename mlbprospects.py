import requests, pandas, json, csv

def get_player_ids(jsondata):
    orgs = ['ana', 'hou', 'sea', 'tex', 'oak', 'min', 'cle', 'cws', 'kc', 'det', 'nyy', 'bal', 'bos', 'tb', 'tor', 'atl', 'nym', 'was', 'phi', 'mia', 'cin', 'chc', 'mil', 'stl', 'pit', 'col', 'ari', 'la', 'sf', 'sd']
    all_ids = []
    data = []
    for i in range(0, len(orgs)):
        for j in range(0,30):
            player_id = jsondata['prospect_players'][orgs[i]][j]['player_id']
            all_ids.append(player_id)
            rank = jsondata['prospect_players'][orgs[i]][j]['rank']
            playerdata = {'Player ID' : player_id, 'Rank' : rank}
            data.append(playerdata)

    return data, all_ids

def get_player_desc(jsondata):
    playerid = jsondata['prospect_player']['player_id']
    drafted = jsondata['prospect_player']['drafted']
    signed = jsondata['prospect_player']['signed']
    team = jsondata['prospect_player']['team_file_code']
    eta = jsondata['prospect_player']['eta']
    scoutinginfo = jsondata['prospect_player']['content']['default']
    descdata = {'Player ID' : playerid, 'Drafted' : drafted, 'Signed' : signed, 'Team' : team, 'ETA' : eta, 'Scouting Info' : scoutinginfo}
    return descdata

def get_player_bio(jsondata):
    position = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['position']
    primary_position = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['primary_position']
    name = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['name_display_first_last']
    college = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['college']
    heightft = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['height_feet']
    heightin = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['height_inches']
    weight = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['weight']
    bats = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['bats']
    throws = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['thrw']
    organization = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['organization']
    birthdate = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['birthdate']
    birth_place = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['birth_place']
    birth_country = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['birth_country']
    team = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['team_name']
    league = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['league']
    playerid = jsondata['prospectwatch_batting']['minors_player_info']['queryResults']['row']['player_id']
    biodata = {'Position' : position, 'Primary Position' : primary_position, 'Name' : name, 'College' : college, 'HeightFt' : heightft, 'HeightIn' : heightin, 'Weight': weight, 'Bats' : bats, 'Throws' : throws, 'Organization' : organization, 'Birthdate' : birthdate, 'Birth Country' : birth_country, 'Birthplace' : birth_place, 'Team' : team, 'League' : league, 'Player ID' : playerid}
    return biodata

###############
# MAIN PROGRAM
###############

masterurl = 'http://m.mlb.com/gen/players/prospects/2017/playerProspects.json'
#MASTER URL contains every players' id, rank, and team

response = requests.get(masterurl)
jsondata = response.json()
master_data, idlist = get_player_ids(jsondata)

alldescdata = []
allbiodata = []

#1 startpoint rather than 0 because of Shohei Ohtani's player_id
for i in range(1, len(idlist)):
    descurl = 'http://m.mlb.com/gen/players/prospects/2017/'+str(idlist[i])+'.json'
    #DESC URL contains all scouting info: drafted, eta, scouting text
    descdata = requests.get(descurl)
    descdata = descdata.json()
    player_desc = get_player_desc(descdata)
    alldescdata.append(player_desc)
    print(player_desc['Player ID'])
    biourl = 'http://m.mlb.com/lookup/json/named.prospectwatch_batting.bam?player_id='+str(idlist[i])+'&season=2017'
    #BIO URL contains all relevant biographical info: position, birth country, name, org, college, height, bats, throws, birthdate, weight, birth city, primary position, team name, league
    biodata = requests.get(biourl)
    biodata = biodata.json()
    player_bio = get_player_bio(biodata)
    allbiodata.append(player_bio)
    print(player_bio['Name'])

descdataframe = pandas.DataFrame(alldescdata)
biodataframe = pandas.DataFrame(allbiodata)
descdataframe.to_csv('mlbprospectdata.csv')
biodataframe.to_csv('mlbprospectdata2.csv')

masterframe = pandas.DataFrame(master_data)
masterframe.to_csv('mlbprospectdata3.csv')