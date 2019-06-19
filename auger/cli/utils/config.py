class AugerConfig(object):
    """Modify configuration options in auger.yaml."""

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    def _with_auger_yaml(decorated):
        def wrapper(self, *args, **kwargs) :
            auger_config = self.ctx.config['auger']
            decorated(self, auger_config.yaml, *args, **kwargs)
            auger_config.write()
            return self
        return wrapper

    @_with_auger_yaml
    def config(self, yaml, *args, **kwargs):
        yaml['source'] = \
            kwargs.get('source', '')
        yaml['dataset'] = \
            kwargs.get('data_set_name', '')
        yaml['experiment']['name'] = \
            kwargs.get('experiment_name', '')
        yaml['experiment']['experiment_session_id'] = \
            kwargs.get('experiment_session_id', '')

        yaml['project'] = kwargs.get('project_name', '')

        model_type = kwargs.get('model_type', None)
        if model_type:
            yaml['experiment']['metric'] = \
                'f1_macro' if model_type == 'classification' else 'r2'
        yaml['model_type'] = model_type or ''
        yaml['target'] = kwargs.get('target', '')

    @_with_auger_yaml
    def set_project(self, yaml, project_name):
        yaml['project'] = project_name

    @_with_auger_yaml
    def set_data_set(self, yaml, data_set_name, data_set_source):
        yaml['dataset'] = data_set_name
        yaml['source'] = data_set_source

    @_with_auger_yaml
    def set_experiment(self, yaml, experiment_name, experiment_session_id):
        yaml['experiment']['name'] = experiment_name
        yaml['experiment']['experiment_session_id'] = experiment_session_id
