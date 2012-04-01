import logging
import os
import time

from random import choice, shuffle

from flask import json, redirect, render_template, session, url_for

from watracest.app import app, redis
from watracest.tasks import parse_alltheragefaces


logger = logging.getLogger(__name__)


def home():
    """
    Home page.

    If user already calculated rage face it will show rage face and
    recalculate banner.

    If user not calculated rage face - it will show big calculate banner.
    """
    return render_template('home.html',
                           face=session.get(app.config['SESSION_KEY'], None))


def find_out():
    """
    Calculation on which rage face are current user.

    .. warning:: HERE IS THE PLACE WHERE AI USED!
    """
    key = app.config['DATABASE_KEY']

    if not redis.exists(key):
        return render_template('find_out.html', run=True)

    if redis.exists(app.config['DATABASE_EXISTS_KEY']):
        return render_template('find_out.html', run=True)

    length = redis.llen(key)
    images = redis.lrange(key, 0, length)

    shuffle(images)
    image = choice(images)

    session[app.config['SESSION_KEY']] = image
    return render_template('find_out.html')


def parse_it():
    """
    Parse alltheragefaces.com site and store results to redis.
    """
    status = 'parsing'

    if redis.exists(app.config['DATABASE_KEY']):
        status = 'ok'
    elif not redis.exists(app.config['DATABASE_EXISTS_KEY']):
        try:
            parse_alltheragefaces()
        except:
            logger.exception('Something wrong happened...')
            status = 'error'
        else:
            status = 'ok'

    return json.dumps({'status': status})


def reset():
    """
    Cleanup current session if any.
    """
    if app.config['SESSION_KEY'] in session:
        session.pop(app.config['SESSION_KEY'])
    return redirect(url_for('home'))


def show_me():
    """
    Show how calculation done for current user.
    """
    # Scumbag thumbnail code
    try:
        from PIL import Image
    except ImportError:
        pass
    else:
        filename = os.path.join(app.static_folder, 'img', 'badumtss.png')
        image = Image.open(filename)

    return render_template('show_me.html')
