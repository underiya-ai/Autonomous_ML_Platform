from typing import TypedDict,Literal,Optional,List,NotRequired
from pydantic import BaseModel,Field




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
    cleaned_file_path: NotRequired[str]
    profile_state: DatasetProfileState
    column_identifier_state: dict
    summary_state: dict
    cleaning_plan: dict
    cleaning_state: dict
    




class CleaningActionState(BaseModel):

    column: Optional[str] = None

    action: Literal[
        "drop_column",
        "drop_duplicates",
        "fill_missing",
        "drop_missing_rows",
        "convert_dtype",
        "standardize_text",
        "remove_invalid_values",
        "handle_outliers",
        "transform_skewness",
        "remove_constant_column",
        "keep"
    ]

    reason: str
    method: Optional[str] = None
    value: Optional[str] = None


class CleaningPlanState(BaseModel):

    actions: List[CleaningActionState]
    important_warnings: List[str]
    summary: str


class ColumnRoleState(BaseModel):

    column: str
    role: Literal[
        "identifier",
        "entity_identifier",
        "numerical_feature",
        "categorical_feature",
        "datetime",
        "text",
        "boolean",
        "constant"
    ]

    confidence: Literal["high","medium","low"]
    reason: str


class ColumnIdentifierState(BaseModel):

    columns: List[ColumnRoleState]
    important_warnings: List[str]
    summary: str