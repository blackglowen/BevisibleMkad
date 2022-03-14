#!/usr/bin/env python
#-*- coding: utf-8 -*-

from mkad.wsgi import make_app

# This is an entry point for the application. 
# This function could be called to get the app running.
# The debug parameter is set to True by default, but
# should be False in production environment. 
def main():
    app = make_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()