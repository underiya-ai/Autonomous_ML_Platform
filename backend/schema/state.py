from typing import TypedDict, Any


class DatasetProfileState(TypedDict):
    dataset_name: str

    rows: int
    columns: int

    column_names: list[str]
    column_types: dict[str, str]

    missing_values: dict[str, int]
    missing_percentage: dict[str, float]

    unique_values: dict[str, int]

    duplicate_rows: int

    column_details: dict[str, Any]

    statistics: dict[str, Any]

    skewness: dict[str, float]

    outliers: dict[str, Any]

    correlations: list[dict[str, Any]]

    alerts: list[str]