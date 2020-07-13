import requests

API_URL = 'https://hy.wikipedia.org/w/api.php'


def get_bots():
    bots = []
    r = requests.get('https://hy.wikipedia.org/w/api.php?', params={
        "action": "query",
        "format": "json",
        "list": "allusers",
        "augroup": "bot",
        "aulimit": "max"
    })
    jsn = r.json()
    if 'query' in jsn and 'allusers' in jsn['query']:
        bots = [bot['userid'] for bot in jsn['query']['allusers']]
    return bots + ['MusikyanBot']


def get_random_article(ns=0, redirect=None):
    r = requests.get(API_URL, params={
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": ns,
        "rnfilterredir": redirect
    })
    jsn = r.json()
    if 'query' in jsn and 'random' in jsn['query'] and jsn['query']['random']:
        return jsn['query']['random'][0]
    return None


def get_creator(title):
    r = requests.get(API_URL, params={
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "formatversion": "2",
        "rvprop": "userid",
        "rvlimit": "1",
        "rvdir": "newer"
    })
    jsn = r.json()
    try:
        return jsn['query']['pages'][0]['revisions'][0]['userid']
    except Exception as e:
        return 0


def get_random_not_bot():
    bots = get_bots()
    article = get_random_article()
    while get_creator(article['title']) in bots:
        article = get_random_article()
    return article['title']
