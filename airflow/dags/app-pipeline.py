from os import environ
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator  # FIXME: Remove this import


SCRIPTS_PATH  = environ.get('SCRIPTS_PATH', '/airflow/scripts')
DATALAKE_HOST = environ.get('DATALAKE_HOST', './')
ARGS = {
    'owner'            : 'avcaliani',
    'description'      : 'App Pipeline',
    'depend_on_past'   : False,
    'start_date'       : datetime.now() - timedelta(hours=0, minutes=20),
    'email_on_failure' : False,
    'email_on_retry'   : False,
    'retries'          : 1,
    'retry_delay'      : timedelta(minutes=1)
}


with DAG('app-pipeline', default_args=ARGS, schedule_interval='*/15 * * * *', catchup=False) as dag:

    app_initialize = BashOperator(
        task_id='app-initialize',
        bash_command=f'bash {SCRIPTS_PATH}/app-initialize.sh\n'
    )

    app_extractor = DockerOperator(
        task_id='app-extractor',
        image='app-extractor:latest',
        api_version='auto',
        auto_remove=True,
        network_mode='bridge',
        environment={
            'LAKE_PATH': '/datalake/transient/jokes',
            'LOG_PATH': '/datalake/logs/app-extractor'
        },
        volumes=[f'{DATALAKE_HOST}:/datalake/'],
        docker_url='unix://var/run/docker.sock'
    )

    app_broken = DockerOperator(
        task_id='app-broken',
        image='app-broken:latest',
        api_version='auto',
        auto_remove=True,
        network_mode='bridge',
        environment={'LOG_PATH': '/datalake/logs/app-broken'},
        volumes=[f'{DATALAKE_HOST}:/datalake/'],
        docker_url='unix://var/run/docker.sock'
    )

    # FIXME: Add Docker Operator
    app_processor = DummyOperator(task_id='app-processor')

    app_teardown = BashOperator(
        task_id='app-teardown',
        bash_command=f'bash {SCRIPTS_PATH}/app-teardown.sh\n',
        trigger_rule='none_skipped'
    )

    app_initialize >> app_extractor >> app_broken >> app_processor >> app_teardown
