from flask import Blueprint, render_template, request
import requests
from app import db
from app.models.ids import IDs
from app.models.comment import Comment
from app.models.win import Win
from app.models.league import League
from dotenv import load_dotenv
import os
load_dotenv()

bp = Blueprint('search', __name__)

@bp.route('/search')
def search():
    sum_name = request.args.get('name')
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(sum_name)
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": os.getenv('api_key'),
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    res = requests.get(url=url,headers=headers)
    encrypted_id = res.json()['id']
    url_league = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(encrypted_id)
    res_league = requests.get(url=url_league,headers=headers)
    league_dicts = res_league.json()
    
    
    def get_league_info(league_dict):
        res = [
        league_dict.get('queueType'),
        league_dict.get('tier'),
        league_dict.get('rank'),
        league_dict.get('wins'),
        league_dict.get('losses'),
        league_dict.get('leaguePoints')
            ]
        return res
    results = []
    for league_dict in league_dicts:
        results.append(get_league_info(league_dict))
    length = len(results)

    acc_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(sum_name)
    acc_res = requests.get(url=acc_url, headers=headers)
    acc_id = acc_res.json()['accountId']
    data = IDs(id=encrypted_id,nickname=sum_name,acc_id=acc_id)
    #db.create_all()
    name = IDs.query.filter(IDs.nickname == sum_name).first()
    if name is None :
        db.session.add(data)
        db.session.commit()
    
    comments = Comment.query.filter(Comment.nickname==sum_name).all()

    lgdata = League.query.filter(League.ids_id == encrypted_id).first()

    if lgdata is None :
        data = League(ids_id=encrypted_id, queueType=results[0][0], tier=results[0][1],
        rank=results[0][2], wins=results[0][3], losses=results[0][4], leaguePoints=results[0][5])
        db.session.add(data)
        db.session.commit()
    
    windata = db.session.query(League.wins).filter(League.ids_id == encrypted_id)
    losedata = db.session.query(League.losses).filter(League.ids_id == encrypted_id)
    if windata != results[0][3] :
        League.query.filter(League.ids_id==encrypted_id).update({'tier':results[0][1], 'rank':results[0][2], 'wins':results[0][3], 'losses':results[0][4], 'leaguePoints':results[0][5]})
        db.session.commit()
    if losedata != results[0][4] :
        League.query.filter(League.ids_id==encrypted_id).update({'tier':results[0][1], 'rank':results[0][2], 'wins':results[0][3], 'losses':results[0][4], 'leaguePoints':results[0][5]})
        db.session.commit()
        
    return render_template('search.html',sum_name=sum_name,results=results,length=length,comments=comments)

@bp.route('/comment', methods=['GET', 'POST'])
def comment():
    nickname_ = request.args.get('nickname')
    comment_ = request.args.get('comment')
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(nickname_)
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": os.getenv('api_key'),
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    res = requests.get(url=url,headers=headers)
    encrypted_id = res.json()['id']
    data = Comment(nickname=nickname_, comment=comment_, ids_id=encrypted_id)
    db.session.add(data)
    db.session.commit()

    return render_template('thanks.html')

@bp.route('/delete')
def delete():
    comment = request.args.get('comment')
    print(comment)
    data = Comment.query.filter(Comment.comment == comment).first()
    db.session.delete(data)
    db.session.commit()

    return render_template('delete.html')