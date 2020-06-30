SELECT COUNT(*) edits
FROM revision
JOIN actor ON rev_actor = actor_id
JOIN page ON page_id = rev_page
WHERE actor_name = 'USERNAME'
    AND rev_timestamp < STARTDATE
    AND page_namespace = 0
LIMIT 1000