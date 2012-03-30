#!/usr/bin/env python

import unittest

from watracest.app import app, redis
from watracest.tasks import build_url, parse_alltheragefaces


class TestTasks(unittest.TestCase):

    def setUp(self):
        self.old_DATABASE_KEY = app.config['DATABASE_KEY']
        self.old_DATABASE_EXISTS_KEY = app.config['DATABASE_EXISTS_KEY']

        app.config['DATABASE_KEY'] = 'test_' + app.config['DATABASE_KEY']
        app.config['DATABASE_EXISTS_KEY'] = \
            'test_' + app.config['DATABASE_EXISTS_KEY']

    def tearDown(self):
        redis.delete(app.config['DATABASE_KEY'])
        redis.delete(app.config['DATABASE_EXISTS_KEY'])

        app.config['DATABASE_KEY'] = self.old_DATABASE_KEY
        app.config['DATABASE_EXISTS_KEY'] = self.old_DATABASE_EXISTS_KEY

    def test_build_url(self):
        url = 'http://www.google.com/'
        new = '/search?q=python'
        result = url.strip('/') + new

        self.assertEqual(build_url(url, new), result)

        url = 'http://www.google.com/reader/view/'
        self.assertEqual(build_url(url, new), result)

    def test_parse_alltheragefaces(self):
        self.assertFalse(redis.exists(app.config['DATABASE_KEY']))
        self.assertFalse(redis.exists(app.config['DATABASE_EXISTS_KEY']))

        parse_alltheragefaces()

        self.assertTrue(redis.exists(app.config['DATABASE_KEY']))
        self.assertFalse(redis.exists(app.config['DATABASE_EXISTS_KEY']))


if __name__ == '__main__':
    unittest.main()
