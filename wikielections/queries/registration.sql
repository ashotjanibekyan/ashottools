SELECT user_registration
FROM user
JOIN user_properties ON up_user = user_id
WHERE user_name = 'USERNAME'