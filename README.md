# API backend usage

The backend is written in **Python** and uses **Django** framework.
Here's the **How to** install and start the **api server**

## Link the backend simulation library

	ln -s [simulation_repo/path] ./socket_api/api/sockets/chesssimul

## Create virtual environment (optional)

**Create** a virtual environment with python :

	python -m venv [venv directory name i.e .venv]

**Activate** an existing virtual environment :

* In a Linux environment :

		source .venv/bin/activate
* In a windows environment :

		.venv\Scripts\activate.bat

**Exit** a virtual environment :

	deactivate

## Install python pre-requisites

Install requirements.txt file with python pip (inside your venv e.g.):

	python -m pip install -r requirements.txt


## Create and migrate database

	python manage.py migrate

## Start the server

1. Go to the **Django** root directory
2. Start the server :
	
		python manage.py runserver

## Socket.io routes

You can find all **socket.io** defined routes inside
 
    chess-API/socket_api/api/sockets/*_handler.py
    
Every **@sio.event** annotated function is a valid route on which the server is listening.
From the client, use :

    socket.emit('[route name]', [optional data object i.e {'uuid': 'abc'}])
    
And :

    socket.on('[response route name]')
    
To emit and receive to and from a socket.
