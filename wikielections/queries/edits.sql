SELECT COUNT(*)
FROM (SELECT 1 FROM revision
JOIN actor ON rev_actor = actor_id
WHERE actor_name = 'USERNAME'
    AND rev_timestamp < STARTDATE
    AND rev_timestamp > ENDDATE
LIMIT 1000) edits