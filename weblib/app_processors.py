#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from weblib.logging import create_logger
from jinja2 import TemplateNotFound
from jinja2 import TemplatesNotFound


def load_logger():
    '''Add a logger to the shared context.'''
    web.ctx.logger = create_logger()


def load_path_url():
    '''Add 'path_url' property to the shared context containing the
    concatenation of ``web.ctx.home`` and ``web.ctx.path``.'''
    web.ctx.path_url = web.ctx.home + web.ctx.path


def load_render(views, **globals):
    '''Add the renderer to the shared context.'''

    class render_jinja:
        """Rendering interface to Jinja2 Templates

        Example:

            render= render_jinja('templates')
            render.hello(name='jinja2')
            """
        def __init__(self, *a, **kwargs):
            extensions = kwargs.pop('extensions', [])
            globals = kwargs.pop('globals', {})

            from jinja2 import Environment,FileSystemLoader
            self._lookup = Environment(loader=FileSystemLoader(*a, **kwargs), extensions=extensions)
            self._lookup.globals.update(globals)

        def __getattr__(self, name):
            paths = [name + '.' + ext for ext in ['html', 'xml']]
            t = self._lookup.select_template(paths)
            return t.render

    render = render_jinja(views, encoding='utf-8',
                          extensions=['jinja2.ext.do'],
                          globals=globals)

    def inner():
        web.ctx.render = render
    return inner


def load_render(views, **globals):
    '''Add the renderer to the shared context.'''
    import pdb; pdb.set_trace()  # XXX BREAKPOINT

    class render_jinja:
        """Rendering interface to Jinja2 Templates

        Example:

            render= render_jinja('templates')
            render.hello(name='jinja2')
            """
            def __init__(self, *a, **kwargs):
                extensions = kwargs.pop('extensions', [])
                globals = kwargs.pop('globals', {})

            from jinja2 import Environment,FileSystemLoader
            self._lookup = Environment(loader=FileSystemLoader(*a, **kwargs), extensions=extensions)
            self._lookup.globals.update(globals)

        def __getattr__(self, name):
            # Assuming all templates end with .html
            import pdb; pdb.set_trace()  # XXX BREAKPOINT

            try:
                path = name + '.html'
                t = self._lookup.get_template(path)
            except TemplateNotFound:
                path = name + '.xml'
                t = self._lookup.get_template(path)
            return t.render

    render = render_jinja(views, encoding='utf-8',
                          extensions=['jinja2.ext.do'])
    render._lookup.globals.update(globals)

    def inner():
        web.ctx.render = render
    return inner


def load_render_with_assets(views, env, **globals):
    '''Add the renderer to the shared context.'''
    from webassets.ext.jinja2 import AssetsExtension
    render = render_jinja(views, encoding='utf-8',
                          extensions=['jinja2.ext.do', AssetsExtension])
    render._lookup.assets_environment = env
    render._lookup.globals.update(globals)
    def inner():
        web.ctx.render = render;
    return inner


def load_session(session):
    '''Load the session into the shared context.'''
    def inner():
        web.ctx.session = session
    return inner


def load_gettext(gettext):
    '''Load the gettext object into the shared context.'''
    def inner():
        web.ctx.gettext = gettext
    return inner


def load_redis(redis):
    '''Load a Redis client object into the shared context.'''
    def inner():
        web.ctx.redis = redis
    return inner


def load_and_manage_orm(ormfactory):
    '''Load ORM database connection and manage exceptions properly.'''
    def inner(handler):
        web.ctx.orm = ormfactory()

        try:
            return handler()
        finally:
            ormfactory.remove()
    return inner


def load_dict(**kw):
    def inner():
        web.ctx.update(**kw)
    return inner
