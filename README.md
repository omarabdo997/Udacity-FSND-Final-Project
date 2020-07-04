# FSND Final Project Capstone

## Casting Agency

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.
Casting Agency is a backend app, this app has 2 models Movie and Actor and they have many to many realtionship it has multiple APIs most of them have authentications required and the app has 45 test cases for all the APIs.

## Motivation

This app was created as the last project of Udacity FSND to put the learning of ORM, APIs, Authentication, Testing, Documentation and Deployment to practice.

## Project Dependencies

Python 3.6 or higher - (https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

Virtual Enviroment - its recommended to have it installed when working with a python project (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

PIP Dependencies - Once you have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```

## Hosting

The application is hosted on https://casting-agency997.herokuapp.com/

And hosted locally on http://localhost:8080/

## Running The Development Server

In order to run the application locally you will need to do the following:

1- Create 2 postgres databases one for testing and one for the application.

2- Open 'setup.sh' file in project directory and put the two databases urls in the DATABASE_URL and the TEST_DATABASE_URL.

3- Create a virtual enviroment and run it.

4- Install all the requirements by navigating to the project directory and running:
```bash
pip install -r requirements.txt
```

5- Go to the 'setup.sh' file and make sure that the enviromental variables CASTING_ASSISTANT_TOKEN, CASTING_DIRECTOR_TOKEN, and EXECUTIVE_PRODUCER_TOKEN have valid tokens (no need to do this withing 24 hours of submitting the project)

6- Run the following commands to obtain the enviromental variables and create the tables:
```bash
source setup.sh
python manage.py db upgrade
```

7- Run the following command to test the application:
```bash
python test_app.py
```

8- If all the test cases have passed run the following command to start the server
```bash
python app.py
```

## Roles and permissions


The application has the following roles:

Casting Assistant - (permissions: get:actor-details, get:movie-details)

Casting Director - (permissions: get:actor-details, get:movie-details, post:actors, patch:actors, patch:movies, delete:actors)

Executive Producer - (permissions: get:actor-details, get:movie-details, post:actors, post:movies, patch:actors, patch:movies, delete:actors, delete:movies, post:movies-to-actors, delete:movies-from-actors) 


## End Points


### Errors:

description part in the errors return the exact reason of why this error occured.

400-bad request:

returns 

    {
        'success': False,
        'error': 400,
        'message': 'bad request',
        'description': error.description
    }

401-unauthorized:

returns 

    {
        'success': False,
        'error': 401,
        'message': 'unauthorized',
        'description': error.description
    }

403-forbidden:

returns 

    {
    'success': False,
    'error': 403,
    'message': 'forbidden',
    }

404-resource not found:

returns 

    {
        'success': False,
        'error': 404,
        'message': 'resource not found',
        'description': error.description
    }

405-method not allowed:

returns 

    {
        'success': False,
        'error': 405,
        'message': 'method not allowed',
        'description': error.description
    }

422-unprocessable:
returns 

    {
        'success': False,
        'error': 422,
        'message': 'unprocessable',
    }

500-internal server error:
returns

    {
        'success': False,
        'error': 500,
        'message': 'internal server error',
        'description': error.description
    }


### APIs

GET '/actors'

POST '/actors'

GET '/actors/{actor_id}'

PATCH '/actors/{actor_id}'

DELETE '/actors/{actor_id}'

POST '/actors/{actor_id}/movie'

DELETE '/actors/{actor_id}/movie/{movie_id}'

GET '/movies'

POST '/movies'

GET '/movies/{movie_id}'

PATCH '/movies/{movie_id}'

DELETE '/movies/{movie_id}'

POST '/movies/{movie_id}/actor'

DELETE '/movies/{movie_id}/actor/{actor_id}'


Note: Before testing the APIs please make sure to set the variable executive_producer_token to the value EXECUTIVE_PRODUCER_TOKEN from the 'setup.sh' file
-----------------------------------------------
GET '/actors'

-Returns actors paginated.

-Returns a success value, total_actors value and a list of actors objects each object has id, image_link, and name values.

-Supports paging and returns a maximum of 8 actors.

-Doesn't require an authentication.

sample:

curl -X GET https://casting-agency997.herokuapp.com/actors?page=1

    {
        "actors": [
            {
                "id": 1,
                "image_link": null,
                "name": "Angelina Joliey"
            },
            {
                "id": 2,
                "image_link": null,
                "name": "Brad Pitt"
            },
            {
                "id": 3,
                "image_link": null,
                "name": "Kevin Costner"
            },
            {
                "id": 4,
                "image_link": null,
                "name": "Mel Gibson"
            },
            {
                "id": 5,
                "image_link": null,
                "name": "Adam Sandler"
            },
            {
                "id": 6,
                "image_link": null,
                "name": "Tom Hanks"
            },
            {
                "id": 7,
                "image_link": null,
                "name": "Will Smith"
            },
            {
                "id": 8,
                "image_link": null,
                "name": "Leonardo Dicaprio"
            }
        ],
        "success": true,
        "total_actors": 10
    }


-----------------------------------------------
POST '/actors'

-Adds new actors.

-Returns a success value.

-Takes 2 inputs name and image_link but image_link is optional.

-Requires (post:actors) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -H "Content-Type: application/json" -X POST https://casting-agency997.herokuapp.com/actors -d '{"name": "Johnny Depp", "image_link": "https://media1.popsugar-assets.com/files/thumbor/SzH64gnTws09oWZaWy6RrXpq6gI/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2018/07/13/027/n/1922398/a3f0a2e05b4938311543f8.44799569_/i/Johnny-Depp.jpg"}'
 
    {
        "success": true
    }


-----------------------------------------------
GET '/actors/{actor_id}'

-Returns detailed information about the selected actor(here it's his movies).

-Returns a success value, id value, image_link value, name value and a list of movies objects that this actor has acted in each object has id, image_link, and name values.

-Requires (get:actor-details) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -X GET https://casting-agency997.herokuapp.com/actors/2
 
    {
        "id": 2,
        "image_link": null,
        "movies": [
            {
                "id": 5,
                "image_link": null,
                "name": "Mr. & Mrs. Smith"
            },
            {
                "id": 7,
                "image_link": null,
                "name": "Troy"
            }
        ],
        "name": "Brad Pitt",
        "success": true
    }


-----------------------------------------------
PATCH '/actors/{actor_id}'

-Updates the selected actor.

-Returns a success value.

-Takes two inputs image_link and name both are optional.

-Requires (patch:actors) permission.


sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -H "Content-Type: application/json" -X PATCH https://casting-agency997.herokuapp.com/actors/2 -d '{"image_link": "https://www.cheatsheet.com/wp-content/uploads/2020/06/Brad-Pitt-16-1024x681.jpg"}'
 
    {
      "success": true
    }


-----------------------------------------------
DELETE '/actors/{actor_id}'

-Deletes the selected actor.

-Returns a success value.

-Requires (delete:actors) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -H "Content-Type: application/json" -X DELETE https://casting-agency997.herokuapp.com/actors/11
 
    {
      "success": true
    }


-----------------------------------------------
POST '/actors/{actor_id}/movie'

-Adds an existing movie in the app to the selected actor list of movies

-Returns a success value.

-Takes 1 input movie_id.

-Requires (post:movies-to-actors) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -H "Content-Type: application/json" -X POST https://casting-agency997.herokuapp.com/actors/12/movie -d '{"movie_id":20}'
 
    {
      "success": true
    }


-----------------------------------------------
DELETE '/actors/{actor_id}/movie/{movie_id}'

-Deletes the selected movie from the actors movies list (the movie is not deleted from the app)

-Returns a success value.

-Requires (delete:movies-from-actors) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -X DELETE https://casting-agency997.herokuapp.com/actors/12/movie/20
 
    {
      "success": true
    }


-----------------------------------------------
GET '/movies'

-Returns movies paginated.

-Returns a success value, total_movies value and a list of movies objects each object has id, image_link, and name values.

-Supports paging and returns a maximum of 8 movies.

-Doesn't require an authentication.

sample:

curl -X GET https://casting-agency997.herokuapp.com/movies?page=1
 
    {
        "movies": [
            {
                "id": 1,
                "image_link": null,
                "name": "Lethal Weapon"
            },
            {
                "id": 2,
                "image_link": null,
                "name": "Brave Heart"
            },
            {
                "id": 4,
                "image_link": null,
                "name": "What Women Want"
            },
            {
                "id": 5,
                "image_link": null,
                "name": "Mr. & Mrs. Smith"
            },
            {
                "id": 6,
                "image_link": null,
                "name": "Wanted"
            },
            {
                "id": 7,
                "image_link": null,
                "name": "Troy"
            },
            {
                "id": 8,
                "image_link": null,
                "name": "Dance With Wolves"
            },
            {
                "id": 9,
                "image_link": null,
                "name": "Man Of Steel"
            }
        ],
        "success": true,
        "total_movies": 18
    }

-----------------------------------------------
POST '/movies'

-Adds new movies.

-Returns a success value.

-Takes 2 inputs name and image_link but image_link is optional.

-Requires (post:movies) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -H "Content-Type: application/json" -X POST https://casting-agency997.herokuapp.com/movies -d '{"name": "Pirates Of The Cariebian"}'

    {
      "success": true
    }


-----------------------------------------------
GET '/movies/{movie_id}'

-Returns detailed information about the selected movie (here it's the movie actors).

-Returns a success value, id value, image_link value, name value and a list of actors objects that have acted in this movie object has id, image_link, and name values.

-Requires (get:movie-details) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -X GET https://casting-agency997.herokuapp.com/movies/2
 
    {
        "actors": [
            {
                "id": 4,
                "image_link": null,
                "name": "Mel Gibson"
            }
        ],
        "id": 2,
        "image_link": null,
        "name": "Brave Heart",
        "success": true
    }


-----------------------------------------------
PATCH '/movies/{movie_id}'

-Updates the selected movie.

-Returns a success value.

-Takes two inputs image_link and name both are optional.

-Requires (patch:movies) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -H "Content-Type: application/json" -X PATCH https://casting-agency997.herokuapp.com/movies/20 -d '{"name":"Pirates OF The Cariebian 2"}'
 
    {
      "success": true
    }


-----------------------------------------------
DELETE '/movies/{movie_id}'

-Deletes the selected movie.

-Returns a success value.

-Requires (delete:movies) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -H "Content-Type: application/json" -X DELETE https://casting-agency997.herokuapp.com/movies/21
 
    {
      "success": true
    }


-----------------------------------------------
POST '/movies/{movie_id}/actor'

-Adds an existing actor in the app to the selected movie list of actors.

-Returns a success value.

-Requires (post:movies-to-actors) permission.

-Takes 1 input actor_id.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -H "Content-Type: application/json" -X POST https://casting-agency997.herokuapp.com/movies/21/actor -d '{"actor_id":20}'
 
    {
      "success": true
    }


-----------------------------------------------
DELETE '/movies/{movie_id}/actor/{actor_id}'

-Deletes the selected actor from the movie actors list (the actor is not deleted from the app)
-Returns a success value.

-Requires (delete:movies-from-actors) permission.

sample:

curl -H "Authorization: Bearer ${executive_producer_token}" -X DELETE https://casting-agency997.herokuapp.com/movies/22/actor/20
 
    {
      "success": true
    }

