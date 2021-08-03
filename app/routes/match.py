from flask import Blueprint, render_template, request
import requests
from dotenv import load_dotenv
import os
load_dotenv()


bp = Blueprint('match', __name__)

@bp.route('/match')
def match():
    sum_name = request.args.get('nickname')
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(sum_name)
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": os.getenv('api_key'),
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    res = requests.get(url=url,headers=headers)
    account_Id = res.json()['accountId']

    url_match = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(account_Id)
    res = requests.get(url=url_match, headers=headers)
    matches = res.json()['matches']

    Game_IDs = [] 
    for i in range(0, 20): 
        Game_IDs.append(matches[i].get('gameId'))

    participantId = None
    Win_data = []
    for Game_ID in Game_IDs:
        game_url = "https://kr.api.riotgames.com/lol/match/v4/matches/{}".format(Game_ID)
        res = requests.get(url=game_url, headers=headers)
        data = res.json()
        for i in range(0,10):
            if account_Id == data["participantIdentities"][i]["player"]["accountId"]:
                participantId = i
        if(data["teams"][0]["win"] == "Win"):
            if(participantId >= 5):
                Win_data.append('패배')
            else:
                Win_data.append('승리')
        else:
            if(participantId >= 5):
                Win_data.append('승리')
            else:
                Win_data.append('패배')
    c1 = Win_data.count('승리')
    win_per = round(c1 / 20 * 100, 1)
    
    return render_template('match.html', sum_name=sum_name, Win_data=Win_data, win_per=win_per)
