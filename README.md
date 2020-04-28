# eon-payment

This is a microsevice based payment django project for BITS EOn.

## Important Features

- Python 3+
- Django 2.0+
- Database MongoDb
- Uses Pipenv, Virtualenv

## Installation

```bash
$ git clone https://github.com/bits-pgp-fse/eon-backend-payment.git
$ virtualenv <virtual_env_name_of_your_choice>
$ source <virtual_env_name_of_your_choice>/bin/activate
$ pip install -r requirements.txt
```
https://github.com/bits-pgp-fse/eon-backend-payment.git
## Environment variables

```
#DJANGO
DECODE_KEY= <secret>
SECRET_KEY=<something_very_secret>
DB_NAME=<db_name>
DB_USERNAME=<db_user>
DB_PASSWORD=<your_password>
DB_HOSTNAME=localhost
DB_PORT=27017
```

## Run Server

```bash
$ python manage.py runserver
```
