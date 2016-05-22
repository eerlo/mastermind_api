# Mastermind Rest API
####The Mastermind board game now available as an REST API.

Example running on heroku [https://mastermind-api.herokuapp.com/docs/](https://mastermind-api.herokuapp.com/docs/)

Mastermind [(Wikipedia Link)](https://en.wikipedia.org/wiki/Mastermind_(board_game)) is a code-breaking game for two players.

[Rules Here](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Gameplay_and_rules)

This API was build using:

* Python 2.7
* Django 1.9.6
* Django Rest Framework 3

To access the docs, with the server running, just go to the "/docs" url.


## Run locally

1. Create a new python virtualenv:
    ```virtualenv new_env```

2. Activate it on your terminal session:
    ```source new_env/bin/activate```

3. Install the python requirements:
    ```pip install -r requirements.txt```

4. Create the database(sqlite3 by default on settings.py, you can change it):
    ```python manage.py migrate```

5. Create the database(sqlite3 by default on settings.py, you can change it):
    ```python manage.py runserver```

6. View and play with the interactive API docs, acessing [http://localhost:8000/docs/](http://localhost:8000/docs/)

