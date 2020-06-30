import datetime
import requests

API_URL = 'https://hy.wikipedia.org/w/api.php'


def timestamp_to_datetime(timestamp):
    if type(timestamp) == int:
        timestamp = str(timestamp)
    if len(timestamp) == 14:
        return datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S')
    return None


def datetime_to_timestamp(date):
    if type(date) == datetime.datetime:
        return date.strftime('%Y%m%d%H%M%S')
    return None


def edits(user, start_date, end_date=None, ns=None):
    start_date = datetime_to_timestamp(start_date)
    r = requests.get(url=API_URL, params={
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "uclimit": "max",
        "ucstart": start_date,
        "ucend": end_date,
        "ucuser": user,
        "ucnamespace": ns
    })
    jsn = r.json()
    uccontinue = jsn['continue']['uccontinue'] if 'continue' in jsn and 'uccontinue' in jsn['continue'] else None
    contrb_num = len(jsn['query']['usercontribs']) if 'query' in jsn and 'usercontribs' in jsn['query'] else 0
    while uccontinue and contrb_num < 1000:
        r = requests.get(url=API_URL, params={
            "action": "query",
            "format": "json",
            "list": "usercontribs",
            "uclimit": "max",
            "ucstart": start_date,
            "ucend": end_date,
            "ucuser": user,
            "uccontinue": uccontinue,
            "ucnamespace": ns
        })
        jsn = r.json()
        uccontinue = jsn['continue']['uccontinue'] if 'continue' in jsn and 'uccontinue' in jsn['continue'] else None
        contrb_num += len(jsn['query']['usercontribs']) if 'query' in jsn and 'usercontribs' in jsn['query'] else 0
    return contrb_num


def edits_0(user, start_date):
    return edits(user, start_date, ns=0)


def registration_date(user):
    r = requests.get(API_URL, params={
        "action": "query",
        "format": "json",
        "list": "users",
        "usprop": "registration",
        "ususers": user
    })
    jsn = r.json()
    if 'query' in jsn and 'users' in jsn['query'] and 'registration' in jsn['query']['users'][0]:
        return datetime.datetime.strptime(jsn['query']['users'][0]['registration'], "%Y-%m-%dT%H:%M:%SZ")
    return None


def base_stats(user, start_date):
    user_reg = registration_date(user)
    if user_reg:
        months = (start_date - user_reg).days / 30
        user_edits = edits(user, start_date)
        user_edits_0 = edits_0(user, start_date)
        edits_last_month = edits(user, start_date, start_date - datetime.timedelta(days=31))
        edits_2last_month = edits(user, start_date - datetime.timedelta(days=31),
                                  start_date - datetime.timedelta(days=2 * 31))
        edits_3last_month = edits(user, start_date - datetime.timedelta(days=2 * 31),
                                  start_date - datetime.timedelta(days=3 * 31))
        edits_4last_month = edits(user, start_date - datetime.timedelta(days=3 * 31),
                                  start_date - datetime.timedelta(days=4 * 31))

        return months, user_edits, user_edits_0, edits_last_month, edits_2last_month, edits_3last_month, edits_4last_month
    return 0, 0, 0, 0, 0, 0, 0


def base_analyse(stats, experience, edits, edits0, edits0m, edit1m, edit2m, edit3m):
    msg = {
        'experience': 'Առնվազն ' + str(experience) + ' ամիս վիքիստաժ',
        'edits': 'Առնվազն ' + str(edits) + ' խմբագրում',
        'edits_0': 'Առնվազն ' + str(edits0) + ' խմբագրում հոդվածում',
        'edits0m': 'Առնվազն ' + str(edits0m) + ' խմբագրում նախորդ ամսվա ընթացքում'
    }
    if edit1m == edit2m == edit3m:
        msg['last'] = 'Վերջին ամսվան նախորդող 3 ամիսներին ամսական 1-ական գործողություն'
    else:
        msg['last'] = 'Վերջին ամսվան նախորդող 3 ամիսներին համապատասխանաբար ' + str(edit1m) + ', ' + str(
            edit2m) + ' և ' + str(edit3m) + ' գործողություն'
    result = [[int(stats[0]), stats[0] >= experience, msg['experience']],
              [stats[1], stats[1] >= edits, msg['edits']],
              [stats[2], stats[2] >= edits0, msg['edits_0']],
              [stats[3], stats[3] >= edits0m, msg['edits0m']],
              [', '.join([str(stats[4]).replace('1000', '1000+'), str(stats[5]).replace('1000', '1000+'),
                          str(stats[6]).replace('1000', '1000+')]),
               stats[4] >= edit1m and stats[5] >= edit2m and stats[6] >= edit3m, msg['last']]]
    return result


def article_of_year(user, start_date):
    # 11 ամիս վիքիստաժ
    # Նվազագույնը 500 գործողություն
    # Նվազագույնը 250 գործողություն հոդվածներում
    # Վերջին ամսվան նախորդող 3 ամիսներին ամսական 1-ական գործողություն

    stats = base_stats(user, start_date)
    return base_analyse(stats, 11, 500, 250, 10, 1, 1, 1)


def featured_article(user, start_date):
    # 6 ամիս վիքիստաժ
    # Նվազագույնը 500 գործողություն
    # Նվազագույնը 250 գործողություն հոդվածներում
    # Նվազագույնը 10 գործողություն վերջին ամսում
    # Վերջին ամսվան նախորդող 3 ամիսներին ամսական 1-ական գործողություն
    stats = base_stats(user, start_date)
    return base_analyse(stats, 6, 500, 250, 10, 1, 1, 1)


def good_article(user, start_date):
    return featured_article(user, start_date)  # at this point they have the same requirements


def admin(user, start_date):
    # 6 ամիս վիքիստաժ
    # Նվազագույնը 1000 գործողություն
    # Նվազագույնը 500 գործողություն հոդվածներում
    # Նվազագույնը 33 գործողություն վերջին ամսում
    # Վերջին ամսվան նախորդող 3 ամիսներին ամսական 1-ական գործողություն
    stats = base_stats(user, start_date)
    return base_analyse(stats, 6, 1000, 500, 33, 1, 1, 1)


def deletion(user, start_date):
    # 6 ամիս վիքիստաժ
    # Նվազագույնը 500 գործողություն
    # Նվազագույնը 100 գործողություն հոդվածներում
    user_reg = registration_date(user)
    months = (start_date - user_reg).days / 30
    user_edits = edits(user, start_date)
    user_edits_0 = edits_0(user, start_date)
    result = [[int(months), months >= 6, 'Առնվազն 6 ամիս վիքիստաժ'],
              [user_edits, user_edits >= 500, 'Առնվազն 500 խմբագրում'],
              [user_edits_0, user_edits_0 >= 100, 'Առնվազն 500 խմբագրում հոդվածում']]
    return result
