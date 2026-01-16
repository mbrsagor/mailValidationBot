# mailValidationBot

> MailValidationBot is a high-performance tool designed to validate email addresses in bulk. It checks syntax, MX records, and SMTP availability (where network permits).

### Prerequisites

- **Python 3.10+**
- **Redis** (Required for background processing)

### Setup:

1. **Clone and Install**

   ```bash
   git clone https://github.com/mbrsagor/mailValidationBot.git
   cd mailValidationBot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Create a `.env` file in the root directory (see `.env.example` if available) or simply ensure standard Django env vars are set.

3. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### How to Run

You need **three** separate terminal windows running:

**1. Redis Server**

```bash
redis-server
```

**2. Celery Worker (Background Tasks)**

```bash
celery -A mailValidationBot worker --loglevel=info
```

**3. Django Web Server**

```bash
python manage.py runserver
```

Access the tool at: `http://127.0.0.1:8000/`

### ⚠️ Note on Accuracy (Port 25)

This tool attempts to connect to email servers (Port 25) for maximum accuracy.

- **If Port 25 is Open**: It will verify if the specific user exists (e.g., `user@gmail.com`).
- **If Port 25 is Blocked (most home ISPs/Cloud defaults)**: It will **automatically fallback** to Domain-Only validation. It will verify that `gmail.com` exists and accepts emails, but cannot verify if the specific user exists. This is still sufficient for cleaning lists of typos and invalid domains.
