
# Introduction

This project extend the flask-framework project that i have initiated years ago. As it has been migrated into a fully integrable python package, it is now easier to integrate code within.
#

## Configuration

The configuration is json/yaml ready as inherited from the Configuration module in the flask-framework package. Example bellow:

```yml
SERVER_ENV:
    APP_NAME: Flask
    # your secret key for managing sessions
    APP_KEY : ${SECURED_FLASK_TOKEN}
    #DEV, UAT or PROD
    ENV: ${FLASK_ENV} 
    BIND:
        ADDRESS :  0.0.0.0
        PORT: 4200
    WORKERS: sync
    CAPTURE: false
    STATIC_PATH: static
    TEMPLATE_PATH: template
    SESSION: redis
    THREADS_PER_CORE: 16
    # Mainly used for flask_framework.server and flask_framework.wsgi for logging.  
    # Use env LOG_FILE=<your log file path> for the flask_framework.app 
    LOG:
        DIR: ${LOG_DIR}
        LEVEL: ${LOG_LEVEL}

DATABASE:
    default: cms
    cms:
        driver: mysql+pymysql
        # Your database user
        user: *******
        # Your database password
        password: ********
        database: flask
        address: localhost
        # readonly is true or false whether you want the server to create database schema. 
        readonly: false
        # modules is the name of the module where you store your database models 
        models: cms

# this will alow you to setup the configuration of flask. All variables will bes added to flask.config
FLASK:
    CONFIG:

# Registered custom services for cache and custom services used by your WebApp or flask-cms extentions.
# Will bes accessible using flask_framework.Config.Environment.SERVICES 
SERVICES:
    redis:
        HOST: localhost
        PORT: 6379
    filesystem:
        PATH: sessions
    memcached:
        HOST: localhost
        PORT: 11211
``` 

## How to use

### ```Server``` 

The `Server` module is the most important one by default you need to setup the following files:

###### ```Web.py```

With the following content.
```python
class Route(object):
    """
    Class that will configure all web based routes for the server
    """

    def __init__(self, server):
        """
        Constructor
        :param server: Flask server
        :type server: flask.Flask
        :return: Route object
        """
        import Controllers
        # example of custom route blueprints can also be registered here as server is 
        # the instance of flask provided by flask_framework.
        # Controllers are up to you to create them
        server.add_url_rule('/', "home", Controllers.Web.HomeController.default, methods=["GET"])
        return
```

It is mainly used for all interaction with the users.

###### ```WS.py```

With the following content.

```python
class Route(object):
    """
    Class that will configure all web services based routes for the server
    """
    def __init__(self, server):
        """
        Constructor
        :param server: Flask server
        :type server: flask.Flask
        :return: Route object
        """
        import Controllers
        # It has the same definition of the Web.py file. 
        # It is more convenient to separate users interactions to web services. 
        return
```

It is mainly used for all seb service that can be used with another font-end technologies of other backend application.

###### ```Middleware.py```

With the following content.

```python
class Load(object):

    def __init__(self, server):
        """

        :param server:
        :type server: flask.Flask
        """
        # It has the same definition of the Web.py file. 
        # It is more convenient to separate Middleware functionality from the application business core.
        pass
```

###### ```ErrorHandler.py```

With the following content.

```python
class Route(object):
    """
    Class that will configure all function used for handling requests error code
    """

    def __init__(self, server):
        """
        Constructor
        :param server: Flask server
        :type server: flask.Flask
        :return: Route object
        """
        # It has the same definition of the Web.py file. 
        # It is more convenient to separate errors messages from the application business core. 
        server.register_error_handler(404, Controllers.Web.HTTP40XController.page_or_error404) # yes i know, i must have done the same here .
        server.register_error_handler(500, Controllers.Web.HTTP50XController.error500) # and also here.
        return
```

Used for handling servers errors.  

###### ```Socket.py```

With the following content.

```python
class Handler(object):

    def __init__(self, socketio):
        """

        :param socketio:
        :type socketio: flask_socketio.SocketIO
        """
        import Controllers
        # This one differ from all others file because it is mainly use for setting up websocket events
        # At least there will be those two lines for connection event and disconnection events 
        # Others events are up to you
        socketio.on_event('connect', Controllers.Socket.HandlerController.connect)
        socketio.on_event('disconnect', Controllers.Socket.HandlerController.disconnect)
        pass
```

It is mainly used for realtime events with the user. Can be used  with user or server based events.
Server based event will push notifications to the user. 
User based event is a pull notification either programed within the user interface or ordered by an user's action.

:warning: **All those file are non mandatory**: It will work fine if any of them are missing

###### ```__init__.py``` 

This file is used for loading your code within the flask_framework executions so make sure to includes the files 
```Web.py```, ```WS.py```, ```Socket.py```, ```Middleware.py``` and ```ErrorHandler.py``` accordingly to your project.

Example of ```__init__.py```

```python
from . import WS, Web, Socket
```

### ```Controllers```

The ```Controllers``` module is used for your all your backend functionality and core business and will be used by the
```Server`` module.`

### ```Models```

The ```Models``` module is used for both database(s) data models and forms models to validate user's 
and webservices inputs. It is why there is the presence of Forms and Persistent submodules. It will be used by the
```Controllers``` for data processing.

```Models.Persistent``` will contains module that refer to the correct database. 
Yes you can connect multiples databases to it, even different database types.

This is permitted by the module ```flask_framework.Database```.
You only require to setup the `DATABASE` entry within the yaml configuration file.
See https://github.com/frederickney/flask-framework/blob/master/readme.md 
for further details on how to configure your database connection.

```Models.Forms``` module is used for all your input data forms, refer to the flask-wtf documantation at 
https://flask-wtf.readthedocs.io/en/1.2.x/ 

### ```template```

It is the directory where you can store and create all the UI of your application refer to the jinja documentation.
https://jinja.palletsprojects.com/en/3.1.x/

### ```static```

Well as per the name of this directory, it is where you store all static files of your applications. 
Thanks Captain Obvious 

