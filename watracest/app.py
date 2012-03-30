#!/usr/bin/env python

from flask import Flask
from flask.ext.redis import Redis

from watracest import settings
from watracest.utils import add_url


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(settings)

# Initialize Redis connection
redis = Redis(app)

# Route all views
add_url(app, '/', 'views.home')
add_url(app, '/find-out', 'views.find_out')
add_url(app, '/reset', 'views.reset')
add_url(app, '/secret', 'views.parse_it')
add_url(app, '/show-me-the-truth', 'views.show_me')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4352)
