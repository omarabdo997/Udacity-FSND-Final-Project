from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
import json

db = SQLAlchemy()


def setup_db(app, database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def setup_db_test(app, database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()

    ###########################################################################
    # Add entries to data base for testing and entry number represents it's ID
    ###########################################################################

    actor1 = Actor(name='Leonardo Dicaprio')
    actor1.add()
    actor2 = Actor(name='Brad Pitt')
    actor2.add()
    actor3 = Actor(name='Jennifer Aniston')
    actor3.add()
    actor4 = Actor(
        name='Angelina Jolie',
        image_link=(
            'https://i.insider.com/5e9dde0992e8ba7bde291467?width=1100'
            '&format=jpeg&auto=webp'))
    actor4.add()
    actor5 = Actor(name='Adam Sandler')
    actor5.add()
    actor6 = Actor(name='Jacky Chan')
    actor6.add()

    movie1 = Movie(
        name='Maleficent',
        image_link=(
            'https://m.media-amazon.com/images/M/MV5BMjAwMzAzMzExOF5BMl5BanBnX'
            'kFtZTgwOTcwMDA5MTE@._V1_UY1200_CR90,0,630,1200_AL_.jpg'))
    movie1.add()
    movie2 = Movie(name='Mr and MRS Smith')
    movie2.add()
    movie3 = Movie(name='Avatar')
    movie3.add()
    movie4 = Movie(name='Joker')
    movie4.add()
    movie5 = Movie(name='Click')
    movie5.add()
    movie6 = Movie(name='Rush Hour')
    movie6.add()

    actor4.add_movie(movie1)
    actor4.add_movie(movie2)
    actor5.add_movie(movie5)
    movie6.add_actor(actor6)


class Actor(db.Model):
    __tablename__ = 'Actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    image_link = db.Column(db.String(500))
    movies = db.relationship(
        'MovieActor', backref='actor', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return self.name

    def get_movies(self):
        movies = [movie.movie for movie in self.movies]
        return movies

    def movies_formate(self):
        movies = self.get_movies()
        movies_formated = [movie.brief_formate() for movie in movies]
        return movies_formated

    def add_movie(self, movie):
        movie_actor = MovieActor()
        movie_actor.actor = self
        movie_actor.movie = movie
        db.session.add(movie_actor)
        db.session.commit()

    def delete_movie(self, movie):
        movie_actor = MovieActor.query.filter_by(
                actor_id=self.id,
                movie_id=movie.id
            ).first()
        movie_actor.delete()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def brief_formate(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_link': self.image_link
        }

    def detail_formate(self):
        return {
            'id': self.id,
            'name': self.name,
            'movies': self.movies_formate(),
            'image_link': self.image_link
        }


class Movie(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    image_link = db.Column(db.String(500))
    actors = db.relationship(
        'MovieActor',
        backref='movie',
        cascade='all, delete-orphan',
        lazy=True)

    def __repr__(self):
        return self.name

    def get_actors(self):
        actors = [actor.actor for actor in self.actors]
        return actors

    def actors_formate(self):
        actors = self.get_actors()
        actors_formated = [actor.brief_formate() for actor in actors]
        return actors_formated

    def add_actor(self, actor):
        movie_actor = MovieActor()
        movie_actor.actor = actor
        movie_actor.movie = self
        db.session.add(movie_actor)
        db.session.commit()

    def delete_actor(self, actor):
        movie_actor = MovieActor.query.filter_by(
            actor_id=actor.id, movie_id=self.id).first()
        movie_actor.delete()

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def brief_formate(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_link': self.image_link
        }

    def detail_formate(self):
        return {
            'id': self.id,
            'name': self.name,
            'actors': self.actors_formate(),
            'image_link': self.image_link
        }


class MovieActor(db.Model):
    __tablename__ = 'MovieActor'
    actor_id = db.Column(
        db.Integer,
        db.ForeignKey('Actors.id'),
        nullable=False)
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('Movies.id'),
        nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('actor_id', 'movie_id'),
    )

    def delete(self):
        db.session.delete(self)
        db.session.commit()
