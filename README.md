# Install
```
pip install auger.ai
```

# Auger.ai
Auger Cloud python and command line interface


# CLI commands

- auth - allows to login into Auger Cloud
  - login
  - logout
  - whoami

- new - creates local folder for your Project and puts there auger.yaml;
auger.yaml provides local context for the Project and keeps settings for Experiment(s)

- project
  - list - list all Projects for your Organization.
  - select - selects existing Project and stores it's name in auger.yaml;
  all further operations with DataSet(s), Experiment(s), and Model(s) will be
  performed in context of this Project.  
  - create - creates Project on Auger Cloud; Project name will be stored in auger.yaml;
  all further operations with DataSet(s), Experiment(s), and Model(s) will be
  performed in context of this Project.  
  - delete - deletes Project on Auger Cloud and clears Project name from auger.yaml
  - start - starts Project cluster.
  - stop - stops Project cluster.

- dataset
  - list - list all DataSets(s) for the Project.
  - select - selects existing DataSet and stores it's name in auger.yaml;
  all further operations with Experiments and Models will be performed using this DataSet.
  - create - creates new DataSet on Auger Cloud from the local or remote data file;
  name of the DataSet will be stored in auger.yaml;
  all further operations with Experiments and Models will be performed using this DataSet.
  - delete - deletes DataSet on Auger Cloud and clears DataSet name from auger.yaml

- experiment
  - list - list all Experiment(s) for the DataSet
  - start - starts Experiment with selected DataSet; Experiment settings configured in auger.yaml
  - stop - stops running experiment.
  - leaderboard - shows leaderboard of the currently running or the last completed experiment.
  - history - shows history (leaderboards and settings) of the previous experiment runs.

- model
  - list - lists all deployed models on Auger Cloud; auger.ai don't keep track of locally deployed models.
  - deploy - deploys selected model locally or on Auger Cloud.
  - predict - predicts using deployed model.


# Auger.ai API
## Base Classes
### auger.api.Context
Context provides environment to run Auger Experiments and Models:
- loads Auger Credentials and initializes Auger REST API to communicate
with remote Auger Cloud;
- loads Auger settings from auger.yaml and provides access to these settings
to Auger classes and business objects;
- provides logging interface to all Auger classes and business objects.

Credentials could be acquired using Auger CLI auth command or loaded from Auger website.
Credentials lookup and loading order:
- form environment variable AUGER_CREDENTIALS set with content of
  the credentials json;
- from auger.json file, path to folder with credentials set with
  environment variable AUGER_CREDENTIALS_PATH;
- from auger.json file, path to folder with credentials set with
  path_to_credentials key in auger.yaml
- if none above, form $HOME/.augerai/auger.json

### auger.api.Project
Project provides interface to Auger Project.

- **Project(context, project_name)** - constructs Project instance.
  - context - instance of auger.api.Context.
  - project_name - name of the existing or new Project, optional.

- **list()** - lists all Projects in your Organization. Returns iterator where
  each item is dictionary with Project properties. Throws exception if can't
    validate credentials or network connection error.

  Example:
  ```
  ctx = Context()
  for project in iter(Project(ctx).list()):
    ctx.log(project.get('name'))
  ```

- **create()** - creates Project on Auger Cloud. Throws exception if can't
  validate credentials, Project with such name already exists, or network
  connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, new_project_name).create()
  ```

- **delete()** - deletes Project on Auger Cloud. Throws exception if can't
  validate credentials, Project with such name doesn't exist, or network
  connection error.

  Example:
  ```
  ctx = Context()
  Project(ctx, existing_project_name).delete()
  ```

- **start()** - starts Project cluster. DataSet processing, Experiment runs
  and Model deploy and predict need cluster to perform operations and will
  start cluster automatically. It is possible, but not necessary, to start
  cluster beforehand. Throws exception if can't validate credentials or
  network connection error.

  Project cluster configuration defined in auger.yaml:
  ```
  cluster:
    # Cluster node type: standard|high_memory
    type: high_memory
    # Minimal number of cluster nodes
    min_nodes: 2
    # Maximum number of cluster nodes
    max_nodes: 4
    # Cluster software stack version - optional
    stack_version: experimental
  ```

  Example:
  ```
  ctx = Context()
  Project(ctx, project_name).start()
  ```

- **stop()** - stops Project cluster. DataSet processing, Experiment runs
  and Model deploy and predict need cluster to perform operations and will
  start cluster automatically. Cluster will stop automatically after some
  inactivity period. To stop it explicitly, use Project stop() method.
  Throws exception if can't validate credentials, such project doesn't exist,
  or network connection error.

  Example:
  ```
  ctx = Context()
  Project(ctx, project_name).stop()
  ```

- **properties()** - returns dictionary with Project properties. Throws exception
  if can't validate credentials, such Project doesn't exist, or network connection
  error.

  Example:
  ```
  ctx = Context()
  properties = Project(ctx, project_name).properties()
  ```

### auger.api.DataSet
DataSet for training on Auger Cloud.

- **DataSet(context, project, dataset_name)** - constructs DataSet instance.
  - context - instance of auger.api.Context.
  - project - instance of auger.api.Project pointing to existing remote project.
  - dataset_name - name of the existing or new DataSet, optional.

- **list()** - lists all DataSets(s) for the Project. Returns iterator where
  each item is dictionary with DataSet properties. Throws exception if can't
  validate credentials, parent project doesn't exist, or network connection error.


  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  for dataset in iter(DataSet(ctx, project).list()):
    ctx.log(dataset.get('name'))
  ```

