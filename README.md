
# Campaign Data API - Unique Filter Values

This API provides unique filter values for campaign data based on the uploaded file ID. It extracts various filter fields like company, year, campaign, category, offer, product, source, and segment from the campaign data and returns them in a structured format.

## Requirements

- Python 3.x
- Django 3.x or higher
- Django REST Framework 3.x or higher
- MySQL (local or remote)
- Django CORS headers (for handling cross-origin requests)

## Installation

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository_url>
cd <project_directory>
```

### 2. Install Dependencies

If you already have Python and `pip` installed, use the following command to install all the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

- Ensure that you have MySQL installed and running on your local machine (or a remote MySQL server).
- Create a new database called `campaignhubdb`:

```sql
CREATE DATABASE campaignhubdb;
```

- In `settings.py`, update the `DATABASES` configuration to connect Django to your MySQL database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'campaignhubdb',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password'
    }
}
```

### 4. Run Migrations

Once the database is set up, run the migrations to set up the necessary tables:

```bash
python manage.py migrate
```

### 5. Run the Development Server

Start the Django development server to test the API:

```bash
python manage.py runserver
```

### 6. Access the API

Once the server is running, you can access the API by visiting the following URL:

```
http://127.0.0.1:8000/
```

## CORS Configuration

If you're using this API with a frontend hosted on a different domain, make sure to configure CORS by following the instructions in the [django-cors-headers documentation](https://pypi.org/project/django-cors-headers/).

You can add `'corsheaders'` to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # Other apps
    'corsheaders',
]

MIDDLEWARE = [
    # Other middleware
    'corsheaders.middleware.CorsMiddleware',
]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
