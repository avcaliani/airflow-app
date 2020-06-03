from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


dag = DAG(
	dag_id = 'my_first_dag',
	start_date = datetime.now() - timedelta(hours=0, minutes=20),
	schedule_interval = '*/15 * * * *'
)

def print_hello():
	return "hello from Python Task!"


t1 = BashOperator(
    task_id='task_1',
    bash_command='echo "I am the first one :)"',
    dag=dag
)

t2 = BashOperator(
    task_id='task_2',
    bash_command='echo "Hello from Bash Task!"',
    dag=dag
)

t3 = PythonOperator(
	task_id = 'task_3',
	python_callable = print_hello,
	dag = dag
)

t4 = BashOperator(
    task_id='task_4',
    bash_command='echo "I am the last one :)"',
    dag=dag
)

t2.set_upstream(t1)
t3.set_upstream(t1)
t4.set_upstream(t2)
t4.set_upstream(t3)


#   / -- T2 -- \
# T1            | --- T4
#   \ -- T3 -- /