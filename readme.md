# Box Story
##### This app's APIs serves the users with stories written by other users. Users can perform CRUD operations on the stories data.
## Type of Users
##### There are two types of users in this app.
* Manager
    * Can perform CRUD on stories and authors alike with the exception of deletion of users and viewing their details.
```json
  {"permissions": [
    "delete:story",
    "delete:user",
    "get:stories",
    "get:story",
    "get:users",
    "patch:story",
    "post:story",
    "post:user"
  ]}
```
* Normal User
    * Can perform CRUD on stories and can register/ creat an author with his/her details.
```json
{  "permissions": [
    "delete:story",
    "get:stories",
    "get:story",
    "patch:story",
    "post:story",
    "post:user"
  ]}
```
## Tables
* Authors
    * It stores authors data name and age.
* Stories:
    * It stores stories data title, type, category and content.

## APIs
1. `(/)`, Welcoming screen
1. `(/authors, POST)`, after loging-in a user must POST his details to store it in the database.
1. `(/authors, GET)`, returns authors/users information, only Manager role can perform this action.
1. `(/authors/<int>, DELETE)`, removes an author/user data, only Manager role can perform this action.
1. `(/stories)`, it returns available stories in the database. It does not require authentication.
1. `(/stories/<int>, GET)`, returns a story with specific id.
1. `(/stories, POST)`, creates a story and pend it to the logged-in user.
1. `(/stories/<int>, DELETE)`, removes a story written by the logged-in user only.
1. `(/stories/<int>, PATCH)`, updates a story written by the logged-in user only.
1. `(/logout)`, returns a message after logging out.
___
## Links
* [Box Story Home Page](https://box-story.herokuapp.com
"It turns you back to the home page")
* [Logout Link](https://box-story.herokuapp.com/logout
"You need to logout to be able to login again")
* [Login Link](https://baratest.auth0.com/authorize?audience=story&response_type=token&client_id=9H9u2Vz2wvCmFInkkSEiIPqrsjFyzo64&redirect_uri=https://box-story.herokuapp.com/)
___
## Instructions
#####This app is not suitable for front-end so, it is preferred to use post man.
#####In Postman add an authentication header with bearer key and the provided access_tokens. For POST and PATCH APIs you should also add a json-only body
#####Three access_tokens and users details will be provided:
1. Manager:
    * Email: manager@story.com
    * Password: Aaaa1111
    * Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxHWXRVYnVTYkRVTzlyYnI0VEsxYiJ9.eyJpc3MiOiJodHRwczovL2JhcmF0ZXN0LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkNTc5ODg4MTcwMTAwMzcwOTE5YTMiLCJhdWQiOiJzdG9yeSIsImlhdCI6MTU5ODIyMTMyNiwiZXhwIjoxNTk4MzA3NzI2LCJhenAiOiI5SDl1MlZ6Mnd2Q21GSW5ra1NFaUlQcXJzakZ5em82NCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnN0b3J5IiwiZGVsZXRlOnVzZXIiLCJnZXQ6c3RvcmllcyIsImdldDpzdG9yeSIsImdldDp1c2VycyIsInBhdGNoOnN0b3J5IiwicG9zdDpzdG9yeSIsInBvc3Q6dXNlciJdfQ.FPL8vvhoU8abSIDdhO5Jd2tlqLNoKPVFA0m73Uxr9et4QSBgejB6WDSvPQ9hx4xUOly9pcwhYD_8BMtPTc07YsHHJeI3lsc-tNiiqQfC0uv2d9f_HmPZnhaugBNWXzaNZBnDB9vLjA5gRxs5zgt9MRFfZCVFd_L4kHt4PLQ2qlvc-y4Iqs45WQBMJizkEi6K3lOpwcBaLk73pX24icIUcQfXdacVf-3znFD6_s8oFr-VquCfeLfaxotPeJ_xR3vY9jihdYhXgoOrcg_K1UXNKUUDm5kxtQZPp9Ltczn4GRBcWYffVhUofJhUMLth_xmtjfAN3X7s884vrQ70NHqnYg
1. User1:
    * Email: user@story.com
    * Password: Aaaa1111 
    * Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxHWXRVYnVTYkRVTzlyYnI0VEsxYiJ9.eyJpc3MiOiJodHRwczovL2JhcmF0ZXN0LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkNTc2NTg4MTcwMTAwMzcwOTE5NmIiLCJhdWQiOiJzdG9yeSIsImlhdCI6MTU5ODIyMTQ0NSwiZXhwIjoxNTk4MzA3ODQ1LCJhenAiOiI5SDl1MlZ6Mnd2Q21GSW5ra1NFaUlQcXJzakZ5em82NCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnN0b3J5IiwiZ2V0OnN0b3JpZXMiLCJnZXQ6c3RvcnkiLCJwYXRjaDpzdG9yeSIsInBvc3Q6c3RvcnkiLCJwb3N0OnVzZXIiXX0.G-UsDq4Q_wz0kYLoOX-Wi7ROlfIA7EMdhOh2yYRrH3SjCTLbTohT8F1CMXV6z11H79I1CY6wX7QLIlrZBGeW5eUgUGS8E0ihfWmjTxuoZON4HQYmv-CTEn_mbFJKZOx1yvAxaIy8aWA9T15mteFA6PVbwt5o03bpAWRt45yc0oScOreQuPWm21SExQL8qpPaPhpxF_I9J2cQCQ1xFTwNuzOKk3nhFzVqG0NPcLzavXb6aPtB1pPysYSBDNmyC9JKoVspWaXIdicswgnF9siMIq991haDPQXVEZi_v2nPNrVuo2xV1ouakTRXachrZHgC8-G6oggleodvvxT9W5j3lQ
1. User2:
    * Email: user2@story.com
    * Password: Aaaa1111  
    * Token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxHWXRVYnVTYkRVTzlyYnI0VEsxYiJ9.eyJpc3MiOiJodHRwczovL2JhcmF0ZXN0LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkNjA3NTczZWRjMTAwM2Q2OWViOWMiLCJhdWQiOiJzdG9yeSIsImlhdCI6MTU5ODIyMTU3NiwiZXhwIjoxNTk4MzA3OTc2LCJhenAiOiI5SDl1MlZ6Mnd2Q21GSW5ra1NFaUlQcXJzakZ5em82NCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnN0b3J5IiwiZ2V0OnN0b3JpZXMiLCJnZXQ6c3RvcnkiLCJwYXRjaDpzdG9yeSIsInBvc3Q6c3RvcnkiLCJwb3N0OnVzZXIiXX0.UFT1zoEm5K0hmd_TILH3Xa2R1bcT9T-RRolrSjphtseB24ybzC7gH3G9xRdx6qFV2H3gZ011g2xWotB2O58Bqj0raAZqOk_IZGlf0v_zWbFh5mPvmdLhXVxHWP81CiE1TwCO_c6Luou4I2Qob0QczMyQR77mM-OkQ-rG2kKUVtUktXDtS-GjEGGJGnM_RML0jZQtRs5XS5ygDivaCbuLuDmU1ULyVKG-JLbynfnTTvj06tA9J--XCoTIkm2Xvtn73kcsUBGDyOUUb8hKKtwKk__2UMnIQUJkeRDsdi19CRqzBA57GxMvyas_PIe_yp4dsSWEsek2yWfCQnONeYaV0A
##### \* *IF* \* you going to login, please login with the above provided credentials.
___
## API instructions  
#### Registration Body 
```python
@app.route('register', methods=['POST'])
```
```json
//In Postman's body
{
    "fname":"wrighter",
    "lname":"books",
    "age":33
    }
```
#### Adding Story Body 
```python
@app.route('stories', methods=['POST'])
```
```json
//In Postman's body
{
    "title":"moby deck",
    "type":"novel",
    "category":"adventure/ fiction",
    "content":"a sailor who chases a whale"
    }
```
#### Updating Story Body 
```python
@app.route('stories', methods=['PATCH'])
```
```json
//In Postman's body, You do not have to update all data you can pick which data you want to update
{
    "title":"deck moby",
    "type":"joke",
    "category":"adventure/ fiction",
    "content":"a sailor who chases a whale and turns out to be a tuna"
    }
```