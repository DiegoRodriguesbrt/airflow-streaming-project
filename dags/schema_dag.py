import random
import pandas as pd
import logging
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
from pinot_schema_operator import PinotSchemaSubmitOperator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

start_date = datetime(2025,3,27)
default_args = {
    'owner': 'project-airflow',
    'depends_on_past': False,
    'backfill': False
}

with DAG(
    dag_id = 'schema_dag',
    default_args = default_args,
    start_date = start_date,
    description= 'Airflow DAG to submit schemas to Apache Pinot',
    schedule_interval = timedelta(days=1),
    tags = ['schema']) as dag:

    start_task = EmptyOperator(task_id='start')

    submit_schema = PinotSchemaSubmitOperator(
        task_id='submit_schemas',
        folder_path = '/opt/airflow/dags/schemas',
        pinot_url='http://pinot-controller:9000/schemas'
    )

    end_task = EmptyOperator(task_id='end')

    start_task >> submit_schema >> end_task