- **create(source)** - creates new DataSet on Auger Cloud from the local or
  remote data file. If `dataset_name` is not set, name will be selected
  automatically. Throws exception if can't validate credentials, parent project
  doesn't exist, DataSet with specified name already exists, or network
  connection error.

  - source - path to local or link to remote .csv or .arff file

  If Project cluster is not running, it will be started automatically to
  parse and preprocess DataSet.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project).create('../iris.csv')
  ctx.log('Created dataset %s' % dataset.name)
  ```

- **delete()** - deletes DataSet on Auger Cloud. Throws exception if can't
  validate credentials, parent project doesn't exist, DataSet with specified
  name doesn't exist, or network connection error.       

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  DataSet(ctx, project, dataset_name).delete()
  ctx.log('Deleted dataset %s' % dataset_name)
  ```

- **properties()** - returns dictionary with DataSet properties. Throws exception
  if can't validate credentials, such DataSet doesn't exist, or network connection
  error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  properties = DataSet(ctx, project, dataset_name).properties()
  ```

### auger.api.Experiment
Experiment searches for the best Model(s) for a given DataSet.

- **Experiment(context, dataset, experiment_name)** - constructs Experiment instance.
  - context - instance of auger.api.Context.
  - dataset - instance of auger.api.DataSet pointing to existing remote DataSet
    which will be used to search for the best Model.
  - experiment_name - name of the existing or new Experiment, optional.

- **list()** - list all Experiment(s) for the DataSet. Returns iterator where
  each item is dictionary with Experiment properties. Throws exception if can't
  validate credentials, parent DataSet doesn't exist, or network connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project, dataset_name)
  for exp in iter(Experiment(ctx, dataset).list()):
    ctx.log(exp.get('name'))
  ```

- **start()** - starts Experiment with selected DataSet; Experiment settings
  configured in auger.yaml. If `experiment_name` is not set in constructor,
  unique name for the Experiment will be created automatically. Throws exception
  if can't validate credentials, parent DataSet doesn't exist, experiment with
  such name already exists, or network connection error.

  If Project cluster is not running, it will be started automatically to process
  search for the best Model.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project, dataset_name)
  eperiment_name, session_id = Experiment(ctx, dataset).start()
  ```

  Example of the Experiment settings in auget.yaml:
  ```
  # List of columns to be excluded from the training data
  exclude:

  experiment:
    # Time series feature. If Data Source contains more then one DATETIME feature
    # you will have to explicitly specify feature to use as time series
    time_series:
    # List of columns which should be used as label encoded features
    label_encoded: []
    # Number of folds used for k-folds validation of individual trial
    cross_validation_folds: 5
    # Maximum time to run experiment in minutes
    max_total_time: 60
    # Maximum time to run individual trial in minutes
    max_eval_time: 1
    # Maximum trials to run to complete experiment
    max_n_trials: 10
    # Try to improve model performance by creating ensembles from the trial models
    use_ensemble: true
    ### Metric used to build Model
    # Score used to optimize ML model.
    # Supported scores for classification: accuracy, f1_macro, f1_micro, f1_weighted, neg_log_loss, precision_macro, precision_micro, precision_weighted, recall_macro, recall_micro, recall_weighted
    # Supported scores for binary classification: accuracy, average_precision, f1, f1_macro, f1_micro, f1_weighted, neg_log_loss, precision, precision_macro, precision_micro, precision_weighted, recall, recall_macro, recall_micro, recall_weighted, roc_auc, cohen_kappa_score, matthews_corrcoef
    # Supported scores for regression and time series: explained_variance, neg_median_absolute_error, neg_mean_absolute_error, neg_mean_squared_error, neg_mean_squared_log_error, r2, neg_rmsle, neg_mase, mda, neg_rmse
    metric: f1_macro
  ```

- **stop()** - stops running Experiment. Returns True is Experiment was running
  and stopped now, False is Experiment wasn't running and stop command was ignored.
  Throws exception if can't validate credentials, parent DataSet doesn't exist,
  Experiment with such name doesn't exist, or network connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project, dataset_name)
  if Experiment(self.ctx, dataset, experiment_name).stop():
      ctx.log('Search is stopped...')
  else:
      ctx.log('Search is not running. Stop is ignored.')
  ```

