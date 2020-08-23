# Box Story
##### This app's APIs serves the users with stories written by other users. Users can perform CRUD operations on the stories data.
## Type of Users
##### There are two types of users in this app.
* Manager
    * Can perform CRUD on stories and authors alike with the exception of deletion of users and viewing their details.
* Normal User
    * Can perform CRUD on stories and can register/ creat an author with his/her details.
    
## Tables
* Authors
    * It stores authors data name and age.
* Stories:
    * It stores stories data title, type, category and content.

## APIs
1. `(/)`, it just returns available stories in the database. It does not require authentication.
1. `(/register, POST)`, after loging-in a user must POST his details to store it in the database.
1. `(/authors, GET)`, returns authors/users information, only Manager role can perform this action.
1. `(/authors, DELETE)`, removes an author/user data, only Manager role can perform this action.
1. `(/stories/<int>, GET)`, returns a story with specific id.
1. `(/stories, POST)`, creates a story and pend it to the logged-in user.
1. `(/stories, DELETE)`, removes a story written by the logged-in user only.
1. `(/stories, PATCH)`, updates a story written by the logged-in user only.
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
1. User1:
    * Email: user@story.com
    * Password: Aaaa1111 
1. User2:
    * Email: user2@story.com
    * Password: Aaaa1111  
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
//In Postman's body
{
    "title":"deck moby",
    "type":"joke",
    "category":"adventure/ fiction",
    "content":"a sailor who chases a whale and turns out to be a tuna"
    }
```