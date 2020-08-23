import unittest, json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db

TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxHWXRVYnVTYkRVTzlyYnI0VEsxYiJ9.eyJpc3MiOiJodHRwczovL2JhcmF0ZXN0LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjNkNTc5ODg4MTcwMTAwMzcwOTE5YTMiLCJhdWQiOiJzdG9yeSIsImlhdCI6MTU5ODA3MDE1OSwiZXhwIjoxNTk4MTU2NTU5LCJhenAiOiI5SDl1MlZ6Mnd2Q21GSW5ra1NFaUlQcXJzakZ5em82NCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnN0b3J5IiwiZGVsZXRlOnVzZXIiLCJnZXQ6c3RvcmllcyIsImdldDpzdG9yeSIsImdldDp1c2VycyIsInBhdGNoOnN0b3J5IiwicG9zdDpzdG9yeSIsInBvc3Q6dXNlciJdfQ.XkZSoNkxPdLk58B7lsHNav6_bgJgQCSkGMfpZFoQzKWc7VmPfTehSLLVTC_JxJpBBldCaWW7FoWRt99JHsRQeUyfqecP24mkdWO6pA006s6LG5PyizM_8u8l0XcSwYPeyKUabz1bvIa1XNvFrdpsqvzYlqg3xmb_qx4zsO9sy4HuJZW9OzIDxEZ7gEksVRslackm4aD9t_CIlG-Pc7gWOUJfwsFf_1G6b96uHFbc6MMd9xgq_NwLfTfZXs0i02Cz8vs0S7waZbY9C_zFaEH6H36M1ydxxrrvBAAy2Fdnjw4qbXa9pOx_hBmdJZo5JP3zOkUKOsxquQG5Q4Hh26YGnA'


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "storyTest"
        self.password = 'bara1414'
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', self.password, 'localhost:5432',
                                                             self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

#-----------------------------------------------------------------------------------------------------------------------
# Register Test
# ----------------------------------------------------------------------------------------------------------------------
    def test_register_true(self):
        data = {
        "fname":"boss",
        "lname":"bossy",
        "age":32
        }

        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().post('/register', json=data, headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], True)

    def test_register_failure(self):
        data = {
            "fname": "move",
            "lname": "right",
            "age": 32
        }

        auth_header = {
            'Authorization': TOKEN
        }

        res = self.client().post('/register', json=data, headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], False)

#-----------------------------------------------------------------------------------------------------------------------
# Delete user Test
# ----------------------------------------------------------------------------------------------------------------------
    def test_delete_user_true(self):

        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().delete('/authors/1', headers=auth_header)
        data = json.loads(res.data.decode())
        self.assertEqual(data['success'], True)

    def test_delete_user_failure(self):

        auth_header = {
            'Authorization': 'bearer abc {}'.format(TOKEN)
        }

        res = self.client().delete('/authors/1', headers=auth_header)
        data = json.loads(res.data.decode())
        self.assertEqual(data['success'], False)

#-----------------------------------------------------------------------------------------------------------------------
# Get user Test
# ----------------------------------------------------------------------------------------------------------------------
    def test_get_users_true(self):

        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().get('/authors', headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], True)

    def test_get_users_failure(self):

        auth_header = {
            'Authorization': 'bearer abc {}'.format(TOKEN)
        }

        res = self.client().get('/authors', headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], False)
# ----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
# Get a story Test
# ----------------------------------------------------------------------------------------------------------------------
    def test_get_story_true(self):

        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().get('/stories/1', headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], True)

    def test_get_story_failure(self):

        auth_header = {
            'Authorization': 'bearer abc'
        }

        res = self.client().get('/stories', headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], False)

#-----------------------------------------------------------------------------------------------------------------------
# Post a story Test
# ----------------------------------------------------------------------------------------------------------------------
    def test_post_story_true(self):
        data = {
            "title": "story_title",
            "type": "story_type",
            "category": "story_category",
            "content": "story_content"
        }
        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().post('/stories', json=data, headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], True)

    def test_post_story_failure(self):
        data = {
            "title": "story_title",
            "type": "story_type",
            "category": "story_category",
            "content": "story_content"
        }
        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().post('/stories')
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], False)

#-----------------------------------------------------------------------------------------------------------------------
# Delete a story Test
# ----------------------------------------------------------------------------------------------------------------------
    def test_delete_story_true(self):
        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().delete('/stories/1', headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], True)

    def test_delete_story_failure(self):

        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().delete(f'/stories/{-1}', headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], False)

#-----------------------------------------------------------------------------------------------------------------------
# Patch a story Test
# ----------------------------------------------------------------------------------------------------------------------
    def test_patch_story_true(self):
        data = {
            "title": "3story_title",
            "type": "3story_type",
            "category": "3story_category",
            "content": "3story_content"
        }
        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().patch('/stories/3', json=data, headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], True)

    def test_patch_story_failure(self):
        data = {
            "title": "3story_title",
            "type": "3story_type",
            "category": "3story_category",
            "content": "3story_content"
        }
        auth_header = {
            'Authorization': 'bearer {}'.format(TOKEN)
        }

        res = self.client().patch('/stories/3', headers=auth_header)
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], False)

#-----------------------------------------------------------------------------------------------------------------------
# Logout Test
# ----------------------------------------------------------------------------------------------------------------------
    def test_logout_true(self):

        res = self.client().get('/logout')
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], True)

    def test_logout_failure(self):

        res = self.client().post('/logout')
        data = json.loads(res.data.decode())
        print(data)
        self.assertEqual(data['success'], False)




if __name__ == "__main__":
    unittest.main()