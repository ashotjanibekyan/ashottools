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


def get_random_item_by_label(with_lang, without_lang):
    r = requests.get('https://www.wikidata.org/w/api.php', params={
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": "max",
        "rnnamespace": 0
    })
    jsn = r.json()
    if 'query' in jsn and 'random' in jsn['query'] and jsn['query']['random'] and 'title' in jsn['query']['random'][0]:
        for Q in jsn['query']['random']:
            item = Q['title']
            r1 = requests.get('https://www.wikidata.org/w/api.php', params={
                "action": "wbgetentities",
                "format": "json",
                "ids": item,
                "props": "labels",
                "languages": '|'.join(with_lang + [without_lang])
            })
            jsn1 = r1.json()
            if 'entities' in jsn1 and item in jsn1['entities'] and 'labels' in jsn1['entities'][item]:
                langs = list(jsn1['entities'][item]['labels'].keys())
                if without_lang in langs:
                    continue
                if len(with_lang) == 0:
                    return item
                elif len(with_lang) == 1:
                    if with_lang[0] in langs:
                        return item
                    else:
                        continue
                else:
                    num = 0
                    for lang in with_lang:
                        if lang in langs:
                            num += 1
                    if num > 1:
                        return item

    return get_random_item_by_label(with_lang, without_lang)