- **leaderboard(run_id)** - leaderboard of the currently running or
  previously completed experiment(s). If `run_id` is not specified, method
  returns currently running or last completed experiment leaderboard; otherwise
  returns leaderboard for the run with specified id. Returns None if leaderboard
  wasn't found.

  In addition, returns status of the Experiment run:  
  - preprocess - Search is preprocessing data for traing;
  - started - Search is in progress;
  - completed - Search is completed;
  - interrupted - Search was interrupted.

  Throws exception if can't validate credentials, parent DataSet doesn't exist,
  Experiment with such name doesn't exist, or network connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project, dataset_name)
  # latest experiment leaderboard and latest experiment status
  leaderboard, status = Experiment(ctx, dataset, experiment_name).leaderboard()
  ```

- **history()** - history (leaderboards and settings) of the previous
  experiment runs. Returns iterator where each item is dictionary with properties
  of the previous Experiment runs.
  Throws exception if can't validate credentials, parent DataSet doesn't exist,
  Experiment with such name doesn't exist, or network connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project, dataset_name)
  for run in iter(Experiment(self.ctx, dataset, experiment_name).history()):
      ctx.log("run id: {}, start tiem: {}, status: {}".format(
        run.get('id'),
        run.get('model_settings').get('start_time'),
        run.get('status')))
  ```

- **properties()** - returns dictionary with Experiment properties. Throws exception
  if can't validate credentials, such Experiment doesn't exist, or network connection
  error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project, dataset_name)
  properties = Experiment(self.ctx, dataset, experiment_name).properties()
  ```

- **delete()** - deletes Experiment. Throws exception if can't validate
  credentials, such Experiment doesn't exist, or network connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  dataset = DataSet(ctx, project, dataset_name)
  Experiment(self.ctx, dataset, experiment_name).delete()
  ```

### auger.api.Model
Deploys or predicts using one of the Models from the Project Experiment(s)
leaderboards.

- **Model(context, project)** - constructs Model instance.
  - context - instance of auger.api.Context.
  - project - instance of auger.api.Project pointing to existing remote Project.

- **list()** - lists all deployed models for a Project; auger.ai don't keep
  track of locally deployed models. Returns iterator where each item is
  dictionary with deployed Model properties. Throws exception if can't
  validate credentials or network connection error.

- **deploy(model_id, locally)** - deploys selected model locally or on
  Auger Cloud. Returns deployed model id.
  - model_id - id of the model from the any Experiment leaderboard
  - locally - deploys model locally if True, on Auger Cloud if False; optional,
    default is False.

  Throws exception if can't validate credentials, project of model doesn't exist,
  or network connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  # deploys model locally
  Model(self.ctx, project).deploy(model_id, True)
  ```

- **predict(filename, model_id, threshold, locally)** - predicts using deployed
  model. Predictions stored next to the file with data to be
  predicted on; file name will be appended with suffix `_predicted`.
  - filename - file with data to be predicted
  - model_id - id of the deployed model
  - threshold - prediction threshold
  - locally - if True predict using locally deployed model, predict using model
    deployed on Auger Cloud

  Throws exception if can't validate credentials, project of model doesn't exist,
  or network connection error.

  Example:
  ```
  ctx = Context()
  project = Project(ctx, project_name)
  # predict on the locally deployed model
  Model(self.ctx, project).predict('../irises.csv', model_id, True)
  # result will be stored in ../irises_predicted.csv
  ```

## Development Setup

We strongly recommend to install Python virtual environment:

```
$ pip install virtualenv virtualenvwrapper
```

Clone Auger Cloud repo:

```
$ git clone https://github.com/deeplearninc/auger-ai
```

Setup dependencies and Auger command line:

```
$ pip install -e .[all]
```

Running tests and getting test coverage:

```
$ pytest --cov='auger' --cov-report html tests/
```

#
