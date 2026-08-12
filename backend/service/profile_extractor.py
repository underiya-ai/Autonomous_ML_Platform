from typing import Any
from schema.state import DatasetProfileState


def extract_profile_data(profile) -> DatasetProfileState:
    """
    Extract structured information from YData Profiling ProfileReport.
    """

    # YData Profiling ka internal structured data
    description = profile.description_set

    # Table-level information
    table = description["table"]

    # Column-level information
    variables = description["variables"]

    state: DatasetProfileState = {
        "dataset_name": "",
        "rows": int(table["n"]),
        "columns": int(table["n_var"]),

        "column_names": [],

        "column_types": {},

        "missing_values": {},

        "missing_percentage": {},

        "unique_values": {},

        "duplicate_rows": int(
            table.get("n_duplicates", 0)
        ),

        "column_details": {}
    }

    
    # Extract every column's information


    for column_name, column_info in variables.items():

        column_name = str(column_name)

        # Column name
        state["column_names"].append(column_name)

        # Data type
        state["column_types"][column_name] = str(
            column_info.get("type", "Unknown")
        )

        # Missing values count
        state["missing_values"][column_name] = int(
            column_info.get("n_missing", 0)
        )

        # Missing percentage
        state["missing_percentage"][column_name] = float(
            column_info.get("p_missing", 0)
        )

        # Unique values
        state["unique_values"][column_name] = int(
            column_info.get("n_unique", 0)
        )

        # Store detailed information
        state["column_details"][column_name] = {
            "type": str(
                column_info.get("type", "Unknown")
            ),

            "missing": int(
                column_info.get("n_missing", 0)
            ),

            "missing_percentage": float(
                column_info.get("p_missing", 0)
            ),

            "unique": int(
                column_info.get("n_unique", 0)
            ),

            "count": int(
                column_info.get("count", 0)
            )
        }

    return state