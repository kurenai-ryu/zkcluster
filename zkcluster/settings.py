from django.conf import settings

def get_config():
    '''
    Returns ZKCluster's configuration in dictionary format. e.g:
    ZK_CLUSTER = {
        'TERMINAL_TIMEOUT': 5
    }
    '''
    return getattr(settings, 'ZK_CLUSTER', {})

def get_terminal_timeout():
    return get_config().get('TERMINAL_TIMEOUT', 5)

def get_ommit_ping():
    return get_config().get('OMMIT_PING', False)

def get_verbose():
    return get_config().get('VERBOSE', False)
