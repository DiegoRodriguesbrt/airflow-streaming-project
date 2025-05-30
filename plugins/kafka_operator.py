from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from datetime import datetime, timedelta
import random
import json
from kafka import KafkaProducer
from airflow.utils.context import Context
from typing import Any


class KafkaProducerOperator(BaseOperator):
    """
    Custom Airflow operator to produce messages to a Kafka topic.
    """
    @apply_defaults
    def __init__(self, kafka_broker, kafka_topic, num_records, *args, **kwargs):
        super(KafkaProducerOperator, self).__init__(*args, **kwargs)
        self.kafka_broker = kafka_broker
        self.kafka_topic = kafka_topic
        self.num_records = num_records

        def generate_transaction_data(self, row_number):
            """
            Generate a single transaction record.
            """
            customer_ids = [f'C{str(i).zfill(5)}' for i in range(1, self.num_records + 1)]
            account_ids = [f'A{str(i).zfill(5)}' for i in range(1, self.num_records + 1)]
            branch_ids = [f'B{str(i).zfill(5)}' for i in range(1, self.num_records + 1)]
            transaction_types = ['deposit', 'withdrawal', 'transfer', 'credit', 'debit']
            currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'BRL']

            transaction_id = f'T{str(row_number).zfill(5)}'
            transaction_date = int(datetime.now() - timedelta(days=random.randint(0, 365)).timestamp() * 1000)
            account_id = random.choice(account_ids)
            customer_id = random.choice(customer_ids)
            branch_id = random.choice(branch_ids)
            transaction_type = random.choice(transaction_types)
            currency = random.choice(currencies)
            transaction_amount = round(random.uniform(10.00, 1000000.00), 2)
            exchange_rate = round(random.uniform(0.5, 1.5), 4)
            

            transaction = {
                'transaction_id': transaction_id,
                'transaction_date': transaction_date,
                'account_id': account_id,
                'customer_id': customer_id,
                'branch_id': branch_id,
                'transaction_type': transaction_type,
                'currency': currency,
                'transaction_amount': transaction_amount,
                'exchange_rate': exchange_rate
            }

            return transaction


        def execute(self, context: Context) -> Any:
            producer = KafkaProducer(
                bootstrap_servers=self.kafka_broker,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

            for row_number in range(1, self.num_records + 1):
                transaction = self.generate_transaction_data(row_number)
                producer.send(self.kafka_topic, value=transaction)
                self.log.info(f"Produced record {row_number}: {transaction}")

            producer.flush()
            self.log.info(f"All {self.num_records} records sent to Kafka topic '{self.kafka_topic}'")
            producer.close()    