from pyramid.config import Configurator



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # add_static_view(name='static', path='learning_journal_basic:static')
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
