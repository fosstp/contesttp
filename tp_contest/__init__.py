from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')

    # session settings
    #
    # using builtin session mechanism
    from pyramid.session import SignedCookieSessionFactory
    config.set_session_factory(SignedCookieSessionFactory(settings['secret_key']))

    config.include('pyramid_tm')
    config.include('pyramid_sqlalchemy')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('list_competition', '/competition')
    config.add_route('list_competition_news', '/competition/{competition_id}/news')
    config.add_route('show_competition_news', '/competition/{competition_id}/news/{news_id}')
    config.scan()
    return config.make_wsgi_app()
