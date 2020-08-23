from flask import (Flask, request, jsonify, abort)
from flask_cors import CORS
from models import setup_db, Author, Story
from auth import requires_auth
import sys


def create_app(test_config=None):
    # Application setup.
    #-----------------------------------------------------------------------------------------------------------------------
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    #-----------------------------------------------------------------------------------------------------------------------


    # CORS setup.
    #-----------------------------------------------------------------------------------------------------------------------
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
    #-----------------------------------------------------------------------------------------------------------------------

    # User Account APIs.
    #-----------------------------------------------------------------------------------------------------------------------
    @app.route('/register', methods=['POST'])
    @requires_auth('post:user')
    def register(payload):
        data = request.get_json()
        if data is None:
            return abort(400)
        authors = Author.query.all()
        for author in authors:
            if payload['sub'].split("auth0|")[1] == author.user_id:
                msg = 'Cannot register an existing user.'
                return abort(500, msg)
        author = Author(fname=data['fname'], lname=data['lname'], age=data['age'], user_id=payload['sub'].split("auth0|")[1])
        author.insert()
        res ={
            'success': True,
            'code': 200,
            'message': 'The user was registered successfully.'
        }
        return jsonify(res)

    @app.route('/authors', methods=['GET'])
    @requires_auth('get:users')
    def get_users(payload):
        authors = Author.query.all()
        if len(authors) <=0:
            msg = 'No authors found.'
            return abort(404, msg)

        temp_res=[]
        for author in authors:
            if author is not None:
                stories = author.stories
                titles = []
                for story in stories:
                    titles.append(story.title)
                if len(titles) <= 0:
                    titles.append('No titles')
                temp_author = {
                    'first_name': author.fname,
                    'last_name': author.lname,
                    'age': author.age,
                    'titles': titles
                }
                temp_res.append(temp_author)

            res = {
                'success': True,
                'code': 200,
                'message': 'Users retrieved successfully.',
                'results': temp_res
            }

        return jsonify(res)

    @app.route('/authors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:user')
    def delete_user(payload, id):
        author = Author.query.get(id)
        if author is None:
            msg = 'No user found with this id.'
            return abort(404, msg)
        stories = Story.query.filter_by(author_id=author.id).all()
        if len(stories)>0:
            for story in stories:
                story.delete()
        msg = 'User {} {} was successfully deleted and along with all of his titles'.format(author.fname, author.lname)
        author.delete()
        res = {
            'success': True,
            'code': 200,
            'message': msg
        }
        return jsonify(res)
    #-----------------------------------------------------------------------------------------------------------------------

    # Story APIs.
    #-----------------------------------------------------------------------------------------------------------------------
    @app.route('/')
    def get_stories():
        print(sys.executable)
        stories = Story.query.all()
        if len(stories) <=0:
            msg = 'No stories to view!!!'
            res = {
                'success': True,
                'code': 200,
                'message': msg
            }
            return jsonify(res)

        temp_res=[]
        for story in stories:
            if story is not None:
                author_id = story.author_id
                author = Author.query.get(author_id)
                if author is not None:
                    temp_story = {
                        'title': story.title,
                        'type': story.type,
                        'category': story.category,
                        'content': story.content,
                        'author': author.fname+" "+author.lname
                    }
                    temp_res.append(temp_story)
        res = {
            'success': True,
            'code': 200,
            'message': 'Stories retrieved successfully',
            'results': temp_res
        }
        return jsonify(res)

    @app.route('/stories/<int:id>', methods=['GET'])
    @requires_auth('get:story')
    def get_story(payload, id):
        story = Story.query.get(id)
        if story is None:
            msg = 'No story found with this id.'
            return abort(404, msg)
        if story.author_id is not None:
            author_id = story.author_id
            author = Author.query.get(author_id)
            temp_res = story.format()
            temp_res['author'] =  '{} {}'.format(author.fname, author.lname)
            res = {
                'success': True,
                'code': 200,
                'message': 'Story with title {}, was successfully retrieved'.format(story.title),
                'results': temp_res
            }
            return jsonify(res)
        msg = 'Seems like wrong stored record.'
        return abort(500, msg)

    @app.route('/stories', methods=['POST'])
    @requires_auth('post:story')
    def new_story(payload):
        data = request.get_json()
        if data is None:
            return abort(400)
        authors = Author.query.all()
        for author in authors:
            #Checks if the logged-in user is the one posting
            if payload['sub'].split("auth0|")[1] == author.user_id:
                if 'title' in data and 'type' in data and 'category' in data and 'content' in data:
                    story = Story(title=data['title'], type=data['type'], category=data['category'], content=data['content'], author=author.id)
                    story.insert()
                    temp_res = story.format()
                    res = {
                        'success': True,
                        'code': 200,
                        'message': 'Story {} written by {} {} was successfully added'.format(story.title, author.fname, author.lname)
                    }
                    return jsonify(res)
                msg = 'Some information is missing or a wrong formed request.'
                return abort(400, msg)

        return abort(401)

    @app.route('/stories/<int:id>', methods=['DELETE'])
    @requires_auth('delete:story')
    def delete_story(payload, id):
        story = Story.query.get(id)
        if story is None:
            msg = 'No story found with this id.'
            return abort(404, msg)
        if story.author_id is not None:
            author = Author.query.get(story.author_id)
            #This checks if the logged-in user is the one who made this story
            if payload['sub'].split("auth0|")[1] == author.user_id:
                msg = 'Story: {} written by author: {} {}, was successfully deleted'.format(story.title, author.fname, author.lname)
                story.delete()
                res = {
                    'success': True,
                    'code': 200,
                    'message': msg
                }
                return jsonify(res)
            return abort(401)
        msg = 'Seems like wrong stored record.'
        return abort(500, msg)

    @app.route('/stories/<int:id>', methods=['PATCH'])
    @requires_auth('patch:story')
    def edit_story(payload, id):
        data = request.get_json()
        if data is None:
            return abort(400)
        story = Story.query.get(id)
        if story is None:
            msg = 'No story found with this id.'
            return abort(404, msg)
        author = Author.query.get(story.author_id)
        if author is None:
            msg = 'Seems like wrong stored record.'
            return abort(500, msg)
        #This checks if the logged-in user is the one who made this story
        if payload['sub'].split("auth0|")[1] == author.user_id:
            if('content' in data and data['content']!=""):
                story.content = data['content']
            if('type' in data and data['type']!=""):
                story.type = data['type']
            if('category' in data and data['category']!=""):
                story.category = data['category']
            if('title' in data and data['title']!=""):
                story.title = data['title']

            story.update()
            temp_res = story.format()
            res = {
                'success': True,
                'code': 200,
                'message': 'Story {}, was updated successfully'.format(story.title),
                'results': temp_res
            }
            return jsonify(res)

        return abort(401)

    @app.route('/logout')
    def logout():
        res = {
            'success': True,
            'code': 200,
            'message': 'Logged out successfully.'
        }
        return jsonify(res)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request: '+error.description
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized: '+error.description
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found: '+error.description
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed: '+error.description
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error: '+error.description
        }), 500

    return app
#-----------------------------------------------------------------------------------------------------------------------
# App run.
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = create_app()
    app.run()
#-----------------------------------------------------------------------------------------------------------------------