
from schema.state import DatasetProfileState


def safe_number(value):
    """Convert numpy/pandas values into JSON-safe Python values."""
    if value is None:
        return None

    try:
        if hasattr(value, "item"):
            value = value.item()
    except Exception:
        pass

    try:
        if value != value:  # NaN
            return None
    except Exception:
        pass

    return value


def extract_profile_data(
    profile,
    dataset_name: str
) -> DatasetProfileState:

    description = profile.description_set

    # YData sections
    

    variables = description.variables
    table = description.table

    
    # Dataset level information
    

    rows = safe_number(table.n)
    columns = safe_number(table.n_var)
    duplicate_rows = safe_number(
        getattr(table, "n_duplicates", 0)
    )

    state = {
        "dataset_name": dataset_name,

        "rows": int(rows or 0),
        "columns": int(columns or 0),

        "column_names": [],
        "column_types": {},

        "missing_values": {},
        "missing_percentage": {},
        "unique_values": {},

        "duplicate_rows": int(duplicate_rows or 0),

        # Detailed information
        "column_details": {},

        # Statistical information
        "statistics": {},

        # Distribution information
        "skewness": {},

        # Outlier information
        "outliers": {},

        # Correlations
        "correlations": [],

        # YData warnings
        "alerts": []
    }

    # COLUMN INFORMATION
    

    for column_name, column_info in variables.items():

        column_name = str(column_name)

        state["column_names"].append(column_name)


        # Basic information
        

        dtype = safe_number(
            getattr(column_info, "type", None)
        )

        n_missing = safe_number(
            getattr(column_info, "n_missing", 0)
        )

        p_missing = safe_number(
            getattr(column_info, "p_missing", 0)
        )

        n_unique = safe_number(
            getattr(column_info, "n_unique", 0)
        )

        n = safe_number(
            getattr(column_info, "n", rows)
        )

        # Convert percentages if required
        if p_missing is not None:
            p_missing = float(p_missing)

            # YData normally stores this as a proportion
            if p_missing <= 1:
                p_missing *= 100

        
        # Store basic information
        

        state["column_types"][column_name] = str(
            dtype if dtype is not None else "Unknown"
        )

        state["missing_values"][column_name] = int(
            n_missing or 0
        )

        state["missing_percentage"][column_name] = (
            float(p_missing or 0)
        )

        state["unique_values"][column_name] = int(
            n_unique or 0
        )


        # Detailed column information


        non_null = (
            int(n or 0) - int(n_missing or 0)
        )

        state["column_details"][column_name] = {
            "dtype": str(
                dtype if dtype is not None else "Unknown"
            ),

            "missing_values": int(n_missing or 0),

            "missing_percentage": float(
                p_missing or 0
            ),

            "unique_values": int(n_unique or 0),

            "non_null_values": non_null
        }

    
        # NUMERICAL STATISTICS

        mean = safe_number(
            getattr(column_info, "mean", None)
        )

        median = safe_number(
            getattr(column_info, "50%", None)
        )

        minimum = safe_number(
            getattr(column_info, "min", None)
        )

        maximum = safe_number(
            getattr(column_info, "max", None)
        )

        std = safe_number(
            getattr(column_info, "std", None)
        )

        q25 = safe_number(
            getattr(column_info, "25%", None)
        )

        q75 = safe_number(
            getattr(column_info, "75%", None)
        )

        # Some YData versions expose quantiles differently
        if q25 is None:
            q25 = safe_number(
                getattr(column_info, "q25", None)
            )

        if q75 is None:
            q75 = safe_number(
                getattr(column_info, "q75", None)
            )

        # Only store statistics if numerical information exists
        if any(
            x is not None
            for x in [
                mean,
                median,
                minimum,
                maximum,
                std,
                q25,
                q75
            ]
        ):

            state["statistics"][column_name] = {
                "mean": mean,
                "median": median,
                "min": minimum,
                "max": maximum,
                "std": std,
                "q25": q25,
                "q75": q75
            }

        
        # SKEWNESS
        

        skewness = safe_number(
            getattr(column_info, "skewness", None)
        )

        if skewness is not None:

            state["skewness"][column_name] = (
                float(skewness)
            )

        
        # OUTLIER INFORMATION
        

        # YData may expose extreme values / outlier counts
        outlier_count = safe_number(
            getattr(column_info, "n_extreme_obs", None)
        )

        if outlier_count is not None:

            state["outliers"][column_name] = {
                "count": int(outlier_count)
            }


    
    # CORRELATION INFORMATIon

    correlations = getattr(
        description,
        "correlations",
        None
    )

    if correlations:

        try:

            # Handle correlation objects/dataframes
            for correlation_name, correlation_data in correlations.items():

                if correlation_data is None:
                    continue

                # pandas DataFrame
                if hasattr(correlation_data, "columns"):

                    columns_list = list(
                        correlation_data.columns
                    )

                    for col1 in columns_list:

                        for col2 in columns_list:

                            if col1 >= col2:
                                continue

                            try:
                                value = correlation_data.loc[
                                    col1,
                                    col2
                                ]

                                value = safe_number(value)

                                if value is None:
                                    continue

                                state["correlations"].append({
                                    "method": correlation_name,
                                    "feature_1": str(col1),
                                    "feature_2": str(col2),
                                    "correlation": float(value)
                                })

                            except Exception:
                                continue

        except Exception:
            pass


    
    # YDATA ALERTS
    

    alerts = getattr(
        description,
        "alerts",
        None
    )

    if alerts:

        try:

            for alert in alerts:

                state["alerts"].append(
                    str(alert)
                )

        except Exception:
            pass


    return state