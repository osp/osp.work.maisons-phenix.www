# Phenix Django Project

## Prerequisites

- python &gt;= 2.5
- python-dev
- libxml2-dev
- lixslt1-dev
- libsndfile1-dev
- pip
- virtualenv

## Installation

### Creating the environment

Create a virtual python environment for the project.
If you're not using virtualenv you may skip this step.

```bash
virtualenv --no-site-packages phenix-env
cd phenix-env
source bin/activate
```

### Clone the code

```bash
git clone <URL_TO_GIT_REPOSITORY> phenix
```

### Install the requirements

```bash
cd phenix
pip install -r requirements/common.txt
```

Depending on the your profile (development or production), install the extra
requirements.

In a development environment, run:

```bash
cd phenix
pip install -r requirements/dev.txt
```
In a production environment, run:

```bash
cd phenix
pip install -r requirements/prod.txt
```

### Configure the project

```bash
cp phenix/local_settings.example.py phenix/local_settings.py
vi phenix/local_settings.py
```

### Synchronize the database

```bash
python manage.py syncdb
python manage.py migrate
```

## Run the project

```bash
python manage.py runserver
```

Open you browser at <http://localhost:8000>.
