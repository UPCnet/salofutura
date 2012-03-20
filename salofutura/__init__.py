from pyramid.config import Configurator
from salofutura.models import appmaker

from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid_who.whov2 import WhoV2AuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from models import Root
from pyramid_mailer.mailer import Mailer

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    # security
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    whoconfig_file = settings['whoconfig_file']
    identifier_id = 'auth_tkt'
    authn_policy = WhoV2AuthenticationPolicy(whoconfig_file, identifier_id)
    authz_policy = ACLAuthorizationPolicy()    
    
    config = Configurator(root_factory=Root,
                          settings=settings,
                          session_factory = my_session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    
    config.registry['mailer'] = Mailer.from_settings(settings)
    
    config.add_static_view('static', 'salofutura:static')
    config.add_static_view('css', 'salofutura:css')
    config.add_static_view('images', 'salofutura:images')
    config.add_static_view('js', 'salofutura:js')
    
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_view('salofutura.views.login.login', route_name='login',
                     renderer='salofutura:templates/login.pt')
    config.add_view('salofutura.views.login.logout', route_name='logout')
    
    config.add_view('salofutura.views.login.login',
                    context='pyramid.httpexceptions.HTTPForbidden',
                    renderer='salofutura:templates/login.pt')

    config.scan('salofutura')


    return config.make_wsgi_app()
