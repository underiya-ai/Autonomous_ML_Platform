from typing import TypedDict,Any

class ProfilingReport(TypedDict):
    ReportName:str
    ReportPath:str



class DatasetProfileState(TypedDict):

    dataset_name: str

    rows: int
    columns: int

    column_names: list

    column_types: dict

    numerical_columns: list

    categorical_columns: list

    missing_values: dict

    missing_percentage: dict

    unique_values: dict

    duplicate_rows: int

    column_details: dict

    statistics: dict

    skewness: dict

    outliers: dict

    correlations: list

    alerts: list

class MLState(TypedDict):

    file_path: str

    profile_state: DatasetProfileState

    summary_state: dict
