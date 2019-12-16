# Motherducker to Docker
* docker installed
* docker-compose installed

## steps
### needed files
You only want to have these when you start
* project_folder
* project_folder/requirements.txt
* project_folder/Dockerfile
* project_folder/docker-compose.yml
* project_folder/db_init
* project_folder/db_init/init.sql

In project folder run:
> docker-compose run web django-admin startproject motherducker .

If there are files not owned by your user 'docker':
> sudo chown -R docker:docker project_folder/.

Then edit motherducker/settings.py and edit the DATABASE section.
> vim motherducker/settings.py

> DATABASES = {
>     'default': {
>         'ENGINE': 'django.db.backends.postgresql',
>         'NAME': 'db_name',
>         'USER': 'db_user',
>         'PASSWORD': 'db_user',
>         'HOST': 'db',
>         'PORT': '5432',
>     }
> }



run on your project folder to start containers:
> docker-compose up 


