# motherducker
SecurityLab project 3 - Team Aave

* Velid
* Elom
* Lana
* Teemu
* Pyry
* Waltteri


## TODO
### Week 1
| Task                                        | Assignee        | Status            |
|:--------------------------------------------|:---------------:|:-----------------:|
|GitHub repository                            | Pyry            |:heavy_check_mark: |
|project management method                    | Velid           |:heavy_check_mark: |
|webinterface tech                            | Lana            |:x:                |
|how to connect rubberducky to webinterface   | Teemu           |:x:                |
|how to ducky script                          | Walde           |:heavy_check_mark: |
|usb to rubberducky                           | Velid           |:x:                |
|motherducker functionality                   | Pyry            |:x:                |
|secure coding practices                      | Elom            |:x:                |

# Setup Django project
### Have Python 3.5+ 
### Create a virtual environment (if u have pycharm u can do this in File > Settings > Project: motherducker > Project interpreter > click the cogwheel in the top right corner > Add > New Environment > Ok )
### Once in the virtual environment (u will see (venv) in front of your terminal line) u can install the required packages by navigating to the folder with requirements.txt and enter the command 
* "pip install -r requirements.txt"
### After the requirements are installed run: 
* "python manage.py makemigrations"
* "python manage.py migrate"
* "python manage.py createsuperuser"
* "python manage.py runserver"


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

run on your project folder to start containers:
> docker-compose up 


