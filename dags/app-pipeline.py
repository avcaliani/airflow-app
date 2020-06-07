from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator

args = {
    'owner'            : 'avcaliani',
    'description'      : 'App Pipeline',
    'depend_on_past'   : False,
    'start_date'       : datetime.now() - timedelta(hours=0, minutes=20),
    'email_on_failure' : False,
    'email_on_retry'   : False,
    'retries'          : 1,
    'retry_delay'      : timedelta(minutes=1)
}

with DAG('app-pipeline', default_args=args, schedule_interval='*/15 * * * *', catchup=False) as dag:

    # TODO: Create initialize script
    initialize = BashOperator(task_id='initialize', bash_command='mkdir -p /datalake/logs/app-broken')

    # FIXME: Fix Volume (Host)
    app_broken = DockerOperator(
        task_id='app-broken',
        image='app-broken:latest',
        api_version='auto',
        auto_remove=True,
        network_mode='bridge',
        environment={'LOG_PATH': '/app-logs'},
        volumes=['/Users/anthony.caliani/Documents/projects/airflow/datalake/logs/app-broken/:/app-logs/'],
        docker_url='unix://var/run/docker.sock'
    )

    # TODO: Create teardown script
    teardown = BashOperator(task_id='teardown', bash_command='date')

    initialize >> app_broken >> teardown
