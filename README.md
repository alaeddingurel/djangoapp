## LeaderboardApp


This app is a leaderboard app which manages leaderboard ranking and user profile informations


## LeaderBoard
`GET leaderboard/`\
`GET leaderboard/<str:country_code>`

## User
`POST user/create/`
#### Request Body
`{
  'user_id' : uuid,
  'display_name': str,
  'iso_code': str,
  'points': int,
  'rank': int
  }`

`GET user/profile/<uuid:user_uuid>`\

## Submit Score
`POST submit/score/`
#### Request Body
`{
  'score_worth' : int,
  'user_id': uuid  
  }`

## Additional 
`POST construct/`
Constructs database based on `user_number`
#### Request Body
`{
   'user_number': int
  }`

 
`GET delete/`\
Delete Database




