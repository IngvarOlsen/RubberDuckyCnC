from website import create_app, create_database
# from sanic import Sanic
# from sanic.response import html
from flask import send_from_directory
import socketio
import os

app = create_app()

app.config['SECRET_KEY'] = "UbhodfUMwmeZTyjZ7r0B0g=="

#create_database(app) # Is created inside the __init__.py instead with sqlalchemy


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    #app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=('cert.pem', 'certpriv_key.pem')) # For SSL
