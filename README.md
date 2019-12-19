# motherducker
SecurityLab project 3 - Team Aave

* Velid
* Elom
* Lana
* Teemu
* Pyry
* Waltteri



# Motherducker to Docker
* docker installed
* docker-compose installed


If there are files not owned by your user 'docker':
> sudo chown -R docker:docker .


> cp _settings.py motherducker/settings.py


run on your project folder to start containers:
> docker-compose up 


You should be able to develop 'live' with the container running.
You have to re-build the image if you add requirements.
> docker-compose build




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

