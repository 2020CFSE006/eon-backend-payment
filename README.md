
# EOn Payment

This is a microservice based payment django app for BITS EOn.

## Prerequisites
- Mongo

Note: Make sure that Mongo is installed and running on your system. 
If your don't have mongo. Please installed it from below link.

- Mongo - https://docs.mongodb.com/manual/installation/

## Important Features

- Python 3+
- Django 2.0+
- Database Mongo
- Uses Virtualenv

## Installation
Note: If you have the zip of this project, then skip the git clone command and extract the project.

```bash
$ git clone https://github.com/bits-pgp-fse/eon-backend-payment.git
$ virtualenv <virtual_env_name_of_your_choice>
$ source <virtual_env_name_of_your_choice>/bin/activate
$ cd eon-backend-payment
$ pip install -r requirements.txt
```

## Environment variables

```
#DJANGO
DECODE_KEY=<secret>
SECRET_KEY=<something_very_secret>
DB_NAME=<db_name>
DB_USERNAME=<db_user>
DB_PASSWORD=<your_password>
DB_HOSTNAME=localhost
DB_PORT=27017
```
Note: Use different port to run payment app simultaneously with eon-backend app


## Run Server

```bash
$ python3 manage.py migrate
$ python3 manage.py runserver 8001
```

### Main Libraries Used

- Django-Rest-Framework: 
  Django REST framework is a powerful and flexible toolkit for building Web APIs. 
  It gives us multiple features that combine deeply with Django's existing structures, 
  supporting us build RESTful HTTP resources that agree to the models.

  https://www.django-rest-framework.org/
  
- Djongo:
  It provides the mongo connection for the project with django.
   
  https://nesdis.github.io/djongo/get-started/
