from typing import TypedDict
from pydantic import BaseModel
from typing import List

class ProfilingReport(TypedDict):
    ReportName: str
    ReportPath: str


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



class SummaryState(BaseModel):

    dataset_summary: str

    data_quality_summary: str

    numerical_features_summary: str

    categorical_features_summary: str

    missing_value_insights: List[str]

    outlier_insights: List[str]

    distribution_insights: List[str]

    correlation_insights: List[str]

    important_findings: List[str]

    cleaning_recommendations: List[str]

class MLState(TypedDict):

    file_path: str

    profiling_report: ProfilingReport

    profile_state: DatasetProfileState

    summary_state: SummaryState


