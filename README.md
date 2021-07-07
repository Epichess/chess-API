# API backend usage

The backend is written in **Python** and uses **Django** framework.
Here's the **How to** install and start the **api server**


## Create virtual environment (optional)

Create a virtual environment with python :

	python -m venv [venv directory name i.e .venv]

Activate an existing virtual environment :

* In a Linux environment :

		source .venv/bin/activate
* In a windows environment :

		.venv\Scripts\activate.bat

Install requirements.txt file with python pip :

	python -m pip install -r requirements.txt

Exit a virtual environment :

	deactivate

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