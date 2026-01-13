# mailValidationBot

> mailValidationBot is a tool designed to validate email addresses. Users can submit one or more email addresses, and the bot checks whether they are valid.

### Setup:

```bash
git clone https://github.com/mbrsagor/mailValidationBot.git
cd mailValidationBot
source venv/bin/activate
pip install -r requirements.txt
```

> Added environment into .env file. And then,

```bash
python manage.py makemigrations
python manage.py migrate
```
###### Run Services

> Start the Celery worker:

```bash
celery -A mailValidationBot worker --loglevel=info;
```
