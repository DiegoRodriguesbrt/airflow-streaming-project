from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.context import Context
import requests
import glob
from typing import Any



class PinotSchemaSubmitOperator(BaseOperator):
    """
    Custom Airflow operator to submit schemas to a Pinot controller.
    """
    @apply_defaults
    def __init__(self, folder_path, pinot_url, *args, **kwargs):
        super(PinotSchemaSubmitOperator, self).__init__(*args, **kwargs)
        self.folder_path = folder_path
        self.pinot_url = pinot_url

    def execute(self, context: Context) -> Any:
        
        try:
            schema_files = glob.glob(f"{self.folder_path}/*.json")
            for schema_file in schema_files:
                with open(schema_file, 'r') as file:
                    schema_data = file.read()
                
                response = requests.post(
                    self.pinot_url,
                    headers={'Content-Type': 'application/json'},
                    data=schema_data
                )
                
                if response.status_code == 200:
                    self.log.info(f"Successfully submitted schema to Apache Pinot: {schema_file}")
                else:
                    self.log.error(f"Failed to submit schema: {schema_file}, Status Code: {response.status_code}, Response: {response.text}")
                    raise Exception(f'Schema submission failed with status code {response.status_code}')
        
        except Exception as e:
            self.log.error(f"Error submitting schemas: {str(e)}")
            raise e