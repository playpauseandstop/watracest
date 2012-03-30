import logging

import requests

from BeautifulSoup import BeautifulSoup
from furl import furl
from requests.exceptions import RequestException

from watracest.app import app, redis


logger = logging.getLogger(__name__)
logger.write = logger.info

session = requests.session(config={'verbose': logger})


def build_url(base_url, new_url):
    """
    Concatenate new relative URL to the base URL and returns result as an
    unicode data.
    """
    url = furl(base_url)

    # Strip a path and query from the URL
    if url.args:
        url = url.remove(args=True)

    if url.path:
        url = url.remove(path=True)

    new = furl(new_url)
    return unicode(url.add(path=unicode(new.path), args=new.args))


def get(url, **kwargs):
    """
    Shortcut for sending GET request to the page and save verbose information
    about errors in the log.
    """
    defaults = {'headers': {'user-agent': app.config['USER_AGENT']}}

    if 'headers' in kwargs:
        headers = kwargs.pop('headers')
        defaults['headers'].update(headers)

    defaults.update(kwargs)

    try:
        response = session.get(url, **kwargs)
    except RequestException:
        logger.exception('Cannot fetch requested URL, exit...')
        return None

    if response.status_code == 200:
        return response

    logger.error('Got %d status code, exit...', response.status_code)
    return None


def parse_alltheragefaces(url=None):
    """
    Parse all png rage faces from alltheragefaces.com and store its to the
    redis list.
    """
    url = url or app.config['SITE_URL']
    response = get(url)

    if response is None:
        return

    images = []

    soup = BeautifulSoup(response.content)

    faces = soup.findAll('div', attrs={'class': 'face'})
    finder = lambda tag: tag.name == 'a' and \
                         dict(tag.attrs).get('href', '').endswith('.png')

    for face in faces:
        try:
            download = face.findAll('div', attrs={'class': 'download'})[0]
        except IndexError:
            continue

        try:
            image = download.findAll(finder)[0]
        except IndexError:
            continue

        href = dict(image.attrs)['href']
        images.append(build_url(url, href))

    if not images:
        return

    key = app.config['DATABASE_KEY']
    exists_key = app.config['DATABASE_EXISTS_KEY']

    redis.setnx(exists_key, 1)

    for image in images:
        redis.lpush(key, image)

    try:
        pagination = soup.findAll('div', attrs={'class': 'pagination'})[0]
    except IndexError:
        return

    span = pagination.find('span')

    try:
        attrs = span.next.next.attrs
    except AttributeError:
        redis.delete(exists_key)
        redis.expire(key, app.config['EXPIRE_TIME'])
        return

    return parse_alltheragefaces(build_url(url, dict(attrs)['href']))
