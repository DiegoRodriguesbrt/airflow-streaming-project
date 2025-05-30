import random
import pandas as pd
import logging
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG

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
output_file = './account_dim_large_data.csv'

account_ids = []
account_types = []
statuses = []
customer_ids = []
balances = []
opening_dates = []


def generate_data():
    account_id = f'A{number_rows:05d}'
    account_type = random.choice(['savings', 'checking', 'credit'])
    status = random.choice(['active', 'inactive', 'closed'])
    customer_id = f'C{random.randint(1, 1000):05d}'
    balance = round(random.uniform(100.00, 100000.00), 2)

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 365))
    opening_date_millis = int(random_date.timestamp() * 1000)

    return account_id, account_type, status, customer_id, balance, opening_date_millis


def generate_account_dim_data():
    row_number = 1
    while row_number <= number_rows:
        account_id, account_type, status, customer_id,balance, opening_date_millis = generate_data()
        account_ids.append(account_id)
        account_types.append(account_type)
        statuses.append(status)
        customer_ids.append(customer_id)
        balances.append(balance)
        opening_dates.append(opening_date_millis)
        row_number += 1

    df = pd.DataFrame({
        'account_id': account_ids,
        'account_type': account_types,
        'status': statuses,
        'customer_id': customer_ids,
        'balance': balances,
        'opening_date_millis': opening_dates
    })

    df.to_csv(output_file, index=False)
    logger.info(f"Generated {number_rows} rows of account dimension data and saved to {output_file}")


with DAG('account_dim_generator',
         default_args=default_args,
         description='Generate account dimension data',
         schedule_interval=timedelta(days=1),
         start_date=start_date,
         tags=['schema_account']) as dag:

    start_task = EmptyOperator(
        task_id='start'
    )

    generate_data_task = PythonOperator(
        task_id='generate_account_dim_data',
        python_callable=generate_account_dim_data
    )

    end_task = EmptyOperator(
        task_id='end'
    )

    start_task >> generate_data_task >> end_task