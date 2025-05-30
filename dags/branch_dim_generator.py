import random
import pandas as pd
import logging
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
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

number_rows = 50
output_file = './branch_dim_large_data.csv'


def generate_data():
    branch_id = f'B{number_rows:04d}'
    branch_name = f'Branch {number_rows}'
    branch_address = f'{random.randint(1, 9999)} {random.choice(["Main St", "High St", "Broadway", "Elm St"])}'
    city = random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Rio de Janeiro', 'Sao Paulo', 'Buenos Aires', 'João Pessoa', 'Salvador'])
    region = random.choice(['NY', 'CA', 'IL', 'TX', 'AZ', 'RJ', 'SP', 'BA'])
    postcode = f'{random.randint(10000, 99999)}'

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 365))
    opening_date_millis = int(random_date.timestamp() * 1000)

    return branch_id, branch_name, branch_address, city, region, postcode, opening_date_millis

branch_ids = []
branch_names = []
branch_address = []
cities_list = []
regions_list = []
postcodes_list = []
opening_dates = []

def generate_branch_dim_data():
    row_number = 1
    while row_number <= number_rows:
        data = generate_data(row_number)
        branch_ids.append(data[0])
        branch_names.append(data[1])
        branch_address.append(data[2])
        cities_list.append(data[3])
        regions_list.append(data[4])
        postcodes_list.append(data[5])
        opening_dates.append(data[6])
        row_number += 1
    
    df = pd.DataFrame({
        'branch_id': branch_ids,
        'branch_name': branch_names,
        'branch_address': branch_address,
        'city': cities_list,
        'region': regions_list,
        'postcode': postcodes_list,
        'opening_date_millis': opening_dates
    })
    df.to_csv(output_file, index=False)

    logger.info(f"Generated {number_rows} rows of branch dimension data and saved to {output_file}")

with DAG(
    'branch_dim_generator',
    default_args=default_args,
    description='Generate branch dimension data',
    schedule_interval=timedelta(days=1),
    tags=['schema_branch'],
    start_date=start_date
) as dag:

    start_task = EmptyOperator(task_id='start')

    generate_data_task = PythonOperator(
        task_id='generate_branch_dim_data',
        python_callable=generate_branch_dim_data
    )

    end_task = EmptyOperator(task_id='end')

    start_task >> generate_data_task >> end_task