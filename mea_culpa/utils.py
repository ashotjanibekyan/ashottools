import toolforge

query_template = '''select page_title, page_len, rev_timestamp from page
	join revision on page_id = rev_page
    join actor on actor_id = rev_actor
where rev_parent_id = 0
	and actor_name = %s
    and page_is_redirect = 0
    and page_namespace = 0
    and page_title in
        (select page_title
         from categorylinks
         join page on page_id = cl_from
         where cl_to = %s)
order by rev_timestamp'''

ids = {
    '1': 'Անաղբյուր_և_լրացուցիչ_աղբյուրների_կարիք_ունեցող_հոդվածներ',
    '2': 'Անավարտ_հոդվածներ',
    '3': 'Վիքիֆիկացման_ենթակա_հոդվածներ'
}


def get_data(username, cat_id):
    if cat_id not in ids:
        return []
    username = username[0].upper() + username[1:]
    conn = toolforge.connect('hywiki')
    with conn.cursor() as cur:
        cur.execute(query_template, (username, ids[cat_id]))
        rows = cur.fetchall()
    results = []
    for row in rows:
        results.append([row[0].decode('utf-8'), row[1], row[2].decode('utf-8')])
    return results
