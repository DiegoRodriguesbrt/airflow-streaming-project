import random
import pandas as pd
import logging
from faker import Faker
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

fake = Faker()

start_date = datetime(2025,3,27)
default_args = {
    'owner': 'project-airflow',
    'depends_on_past': False,
    'backfill': False
}

number_rows = 150
output_file = '/opt/airflow/dags/customer_dim_large_data.csv'

customer_id = []
first_name = []
last_name = []
email = []
phone_number = []

def generate_data(row_number):
    customer_id = f'C{row_number:05d}'
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f'{first_name.lower()}.{last_name.lower()}@example.com'
    phone_number = fake.phone_number()
   
    return customer_id, first_name, last_name, email, phone_number


def generate_customer_dim_data():
    row_number = 1
    while row_number <= number_rows:
        data = generate_data(row_number)
        customer_id.append(data[0])
        first_name.append(data[1])
        last_name.append(data[2])
        email.append(data[3])
        phone_number.append(data[4])
        row_number += 1
    
    df = pd.DataFrame({
        'customer_id': customer_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone_number': phone_number
    })
    
    df.to_csv(output_file, index=False)
    logger.info(f"Customer dimension data generated and saved to {output_file}")

with DAG(
    dag_id='customer_dim_generator',
    default_args=default_args,
    start_date=start_date,
    schedule_interval=timedelta(days=1),
    tags=['schema_customer']
) as dag:

    start_task = EmptyOperator(task_id='start')

    generate_data_task = PythonOperator(
        task_id='generate_customer_dim_data',
        python_callable=generate_customer_dim_data
    )

    end_task = EmptyOperator(task_id='end')

    start_task >> generate_data_task >> end_task
    