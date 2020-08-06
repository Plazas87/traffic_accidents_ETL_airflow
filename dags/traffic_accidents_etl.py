from datetime import timedelta
from datetime import datetime
import os
import sys
sys.path.append(os.getcwd())

# The DAG object
from airflow import DAG

# Operators
from airflow.operators.python_operator import PythonOperator, PythonVirtualenvOperator

# Your modules
from traffic_accidents import Controller
from mc_map_generator import Mapper

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Airflow',
    'depends_on_past': True,
    'start_date': datetime(2020, 8, 6, 11),
    # 'end_date': datetime(2020, 7, 5),
    'email': ['example@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'Traffic_accidents_madrid',
    default_args=default_args,
    description='Read and transform a csv file',
    schedule_interval='30 * * * *',
)


def execute_python(*args, **kwargs):
    processor = Controller()
    processor.run()


def generates_heatmap(*args, **kwargs):
    Mapper.heatmap()


def generates_stdmap(*args, **kwargs):
    Mapper.standard_map()


t1 = PythonOperator(
    task_id='Read_process_data',
    provide_context=True,
    python_callable=execute_python,
    dag=dag
)

t2 = PythonOperator(
    task_id='generates_heatmap',
    provide_context=True,
    python_callable=generates_heatmap,
    dag=dag
)


t3 = PythonOperator(
    task_id='generate_stdmap',
    provide_context=True,
    python_callable=generates_stdmap,
    dag=dag
)

t1 >> [t2, t3]
