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

## Running The Development Server

In order to run the application locally you will need to do the following:
1- Create 2 postgres databases one for testing and one for the application.
2- Open 'setup.sh' file in project directory and put the two databases urls in the DATABASE_URL and the TEST_DATABASE_URL.
3- Create a virtual enviroment and run it.
4- Install all the requirements by navigating to the project directory and running
'''bash
pip install -r requirements.txt
'''
5- Go to the 'setup.sh' file and make sure that the enviromental variables CASTING_ASSISTANT_TOKEN, CASTING_DIRECTOR_TOKEN, and EXECUTIVE_PRODUCER_TOKEN have valid tokens (no need to do this withing 24 hours of submitting the project)
6- Run the following commands to obtain the enviromental variables and test the server
'''bash
source setup.sh
python test_app.py
'''
7- If all the test cases have passed simply run the following command to start the server
'''bash
python app.py
'''

## Roles and permissions


The application has the following roles:

Casting Assistant - (permissions: get:actor-details, get:movie-details)

Casting Director - (permissions: get:actor-details, get:movie-details, post:actors, patch:actors, patch:movies, delete:actors)

Executive Producer - (permissions: get:actor-details, get:movie-details, post:actors, post:movies, patch:actors, patch:movies, delete:actors, delete:movies, post:movies-to-actors, delete:movies-from-actors) 


## End Points


### Errors:

description part in the errors return the exact reason of why this error occured.

400-bad request:
returns {
            'success': False,
            'error': 400,
            'message': 'bad request',
            'description': error.description
        }

401-unauthorized:
returns {
            'success': False,
            'error': 401,
            'message': 'unauthorized',
            'description': error.description
        }

403-forbidden:
returns {
            'success': False,
            'error': 403,
            'message': 'forbidden',
         }

404-resource not found:
returns {
            'success': False,
            'error': 404,
            'message': 'resource not found',
            'description': error.description
        }

405-method not allowed:
returns {
            'success': False,
            'error': 405,
            'message': 'method not allowed',
            'description': error.description
        }

422-unprocessable:
returns {
            'success': False,
            'error': 422,
            'message': 'unprocessable',
        }

500-internal server error:
returns {
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


-----------------------------------------------
GET '/actors'
-Returns a success value, total_actors value and a list of actors objects each object has id, image_link, and name values.
-Supports paging and returns a maximum of 8 actors.
-Doesn't require an authentication.

sample:
curl -X GET http://localhost:8080/actors?page=1
 
{
  "actors": [
    {
      "id": 1, 
      "image_link": null, 
      "name": "Leonardo Dicaprio"
    }, 
    {
      "id": 2, 
      "image_link": null, 
      "name": "Brad Pitt"
    }, 
    {
      "id": 3, 
      "image_link": null, 
      "name": "Jennifer Aniston"
    }, 
    {
      "id": 4, 
      "image_link": "https://i.insider.com/5e9dde0992e8ba7bde291467?width=1100&format=jpeg&auto=webp", 
      "name": "Angelina Jolie"
    }, 
    {
      "id": 5, 
      "image_link": null, 
      "name": "Adam Sandler"
    }, 
    {
      "id": 6, 
      "image_link": null, 
      "name": "Jacky Chan"
    }
  ], 
  "success": true, 
  "total_actors": 6
}


-----------------------------------------------
POST '/actors'
-Returns a success value.
-Requires (post:actors) permission.
-Takes 2 inputs name and image_link but image_link is optional

sample:
curl -H "Authorization: Bearer ${casting_director_token}" -H "Content-Type: application/json" -X POST http://localhost:8080/actors -d '{"name": "Johnny Depp", "image_link": "https://media1.popsugar-assets.com/files/thumbor/SzH64gnTws09oWZaWy6RrXpq6gI/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2018/07/13/027/n/1922398/a3f0a2e05b4938311543f8.44799569_/i/Johnny-Depp.jpg"}'
 
{
  "success": true
}


-----------------------------------------------
GET '/actors/{actor_id}'
-Returns a success value, id value, image_link value, name value and a list of movies objects that this actor has acted in each object has id, image_link, and name values.
-Requires (get:actor-details) permission

sample:
curl -X GET http://localhost:8080/actors?page=1
 
{
  "actors": [
    {
      "id": 1, 
      "image_link": null, 
      "name": "Leonardo Dicaprio"
    }, 
    {
      "id": 2, 
      "image_link": null, 
      "name": "Brad Pitt"
    }, 
    {
      "id": 3, 
      "image_link": null, 
      "name": "Jennifer Aniston"
    }, 
    {
      "id": 4, 
      "image_link": "https://i.insider.com/5e9dde0992e8ba7bde291467?width=1100&format=jpeg&auto=webp", 
      "name": "Angelina Jolie"
    }, 
    {
      "id": 5, 
      "image_link": null, 
      "name": "Adam Sandler"
    }, 
    {
      "id": 6, 
      "image_link": null, 
      "name": "Jacky Chan"
    }
  ], 
  "success": true, 
  "total_actors": 6
}


-----------------------------------------------
GET '/questions'
-Returns two lists one of categories values and one of questions objects, and a current_category value, success value, and total_questions value
-Results are paginated in groups of 10 include a request argument to choose page number starting from 1

samlpe:
curl -X GET http://localhost:5000/questions?page=1

{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}

-----------------------------------------------
DELETE '/questions/{question_id}'
-Deletes the question of the given ID if it exists, and returns two lists one of categories values and one of questions objects, and a current_category value, success value, and total_questions value paginated in group of 10 to update front-end

sample:
curl -X DELETE http://localhost:5000/questions/5?page=1

{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 18
}

-----------------------------------------------
POST '/questions'
-Creates a new question using the submitted question, answer, difficulty and category. Returns a success value.

sample:
curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is the first person to walk on the moon", "answer":"Neil Armstrong", "difficulty":"5", "category":"4"}'

{
  "success": true
}

-----------------------------------------------
POST '/questions/search'
-Searches for questions using the submitted searchTerm, Returns success value, total_questions value and a list of questions with question phrase which the searchTerm is subset of, and paginates questions in groups of 10

sample:
curl http://localhost:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"What"}'

{
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 8
}

-----------------------------------------------
GET '/categories/{category_id}/questions'
-Return questions with the given category_id if the questions exist.
-Return success value, current_category value,total_questions value, and a list of questions with the given category id and paginates them in groups of 10.

sample:
curl -X GET http://localhost:5000/categories/2/questions

{
  "current_category": null, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}

-----------------------------------------------
POST '/quizzes'
-Return a randomized question object, and success value using the submitted quiz_category object and previous_questions list, where the randomized question not in the previous_questions list and matches with the submitted quiz category
-To retrieve question with any category set quiz_category["id"]=0

sample:
curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Art","id":2}}'

{
  "question": {
    "answer": "Escher", 
    "category": 2, 
    "difficulty": 1, 
    "id": 16, 
    "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
  }, 
  "success": true
}

















































