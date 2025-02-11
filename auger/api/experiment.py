from datetime import datetime

from .cloud.experiment import AugerExperimentApi
from .cloud.utils.exception import AugerException
from .cloud.experiment import AugerExperimentSessionApi


class Experiment(AugerExperimentApi):
    """Auger Cloud Experiments(s) management"""

    def __init__(self, ctx, dataset, experiment_name=None):
        super(Experiment, self).__init__(
            ctx, dataset.project, experiment_name)
        self.dataset = dataset

    def list(self):
        data_set_id = self.dataset.oid
        filter_by_dataset = \
            lambda exp: exp.get('project_file_id') == data_set_id
        return (e for e in super().list() if filter_by_dataset(e))

    def start(self):
        if self.dataset is None:
            raise AugerException(
                'DataSet is required to start Experiment...')

        if not self.dataset.is_exists:
            raise AugerException('Can\'t find DataSet on Auger Cloud...')

        if self.object_name and self.is_exists:
            data_set_id = self.dataset.oid
            experiment_data_set = self.properties().get('project_file_id')
            if data_set_id != experiment_data_set:
                raise AugerException(
                    'Can\'t start Experiment '
                    'configured with different DataSet...')

        if not self.dataset.project.is_running():
            self.ctx.log('Starting Project to process request...')
            self.dataset.project.start()

        if (self.object_name is None) or (not self.is_exists):
            self.create(self.dataset.name)
            self.ctx.log('Created Experiment %s ' % self.name)

        experiment_session_id = self.run()
        self.ctx.log('Started Experiment %s search...' % self.name)

        return self.name, experiment_session_id

    def stop(self):
        run_id = self._get_latest_run()
        session_api = AugerExperimentSessionApi(
            self.ctx, None, None, run_id)
        return session_api.interrupt()

    def leaderboard(self, run_id=None):
        if run_id is None:
            run_id = self._get_latest_run()

        if run_id is None:
            return None, None
        else:
            session_api = AugerExperimentSessionApi(
                self.ctx, None, None, run_id)
            status = session_api.properties().get('status')
            return session_api.get_leaderboard(), status

    def history(self):
        return AugerExperimentSessionApi(self.ctx, self).list()

    def _get_latest_run(self):
        latest = [None, None]
        for run in iter(self.history()):
            start_time = run.get('model_settings').get('start_time')
            if start_time:
                start_time = datetime.strptime(
                    start_time, '%Y-%m-%d %H:%M:%S.%f')
                if (latest[0] is None) or (latest[1] < start_time):
                    latest = [run.get('id'), start_time]
        return latest[0]
