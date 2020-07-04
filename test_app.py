import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db_test, Actor, Movie


TEST_DATABASE_URL = os.environ['TEST_DATABASE_URL']
CASTING_ASSISTANT_TOKEN = os.environ['CASTING_ASSISTANT_TOKEN']
CASTING_DIRECTOR_TOKEN = os.environ['CASTING_DIRECTOR_TOKEN']
EXECUTIVE_PRODUCER_TOKEN = os.environ['EXECUTIVE_PRODUCER_TOKEN']


class CastingAgencyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''This setup runs only once each test'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = TEST_DATABASE_URL
        setup_db_test(self.app, self.database_path)
        self.casting_assistant_header = {
            'Authorization': 'bearer {}'.format(CASTING_ASSISTANT_TOKEN)}
        self.casting_director_header = {
            'Authorization': 'bearer {}'.format(CASTING_DIRECTOR_TOKEN)}
        self.executive_producer_header = {
            'Authorization': 'bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}

###############################################################################
# Testing all endpoints using a valid authentication header####################
###############################################################################

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])

    def test_404_get_actors(self):
        res = self.client().get('/actors?page=500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['description'], 'No actors found')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_actor(self):
        res = self.client().post(
            '/actors',
            headers=self.casting_director_header,
            json={
                'name': 'Mel Gibson',
                'image_link': (
                    'https://www.gstatic.com/tv/thumb/persons/633/633_v9_bc.'
                    'jpg')})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        actor = Actor.query.filter_by(name='Mel Gibson').first()
        self.assertEqual(actor.name, 'Mel Gibson')
        self.assertEqual(
            actor.image_link,
            'https://www.gstatic.com/tv/thumb/persons/633/633_v9_bc.jpg')

    def test_dublicate_name_post_actor(self):
        res = self.client().post(
            '/actors',
            headers=self.executive_producer_header,
            json={'name': 'Leonardo Dicaprio'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'],
            'An actor with this name already exists')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_no_name_post_actor(self):
        res = self.client().post(
            '/actors',
            headers=self.casting_director_header,
            json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'],
            'Please provide a name in your post request')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_patch_actor(self):
        res = self.client().patch(
            '/actors/1',
            headers=self.casting_director_header,
            json={'name': 'Leo'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        actor = Actor.query.get(1)
        self.assertEqual(actor.name, 'Leo')

    def test_dublicate_name_patch_actor(self):
        res = self.client().patch(
            '/actors/1',
            headers=self.executive_producer_header,
            json={'name': 'Brad Pitt'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'],
            'An actor with this name already exists')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_same_name_patch_actor(self):
        res = self.client().patch(
            '/actors/1',
            headers=self.casting_director_header,
            json={
                'name': 'Leonardo Dicaprio',
                'image_link': (
                    'https://www.telegraph.co.uk/content/dam/films/'
                    '2018/09/21/TELEMMGLPICT000027014340_trans%2B%2BM37qcIWR9C'
                    'trqmiMdQVx7HKcsGtiuU_lafizKj4PQO0.jpeg')})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        actor = Actor.query.get(1)
        self.assertEqual(actor.name, 'Leonardo Dicaprio')
        self.assertEqual(
            actor.image_link,
            (
                'https://www.telegraph.co.uk/content/dam/films/2018/09/21/TELE'
                'MMGLPICT000027014340_trans%2B%2BM37qcIWR9CtrqmiMdQVx7HKcsGtiu'
                'U_lafizKj4PQO0.jpeg'))

    def test_404_patch_actor(self):
        res = self.client().patch(
            '/actors/1000',
            headers=self.executive_producer_header,
            json={'name': 'Leo'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['description'], 'No actor is found with this ID')
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        actor = Actor.query.get(5)
        self.assertTrue(actor)
        res = self.client().delete(
            '/actors/5',
            headers=self.casting_director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        actor = Actor.query.get(5)
        self.assertFalse(actor)

    def test_404_delete_actor(self):
        res = self.client().delete(
            '/actors/1000',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['description'], 'No actor is found with this ID')
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actor(self):
        res = self.client().get(
            '/actors/4',
            headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        self.assertTrue(data['image_link'])
        self.assertTrue(data['movies'])

    def test_404_get_actor(self):
        res = self.client().get(
            '/actors/500',
            headers=self.casting_director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_movie_to_actor(self):
        res = self.client().post(
            '/actors/1/movie',
            headers=self.executive_producer_header,
            json={'movie_id': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actor = Actor.query.get(1)
        movies = actor.get_movies()
        movie = Movie.query.get(1)
        self.assertTrue(movie in movies)

    def test_add_existing_movie_to_actor(self):
        '''Movie already exists in actor's list'''
        res = self.client().post(
            '/actors/4/movie',
            headers=self.executive_producer_header,
            json={'movie_id': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'], 'A movie with this ID already exists')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_actor_not_found_add_movie_to_actor(self):
        res = self.client().post(
            '/actors/500/movie',
            headers=self.executive_producer_header,
            json={'movie_id': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            data['description'], 'No actor is found with this ID')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_movie_not_found_add_movie_to_actor(self):
        res = self.client().post(
            '/actors/1/movie',
            headers=self.executive_producer_header,
            json={'movie_id': 500})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            data['description'], 'No movie is found with this ID')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_remove_movie_from_actor(self):
        actor = Actor.query.get(4)
        movies = actor.get_movies()
        movie = Movie.query.get(2)
        self.assertTrue(movie in movies)
        res = self.client().delete(
            '/actors/4/movie/2',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actor = Actor.query.get(4)
        movies = actor.get_movies()
        movie = Movie.query.get(2)
        self.assertFalse(movie in movies)

    def test_remove_non_existing_movie_from_actor(self):
        '''Movie does exist but not in that actor's list'''
        res = self.client().delete(
            '/actors/2/movie/1',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'], 'No movie is found with this ID in actor list'
            )
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_actor_not_found_remove_movie_from_actor(self):
        res = self.client().delete(
            '/actors/500/movie/1',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            data['description'], 'No actor is found with this ID'
            )
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_movie_not_found_remove_movie_from_actor(self):
        res = self.client().delete(
            '/actors/4/movie/500',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            data['description'], 'No movie is found with this ID')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])

    def test_404_get_movies(self):
        res = self.client().get('/movies?page=500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['description'], 'No movies found')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_movie(self):
        res = self.client().post(
            '/movies',
            headers=self.executive_producer_header,
            json={
                'name': 'Toy Story',
                'image_link': (
                    'https://upload.wikimedia.org/wikipedia/en/thumb'
                    '/1/13/Toy_Story.jpg/220px-Toy_Story.jpg')})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        movie = Movie.query.filter_by(name='Toy Story').first()
        self.assertEqual(movie.name, 'Toy Story')
        self.assertEqual(
            movie.image_link,
            (
                'https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Toy_Stor'
                'y.jpg/220px-Toy_Story.jpg'))

    def test_dublicate_name_post_movie(self):
        res = self.client().post(
            '/movies',
            headers=self.executive_producer_header,
            json={'name': 'Maleficent'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'], 'A movie with this name already exists')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_no_name_post_movie(self):
        res = self.client().post(
            '/movies',
            headers=self.executive_producer_header,
            json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'], 'Please provide a name in your post request')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_patch_movie(self):
        res = self.client().patch(
            '/movies/3',
            headers=self.casting_director_header,
            json={'name': 'Avatar'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        movie = Movie.query.get(3)
        self.assertEqual(movie.name, 'Avatar')

    def test_dublicate_name_patch_movie(self):
        res = self.client().patch(
            '/movies/3',
            headers=self.executive_producer_header,
            json={'name': 'Maleficent'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'], 'A movie with this name already exists')
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_same_name_patch_movie(self):
        res = self.client().patch(
            '/movies/3',
            headers=self.casting_director_header,
            json={
                'name': 'Avatar',
                'image_link': (
                    'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9Gc'
                    'QQbuGtOX1T7WxlzhrGNeHtoXSOYJ_TbvMaeg&usqp=CAU')})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        movie = Movie.query.get(3)
        self.assertEqual(movie.name, 'Avatar')
        self.assertEqual(
            movie.image_link,
            (
                'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQQbuG'
                'tOX1T7WxlzhrGNeHtoXSOYJ_TbvMaeg&usqp=CAU'))

    def test_404_patch_movie(self):
        res = self.client().patch(
            '/movies/1000',
            headers=self.executive_producer_header,
            json={'name': 'Simba'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['description'], 'No movie is found with this ID')
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        movie = Movie.query.get(4)
        self.assertTrue(movie)
        res = self.client().delete(
            '/movies/4',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        movie = Movie.query.get(4)
        self.assertFalse(movie)

    def test_404_delete_movie(self):
        res = self.client().delete(
            '/movies/1000',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['description'], 'No movie is found with this ID')
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movie(self):
        res = self.client().get(
            '/movies/1',
            headers=self.casting_assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        self.assertTrue(data['image_link'])
        self.assertTrue(data['actors'])

    def test_404_get_movie(self):
        res = self.client().get(
            '/movies/500',
            headers=self.casting_director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_actor_to_movie(self):
        res = self.client().post(
            '/movies/2/actor',
            headers=self.executive_producer_header,
            json={'actor_id': 2})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        movie = Movie.query.get(2)
        actors = movie.get_actors()
        actor = Actor.query.get(2)
        self.assertTrue(actor in actors)

    def test_add_existing_actor_to_movie(self):
        '''Actor already exists in movie's list'''
        res = self.client().post(
            '/movies/1/actor',
            headers=self.executive_producer_header,
            json={'actor_id': 4})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'], 'An actor with this ID already exists'
            )
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_movie_not_found_add_actor_to_movie(self):
        res = self.client().post(
            '/movies/500/actor',
            headers=self.executive_producer_header,
            json={'actor_id': 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            data['description'], 'No movie is found with this ID'
            )
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_actor_not_found_add_actor_to_movie(self):
        res = self.client().post(
            '/movies/1/actor',
            headers=self.executive_producer_header,
            json={'actor_id': 500})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            data['description'], 'No actor is found with this ID'
            )
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_remove_actor_from_movie(self):
        movie = Movie.query.get(6)
        actors = movie.get_actors()
        actor = Actor.query.get(6)
        self.assertTrue(actor in actors)
        res = self.client().delete(
            '/movies/6/actor/6',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        movie = Movie.query.get(6)
        actors = movie.get_actors()
        actor = Actor.query.get(6)
        self.assertFalse(actor in actors)

    def test_remove_non_existing_actor_from_movie(self):
        '''Movie does exist but not in that actor's list'''
        res = self.client().delete(
            '/movies/1/actor/2',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['description'], 'No actor is found with this ID in movie list'
            )
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_movie_not_found_remove_actor_from_movie(self):
        res = self.client().delete(
            '/movies/500/actor/1',
            headers=self.executive_producer_header
            )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            data['description'], 'No movie is found with this ID')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_actor_not_found_remove_actor_from_movie(self):
        res = self.client().delete(
            '/movies/4/actor/500',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(
            data['description'], 'No actor is found with this ID'
            )
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

###############################################################################
# Failing some authentication tests############################################
###############################################################################

    def test_no_authorization_header(self):
        res = self.client().post(
            '/actors',
            json={'name': 'Pharel williams'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            data['description'], 'Authorization header is expected'
            )
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertEqual(data['message'], 'unauthorized')

    def test_forbidden_for_casting_assistant(self):
        res = self.client().post(
            '/actors',
            headers=self.casting_assistant_header,
            json={'name': 'Pharel williams'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'forbidden')

    def test_forbidden_for_casting_director(self):
        res = self.client().post(
            '/movies',
            headers=self.casting_director_header,
            json={'name': 'Inception'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'forbidden')


if __name__ == '__main__':
    unittest.main()
