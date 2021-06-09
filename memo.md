# Create venv
python3 -m venv project_venv

# Activate venv
source project_venv/bin/activate.fish

# Install django
pip install django

# Create django project
django-admin startproject mysite

# Run server
python manage.py runserver





# Create the project directory
mkdir tutorial
cd tutorial

# Create a virtual environment to isolate our package dependencies locally
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtual environment
pip install django
pip install djangorestframework

# Set up a new project with a single application
django-admin startproject tutorial .  # Note the trailing '.' character
cd tutorial
django-admin startapp quickstart
cd ..