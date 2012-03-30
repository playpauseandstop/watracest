========================
Which Rage Face Are You?
========================

Test project for Kyiv.py#6.

Project uses real AI to calculate which rage face are you!

Requirements
============

* `Python <http://www.python.org/>`_ 2.6 or 2.7
* `virtualenv <http://www.virtualenv.org/>`_ 0.7 or higher
* `pip <http://www.pip-installer.org/>`_ 1.0 or higher
* `redis <http://redis.io/>`_ 2.4 or higher
* Internet connection :)

Installation
============

::

    $ virtualenv env --distribute
    $ . env/bin/activate
    $ pip install -r requirements.txt

**ps.** Too lazy to use bootstrap.py :)

Running
=======

Make sure, that redis is running, if you need custom redis settings place it
to ``watracest/settings_local.py``.

Then run Flask server by::

    (env)$ ./watracest/app.py

Point browser to ``http://127.0.0.1:4352/`` and have fun.

License
=======

``watracest`` is licensed under the `BSD License
<https://github.com/playpauseandstop/watracest/blob/master/LICENSE>`_.
