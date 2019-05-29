import json
import sys

from a2ml.api.auger.base import AugerBase
from a2ml.api.auger.hub.experiment import AugerExperimentApi
from a2ml.api.auger.hub.utils.exception import AugerException


class AugerTrain(AugerBase):
    """Train you Model on Auger."""
    def __init__(self, ctx):
        super(AugerTrain, self).__init__(ctx)
        self.ctx = ctx

    def train(self):
        try:
            # verify avalability of auger credentials
            self.credentials.verify()

            self.start_project()

            data_source_name = self.ctx.config['auger'].get('data_source/name')
            if data_source_name is None:
                raise AugerException('Plese specify Data Source Name'
                    ' (auger.yaml/data_source/name option).')

            experiment_api = AugerExperimentApi(self.project_api)
            experiment_api.create(data_source_name)
            self.ctx.log(
                'Created Experiment %s ' % experiment_api.object_name)

            experiment_session_id = experiment_api.run()
            self.ctx.log(
                'Started Experiment %s training.' % experiment_api.object_name)

            auger_config = self.ctx.config['auger']
            auger_config.yaml['experiment']['name'] = \
                experiment_api.object_name
            auger_config.yaml['experiment']['experiment_session_id'] = \
                experiment_session_id
            auger_config.write()

        except Exception as exc:
            # TODO refactor into reusable exception handler
            # with comprehensible user output
            import traceback
            traceback.print_exc()
            self.ctx.log(str(exc))
