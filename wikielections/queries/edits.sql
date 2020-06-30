SELECT COUNT(*) edits
FROM revision
JOIN actor ON rev_actor = actor_id
WHERE actor_name = 'USERNAME'
    AND rev_timestamp < STARTDATE
    AND rev_timestamp > ENDDATE
LIMIT 1000