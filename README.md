# API Documentation
Welcome to the API documentation! 
This document provides information on how to access and explore the API endpoints

## Tech Stack
- Python: A powerful programming language used for the backend development.
- Django REST framework: A powerful and flexible toolkit for building Web APIs.
- Git: A distributed version control system used for tracking changes in source code during software development.

## Prerequisite Download
1. Python
2. Vscode
3. PostgreSQL

## How to Run the Project

To run the project on your local machine, follow these steps:

1. Open your terminal or command prompt. Navigate to the directory where you want to clone the repository. e.g cd or mkdir ..
2. Setup Virtual enviroemnt e.g virtualenv .. && source ../bin/activate
3. Use the following command to clone the repository: git clone https://github.com/RydahApp/Server.git
4. Next, install the project's dependencies;by using this command. python -m pip freeze > requirements.txt
5. Create a `.env` file in the root of the project and set the required environment variables:

    ```bash
    export DJANGO_SETTINGS_MODULE="rydah.settings.dev"
    export SECRET_KEY=<your-secret-key>
    export DB_NAME=<your-database-name>
    export DB_USER=<your-database-user>
    export DB_PASSWORD=<your-database-password>
    export DB_HOST=<your-database-host>
    export DB_PORT=<your-database-port>
    export SENDGRID_KEY=<your-sendgrid-key>

      
    > **__NOTE__**: You can generate and copy a secret key(`SECRET_KEY`) for the django app by opening a django shell `python manage.py shell` and running;

    ```python
    from django.core.management.utils import get_random_secret_key  
    get_random_secret_key()
    ```

- Set up the database:
    - Ensure you have PostgreSQL installed and running.
    - Create a database and user according to the value in your `.env`'s file.
- Run makemigrations:
    ```bash
    python manage.py makemigrations
- Run migrations:
    ```bash
    python manage.py migrate
- Run development server:
    ```bash
    python manage.py runserver
    ```
## How TO Test
Running Tests with Coverage for the Entire Project
- coverage run -m pytest

specified file
- coverage run -m pytest apps/auths/tests/test_serializers.py
To see print staements coverage run -m pytest apps/auths/tests/test_serializers.py - s
Coverage Reports
- coverage report

HTML Report
- coverage html


## Resolving Database Conflict / Migration to Database

- Delete Postgres Database from pgAdmin
- Create a new Database with pdAdmin
- Delete all Migration folders
- Run makemigrations:
    ```bash
    python manage.py makemigrations <app_name with users models goes first>
- Run migrations:
    ```bash
    python manage.py migrate
- Run development server:
    ```bash
    python manage.py runserver
    ```

 