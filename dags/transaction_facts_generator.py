from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators import EmptyOperator, PythonOperator
from kafka_operator import KafkaProducerOperator


start_date = datetime(2025, 3, 27)
default_args = {
    'owner': 'project-airflow',
    'depends_on_past': False,
    'backfill': False
}

with DAG(
    dag_id='transaction_facts_generator',
    default_args=default_args,
    start_date=start_date,
    description='Generate transaction facts data into kafka',
    schedule_interval=timedelta(days=1),
    tags=['fact_transaction']
) as dag:

    start_task = EmptyOperator(task_id='start')

    generate_transaction_data = KafkaProducerOperator(
        task_id = 'generate_transaction_facts_data',
        kafka_broker = 'kafka:9092',
        kafka_topic = 'transaction_facts',
        num_records = 100
    )

    end_task = EmptyOperator(task_id='end')

    start_task >> generate_transaction_data >> end_task