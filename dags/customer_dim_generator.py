import random
import pandas as pd
import logging
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta

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

number_rows = 150
output_file = './customer_dim_large_data.csv'

customer_id = []
first_name = []
last_name = []
email = []
phone_number = []

def generate_data():
    customer_id = f'C{number_rows:05d}'
    firt_name = f'FirstName{number_rows}'
    last_name = f'LastName{number_rows}'
    email = f'{firt_name.lower()}.{last_name.lower()}@example.com'
    phone_number = f'{random.randint(1000000000, 9999999999)}'
   
    return customer_id, firt_name, last_name, email, phone_number


def generate_customer_dim_data():
    row_number = 1
    while row_number <= number_rows:
        data = generate_data()
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
    