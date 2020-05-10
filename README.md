# car-supply-chain

This is a car supply chain app built as the Ayulla Software Engineering Tryout Task (ASETT)

The project is built using Django web framework

## Requirements
 - Python 3.7.6
 - Django 3.0.5
 - Django Crispy Forms
 - Django guardian

## Installation
To install this app, clone this repo and run
```
cd car-supply-chain
```
then, create a virtual environment (pyenv, venv, virtualenv, etc). Then run, 
```
pip install -r requirements.txt
```
to install all necessary dependencies.
Then run 
```
python manage.py migrate
```
to create database tables (this requires that postgres be previously set up and the database credentials in settings.py are used).

To populate the database, run 
```
python manage.shell

>>> from populate import populate_database
>>> populate_database()
```
To create a superuser for the admin panel, run
```
python manage.py createsuperuser
```
and fill the required fields.
Then, run 
```
python manage.py runserver
```
to start the development server.
Open http://localhost:8000/ to access the user.

The app is also online on https://car-supply.herokuapp.com.