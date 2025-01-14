from .rest_api import RestApi
from .org import AugerOrganizationApi
from .utils.exception import AugerException


class AugerAuthApi(object):
    """Auger Authentication API."""
    def __init__(self, ctx):
        super(AugerAuthApi, self).__init__()
        self.ctx = ctx

    def login(self, username, password, organisation, url):
        rest_api = RestApi(url, None)
        try:
            res = rest_api.call_ex(
                'create_token', {'email': username, 'password': password})
        except Exception as e:
            if 'Email or password incorrect' in str(e):
                raise AugerException('Email or password incorrect...')
            else:
                raise e
        self.ctx.rest_api = RestApi(url, res['data']['token'])
        org_api = AugerOrganizationApi(self.ctx, organisation)
        if org_api.properties() == None:
            raise AugerException(
                'Auger Organization %s doesn\'t exist' % organisation)
        return res['data']['token']
