from .cloud.project import AugerProjectApi
from .cloud.org import AugerOrganizationApi
from .cloud.utils.exception import AugerException


class Project(AugerProjectApi):
    """Auger Cloud Projects(s) management"""

    def __init__(self, ctx, project_name=None):
        org = AugerOrganizationApi(ctx, ctx.credentials.organisation)
        super(Project, self).__init__(ctx, org, project_name)
