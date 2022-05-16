import os
import uuid
import great_expectations as ge
import json
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.profile.json_schema_profiler import JsonSchemaProfiler
from ruamel import yaml
from great_expectations.data_context.types.base import DataContextConfig, DatasourceConfig, \
    FilesystemStoreBackendDefaults
from great_expectations.data_context import BaseDataContext
import warnings


class GreatExepectationsValidator:
    context = None
    expectations = None

    def __init__(self):
        data_context_config = DataContextConfig(
            store_backend_defaults=FilesystemStoreBackendDefaults(root_directory=f"{os.getcwd()}/store"),
        )
        self.context = BaseDataContext(project_config=data_context_config)

    def set_expectations(self, file_path):
        with open(file_path, 'r') as file:
            exp_suite = json.load(file)
        self.context.create_expectation_suite(overwrite_existing=True, **exp_suite)

    def set_schema(self, schema):
        self.context.create_expectation_suite(overwrite_existing=True, **schema)

    def validate_csv(self, csv_path):
        run_id = str(uuid.uuid4())
        datasource_yaml = f"""
        name: {run_id}
        class_name: Datasource
        module_name: great_expectations.datasource
        execution_engine:
          module_name: great_expectations.execution_engine
          class_name: PandasExecutionEngine
        data_connectors:
            default_runtime_data_connector_name:
                class_name: RuntimeDataConnector
                batch_identifiers:
                    - default_identifier_name
            default_inferred_data_connector_name:
                class_name: ConfiguredAssetFilesystemDataConnector
                base_directory: {csv_path}
                assets:
                  csv_dataset:
                    pattern: (.*)\.csv
                    group_names:
                        - primary
        """
        self.context.test_yaml_config(datasource_yaml)
        self.context.add_datasource(**yaml.safe_load(datasource_yaml))
        batch_request = RuntimeBatchRequest(
            datasource_name=run_id,
            data_connector_name="default_runtime_data_connector_name",
            data_asset_name=csv_path,  # This can be anything that identifies this data_asset for you
            runtime_parameters={"path": csv_path},  # Add your path here.
            batch_identifiers={"default_identifier_name": "default_identifier"},
        )
        self.context.create_expectation_suite(
            expectation_suite_name="test_suite", overwrite_existing=True
        )
        validator = self.context.get_validator(
            batch_request=batch_request, expectation_suite_name="test_suite"
        )
