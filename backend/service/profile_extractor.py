import pandas as pd
import numpy as np

from schema.state import DatasetProfileState


def safe_number(value):
    """Convert numpy/pandas values into JSON-safe Python values."""

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    try:
        if hasattr(value, "item"):
            value = value.item()
    except Exception:
        pass

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        if np.isnan(value):
            return None
        return float(value)

    return value


def extract_profile_data(
    df: pd.DataFrame,
    dataset_name: str
) -> DatasetProfileState:

    # DATASET INFORMATION


    rows = len(df)
    columns = len(df.columns)

    column_names = df.columns.tolist()

    duplicate_rows = int(df.duplicated().sum())

    
    # COLUMN TYPES
    

    column_types = {
        column: str(df[column].dtype)
        for column in df.columns
    }

    # NUMERICAL / CATEGORICAL FEATURES
    

    numerical_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    
    # INITIAL STATe

    state = {
        "dataset_name": dataset_name,

        "rows": rows,
        "columns": columns,

        "column_names": column_names,

        "column_types": column_types,

        "numerical_columns": numerical_columns,

        "categorical_columns": categorical_columns,

        "missing_values": {},

        "missing_percentage": {},

        "unique_values": {},

        "duplicate_rows": duplicate_rows,

        "column_details": {},

        "statistics": {},

        "skewness": {},

        "outliers": {},

        "correlations": [],

        "alerts": []
    }


    # COLUMN INFORMATION
    

    for column in df.columns:

        series = df[column]

        missing_count = int(series.isna().sum())

        missing_percentage = (
            missing_count / rows * 100
            if rows > 0
            else 0
        )

        unique_count = int(
            series.nunique(dropna=True)
        )

        non_null_count = int(
            series.notna().sum()
        )

        dtype = str(series.dtype)

        
        # BASIC INFORMATION
    

        state["missing_values"][column] = missing_count

        state["missing_percentage"][column] = round(
            missing_percentage,
            2
        )

        state["unique_values"][column] = unique_count

        
        # COLUMN DETAILS
    

        state["column_details"][column] = {

            "dtype": dtype,

            "missing_values": missing_count,

            "missing_percentage": round(
                missing_percentage,
                2
            ),

            "unique_values": unique_count,

            "non_null_values": non_null_count
        }

    
        # NUMERICAL FEATURES
        

        if column in numerical_columns:

            numeric_series = pd.to_numeric(
                series,
                errors="coerce"
            )

            state["statistics"][column] = {

                "mean": safe_number(
                    numeric_series.mean()
                ),

                "median": safe_number(
                    numeric_series.median()
                ),

                "min": safe_number(
                    numeric_series.min()
                ),

                "max": safe_number(
                    numeric_series.max()
                ),

                "std": safe_number(
                    numeric_series.std()
                ),

                "q25": safe_number(
                    numeric_series.quantile(0.25)
                ),

                "q75": safe_number(
                    numeric_series.quantile(0.75)
                )
            }

            
            # SKEWNESS
            

            skew = numeric_series.skew()

            if pd.notna(skew):

                state["skewness"][column] = round(
                    float(skew),
                    4
                )

            
            # OUTLIERS - IQR METHOD
            

            q1 = numeric_series.quantile(0.25)

            q3 = numeric_series.quantile(0.75)

            iqr = q3 - q1

            if pd.notna(iqr) and iqr != 0:

                lower_bound = q1 - 1.5 * iqr

                upper_bound = q3 + 1.5 * iqr

                outlier_mask = (
                    (numeric_series < lower_bound)
                    |
                    (numeric_series > upper_bound)
                )

                outlier_count = int(
                    outlier_mask.sum()
                )

                outlier_percentage = (
                    outlier_count / rows * 100
                    if rows > 0
                    else 0
                )

                state["outliers"][column] = {

                    "count": outlier_count,

                    "percentage": round(
                        outlier_percentage,
                        2
                    ),

                    "lower_bound": safe_number(
                        lower_bound
                    ),

                    "upper_bound": safe_number(
                        upper_bound
                    )
                }

        
        # CATEGORICAL FEATURES

        if column in categorical_columns:

            value_counts = (
                series
                .value_counts(dropna=False)
                .head(10)
                .to_dict()
            )

            state["column_details"][column][
                "top_values"
            ] = {
                str(k): int(v)
                for k, v in value_counts.items()
            }

    
    # CORRELATION
    

    if len(numerical_columns) >= 2:

        correlation_matrix = df[
            numerical_columns
        ].corr(method="pearson")

        for i, column1 in enumerate(
            numerical_columns
        ):

            for column2 in numerical_columns[i + 1:]:

                value = correlation_matrix.loc[
                    column1,
                    column2
                ]

                if pd.notna(value):

                    state["correlations"].append({

                        "method": "pearson",

                        "feature_1": column1,

                        "feature_2": column2,

                        "correlation": round(
                            float(value),
                            4
                        )
                    })

    
    # ALERTS
    

    # Missing value alerts

    for column in df.columns:

        percentage = state[
            "missing_percentage"
        ][column]

        if percentage > 50:

            state["alerts"].append(
                f"{column} has very high missing values "
                f"({percentage}%)"
            )

        elif percentage > 10:

            state["alerts"].append(
                f"{column} has significant missing values "
                f"({percentage}%)"
            )

    # Skewness alerts

    for column, skew in state["skewness"].items():

        if abs(skew) > 20:

            state["alerts"].append(
                f"{column} is highly skewed "
                f"(skewness={skew})"
            )

    # Duplicate alert

    if duplicate_rows > 0:

        duplicate_percentage = (
            duplicate_rows / rows * 100
        )

        state["alerts"].append(
            f"Dataset contains {duplicate_rows} "
            f"duplicate rows "
            f"({duplicate_percentage:.2f}%)"
        )

    return state