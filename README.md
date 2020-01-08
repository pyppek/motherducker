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