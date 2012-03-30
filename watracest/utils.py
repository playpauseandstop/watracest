from werkzeug import cached_property, import_string


__all__ = ('add_url', )


class LazyView(object):
    """
    Import view function only when necessary.
    """
    def __init__(self, name):
        self.__module__, self.__name__ = name.rsplit('.', 1)
        self.import_name = name

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)

    @cached_property
    def view(self):
        return import_string(self.import_name)


def add_url(app, url, view, **kwargs):
    """
    Register lazy view to the application.
    """
    view = LazyView('watracest.%s' % view)
    app.add_url_rule(url, view_func=view, **kwargs)
