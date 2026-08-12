from typing import TypedDict, Any


class DatasetProfileState(TypedDict, total=False):
    dataset_name: str
    rows: int
    columns: int
    column_names: list[str]
    column_types: dict[str, str]
    missing_values: dict[str, int]
    missing_percentage: dict[str, float]
    unique_values: dict[str, int]
    duplicate_rows: int
    profile_data: dict[str, Any]