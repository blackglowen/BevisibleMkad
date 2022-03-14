#!/usr/bin/env python
#-*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from . import api

# This is the application factory function responsible for creating and initializing the instances.
# If the FLASK_APP env variable is not set when trying to run "flask run" command, it will try to 
# import “app” or “wsgi” (as module or package) and try to detect an app instance or this factory.
# Within the given import, the command looks for a Flask instance named app or application, then
# any application instance. If no instance is found, the command looks for a factory function 
# named create_app or make_app that returns an instance.
# This function is also called by the application entry point main function located in app.py module.
def make_app(test_config=None) -> Flask:
    """Retruns the flask object implementing a WSGI application and acting as the central object. 
    @param Any test_config: optional test configuration used instead of the app 
    instance configuration.
    @return Flask: an instance representing  a WSGI application
    """
    app = Flask(__name__, instance_relative_config=True)  # create and configure the app
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Allow users to access the app hompage via more than one routes        
    @app.route('/mkad')
    @app.route('/mkad/')
    @app.route('/')
    def home():
        return render_template('index.html')
    
    app.register_blueprint(api.bp)
    
    return app