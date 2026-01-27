# Djora
> Djora is a custom-built CMS powered by Django, designed for flexible content management.

#### Setup

##### Dependencies

- Python 3.14
- postgres 18

> The following steps will walk you through installation on a Mac. Linux should be similar. It's also possible to develop 
on a Windows machine, but I have not documented the steps. If you've developed Django apps on Windows, you should have little problem getting up and running.

Run the application in your local development server:

```bash
virtualenv venv --python=python3.14
source venv/bin/activate
pip install -r requirements.txt
./manage.py makemigrations user
./manage.py migrate user
./manage.py migrate
./manage.py createsuperuser
./mangae.py runserver
```
