from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.context import Context
import requests
import glob
from typing import Any



class PinotTableSubmitOperator(BaseOperator):
    """
    Custom Airflow operator to submit tables to a Pinot controller.
    """
    @apply_defaults
    def __init__(self, folder_path, pinot_url, *args, **kwargs):
        super(PinotTableSubmitOperator, self).__init__(*args, **kwargs)
        self.folder_path = folder_path
        self.pinot_url = pinot_url

    def execute(self, context: Context) -> Any:
        
        try:
            table_files = glob.glob(f"{self.folder_path}/*.json")
            for table_file in table_files:
                with open(table_file, 'r') as file:
                    table_data = file.read()
                
                response = requests.post(
                    self.pinot_url,
                    headers={'Content-Type': 'application/json'},
                    data=table_data
                )
                
                if response.status_code == 200:
                    self.log.info(f"Successfully submitted table to Apache Pinot: {table_file}")
                else:
                    self.log.error(f"Failed to submit table: {table_file}, Status Code: {response.status_code}, Response: {response.text}")
                    raise Exception(f'table submission failed with status code {response.status_code}')
        
        except Exception as e:
            self.log.error(f"Error submitting tables: {str(e)}")
            raise e