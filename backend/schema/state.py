from typing import TypedDict


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

class SummaryState(TypedDict):

    dataset_summary: str

    data_quality_summary: str

    numerical_features_summary: str

    categorical_features_summary: str

    missing_value_insights: list

    outlier_insights: list

    distribution_insights: list

    correlation_insights: list

    important_findings: list

    cleaning_recommendations: list

    
class MLState(TypedDict):

    file_path: str

    profiling_report: ProfilingReport

    profile_state: DatasetProfileState

    summary_state: SummaryState


