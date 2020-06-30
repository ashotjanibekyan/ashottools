import toolforge
import datetime


def timestamp_to_datetime(timestamp):
    if type(timestamp) == int:
        timestamp = str(timestamp)
    if len(timestamp) == 14:
        print(timestamp)
        return datetime.datetime(int(timestamp[0:4]),
                                 int(timestamp[4:6]),
                                 int(timestamp[6:8]),
                                 int(timestamp[8:10]),
                                 int(timestamp[10:12]),
                                 int(timestamp[12:14]))
    return None


def datetime_to_timestamp(date):
    if type(date) == datetime.datetime:
        return str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute) + str(date.second)
    return None


def edits(user, start_date, end_date=None):
    conn = toolforge.connect('hywiki')
    start_date = datetime_to_timestamp(start_date)
    if end_date:
        end_date = datetime_to_timestamp(end_date)
    else:
        end_date = '00000000000000'
    with open('./queries/edits.sql', 'r') as sql:
        query = sql.read()
        query = query.replace('USERNAME', user)
        query = query.replace('STARTDATE', start_date)
        query = query.replace('ENDDATE', end_date)
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
            return results[0][0]


def edits_0(user, start_date):
    conn = toolforge.connect('hywiki')
    start_date = datetime_to_timestamp(start_date)
    with open('./queries/edits_0.sql', 'r') as sql:
        query = sql.read()
        query = query.replace('USERNAME', user)
        query = query.replace('STARTDATE', start_date)
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
            return results[0][0]


def registration_date(user):
    conn = toolforge.connect('hywiki')
    with open('./queries/registration.sql', 'r') as sql:
        query = sql.read()
        query = query.replace('USERNAME', user)
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
            timestamp = results[0][0].decode('utf-8')
    return timestamp_to_datetime(timestamp)


def base_stats(user, start_date):
    user_reg = registration_date(user)
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


def base_analyse(stats, experience, edits, edits0, edits0m, edit1m, edit2m, edit3m):
    msg = {
        'experience': 'Առնվազն ' + str(experience) + ' ամիս վիքիստաժ',
        'edits': f'Առնվազն ' + str(edits) + ' խմբագրում',
        'edits_0': f'Առնվազն ' + str(edits0) + ' խմբագրում հոդվածում',
        'edits0m': f'Առնվազն ' + str(edits0m) + ' նախորդ ամսվա ընթացքում'
    }
    if edit1m == edit2m == edit3m:
        msg['last'] = 'Վերջին ամսվան նախորդող 3 ամիսներին ամսական 1-ական գործողություն'
    else:
        msg['last'] = 'Վերջին ամսվան նախորդող 3 ամիսներին համապատասխանաբար ' + str(edit1m) + ', ' + str(edit2m) + ' և ' + str(edit3m) + ' գործողություն'
    result = [(stats[0], stats[0] >= experience, msg['experience']),
              (stats[1], stats[1] >= edits, msg['edits']),
              (stats[2], stats[2] >= edits0, msg['edits_0']),
              (stats[3], stats[3] >= edits0m, msg['edits0m']),
              (', '.join([str(stats[4]), str(stats[5]), str(stats[6])]),
               stats[4] >= edit1m and stats[5] >= edit2m and stats[6] >= edit3m, msg['last'])]
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
    result = [(months, months >= 6, 'Առնվազն 6 ամիս վիքիստաժ'),
              (user_edits, user_edits >= 500, 'Առնվազն 500 խմբագրում'),
              (user_edits_0, user_edits_0 >= 100, 'Առնվազն 500 խմբագրում հոդվածում')]
    return result
