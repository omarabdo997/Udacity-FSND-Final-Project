import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from auth import requires_auth
from models import(
    db,
    setup_db,
    Actor,
    Movie,
    MovieActor)


def paginate(request, data):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 8
    end = start + 8
    data_formated = [single_data.brief_formate() for single_data in data]
    return data_formated[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    DATABASE_URL = os.environ['DATABASE_URL']
    setup_db(app, DATABASE_URL)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

###############################################################################
# ROUTES#######################################################################
###############################################################################

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'You are viewing the home page'
            })

    @app.route('/actors', methods=['GET'])
    def get_actors():
        error = 0
        try:
            actors = Actor.query.all()
            actors_formated = paginate(request, actors)
            if(len(actors_formated) == 0):
                error = 404
            else:
                return jsonify({
                    'success': True,
                    'total_actors': len(actors_formated),
                    'actors': actors_formated
                    })
        except:
            db.session.rollback()
            error = 422
        finally:
            if(error):
                abort(error)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        error = 0
        try:
            body = request.get_json()
            name = body.get('name', '')
            image_link = body.get('image_link')
            if(name == ''):
                error = 400
                description = 'Please provide a name in your post request'
            elif(Actor.query.filter_by(name=name).first()):
                error = 400
                description = 'An actor with this name already exists'
            else:
                Actor(name=name, image_link=image_link).add()
                return jsonify({
                    'success': True,
                    })
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong!'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        error = 0
        try:
            actor = Actor.query.get(actor_id)
            if(actor):
                body = request.get_json()
                name = body.get('name', '')
                image_link = body.get('image_link', '')
                if (not(name == '')):
                    if(Actor.query.filter_by(name=name).first() and
                            not(actor.name == name)):
                        error = 400
                        description = 'An actor with this name already exists'
                    else:
                        actor.name = name
                if (not(image_link == '')):
                    actor.image_link = image_link

                if(error == 0):
                    actor.update()
                    return jsonify({
                        'success': True,
                    })

            else:
                error = 404
                description = 'No actor is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong!'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        error = 0
        try:
            actor = Actor.query.get(actor_id)
            if(actor):
                actor.delete()
                return jsonify({
                    'success': True,
                })
            else:
                error = 404
                description = 'No actor is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong!'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actor-details')
    def get_actor(payload, actor_id):
        error = 0
        try:
            actor = Actor.query.get(actor_id)
            if(actor):
                response_data = {'success': True}
                response_data.update(actor.detail_formate())
                return jsonify(response_data)
            else:
                error = 404
                description = 'No actor is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong!'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/actors/<int:actor_id>/movie', methods=['POST'])
    @requires_auth('post:movies-to-actors')
    def add_movie_to_actor(payload, actor_id):
        error = 0
        try:
            actor = Actor.query.get(actor_id)
            if(actor):
                body = request.get_json()
                movie_id = body.get('movie_id', '')
                movie = Movie.query.get(movie_id)
                if(movie):
                    if(movie in actor.get_movies()):
                        error = 400
                        description = 'A movie with this ID already exists'
                    else:
                        actor.add_movie(movie)
                        return jsonify({
                            'success': True
                            })
                else:
                    error = 404
                    description = 'No movie is found with this ID'

            else:
                error = 404
                description = 'No actor is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong'
        finally:
            if(error):
                abort(error, description=description)

    @app.route(
        '/actors/<int:actor_id>/movie/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies-from-actors')
    def remove_movie_from_actor(payload, actor_id, movie_id):
        error = 0
        try:
            actor = Actor.query.get(actor_id)
            if(actor):
                movie = Movie.query.get(movie_id)
                if(movie):
                    if(movie in actor.get_movies()):
                        actor.delete_movie(movie)
                        return jsonify({
                            'success': True
                            })
                    else:
                        error = 404
                        description = 'No movie is found with this ID in '\
                            'actor list'
                else:
                    error = 404
                    description = 'No movie is found with this ID'
            else:
                error = 404
                description = 'No actor is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/movies', methods=['GET'])
    def get_movies():
        error = 0
        try:
            movies = Movie.query.all()
            movies_formated = paginate(request, movies)
            if(len(movies_formated) == 0):
                error = 404
            else:
                return jsonify({
                    'success': True,
                    'total_movies': len(movies_formated),
                    'movies': movies_formated
                    })
        except:
            db.session.rollback()
            error = 422
        finally:
            if(error):
                abort(error)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        error = 0
        try:
            body = request.get_json()
            name = body.get('name', '')
            image_link = body.get('image_link')
            if(name == ''):
                error = 400
                description = 'Please provide a name in your post request'
            elif(Movie.query.filter_by(name=name).first()):
                error = 400
                description = 'A movie with this name already exists'
            else:
                Movie(name=name, image_link=image_link).add()
                return jsonify({
                    'success': True,
                    })
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong!'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        error = 0
        try:
            movie = Movie.query.get(movie_id)
            if(movie):
                body = request.get_json()
                name = body.get('name', '')
                image_link = body.get('image_link', '')
                if (not(name == '')):
                    if(Movie.query.filter_by(name=name).first() and
                            not(movie.name == name)):
                        error = 400
                        description = 'A movie with this name already exists'
                    else:
                        movie.name = name
                if (not(image_link == '')):
                    movie.image_link = image_link

                if(error == 0):
                    movie.update()
                    return jsonify({
                        'success': True,
                    })

            else:
                error = 404
                description = 'No movie is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong!'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        error = 0
        try:
            movie = Movie.query.get(movie_id)
            if(movie):
                movie.delete()
                return jsonify({
                    'success': True,
                })
            else:
                error = 404
                description = 'No movie is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong!'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movie-details')
    def get_movie(payload, movie_id):
        error = 0
        try:
            movie = Movie.query.get(movie_id)
            if(movie):
                response_data = {'success': True}
                response_data.update(movie.detail_formate())
                return jsonify(response_data)
            else:
                error = 404
                description = 'No movie is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong!'
        finally:
            if(error):
                abort(error, description=description)

    @app.route('/movies/<int:movie_id>/actor', methods=['POST'])
    @requires_auth('post:movies-to-actors')
    def add_actor_to_movie(payload, movie_id):
        error = 0
        try:
            movie = Movie.query.get(movie_id)
            if(movie):
                body = request.get_json()
                actor_id = body.get('actor_id', '')
                actor = Actor.query.get(actor_id)
                if(actor):
                    if(actor in movie.get_actors()):
                        error = 400
                        description = 'An actor with this ID already exists'
                    else:
                        movie.add_actor(actor)
                        return jsonify({
                            'success': True
                            })
                else:
                    error = 404
                    description = 'No actor is found with this ID'

            else:
                error = 404
                description = 'No movie is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong'
        finally:
            if(error):
                abort(error, description=description)

    @app.route(
        '/movies/<int:movie_id>/actor/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:movies-from-actors')
    def remove_actor_from_movie(payload, movie_id, actor_id):
        error = 0
        try:
            movie = Movie.query.get(movie_id)
            if(movie):
                actor = Actor.query.get(actor_id)
                if(actor):
                    if(actor in movie.get_actors()):
                        movie.delete_actor(actor)
                        return jsonify({
                            'success': True
                            })
                    else:
                        error = 404
                        description = 'No actor is found with this ID in '\
                            'movie list'
                else:
                    error = 404
                    description = 'No actor is found with this ID'
            else:
                error = 404
                description = 'No movie is found with this ID'
        except:
            db.session.rollback()
            error = 422
            description = 'Something went wrong'
        finally:
            if(error):
                abort(error, description=description)

###############################################################################
# ERRORS#######################################################################
###############################################################################

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable',
            }), 422)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request',
            'description': error.description,
            }), 400)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed',
            'description': error.description
            }), 405)

    @app.errorhandler(500)
    def internal_server_error(error):
        return (jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error',
            'description': error.description
            }), 500)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found',
            'description': error.description
            }), 404)

    @app.errorhandler(401)
    def unauthorized(error):
        return (jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized',
            'description': error.description
            }), 401)

    @app.errorhandler(403)
    def forbidden(error):
        return (jsonify({
            'success': False,
            'error': 403,
            'message': 'forbidden',
            }), 403)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
