import pandas as pd
import numpy as np
from pathlib import Path

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

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        if np.isnan(value):
            return None
        return float(value)

    return value


def extract_profile_data(
    file_path: str
) -> DatasetProfileState:

    
    # 1. FILE VALIDATION


    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    if file_path.suffix.lower() != ".csv":
        raise ValueError(
            "Only CSV files are supported."
        )

    
    # 2. LOAD DATASET
    

    df = pd.read_csv(file_path)

    dataset_name = file_path.name

    
    # 3. Dataset Information

    rows = len(df)

    columns = len(df.columns)

    column_names = df.columns.tolist()

    duplicate_rows = int(
        df.duplicated().sum()
    )

    # 4. COLUMN TYPES


    column_types = {
        column: str(df[column].dtype)
        for column in df.columns
    }

    
    # 5. NUMERICAL / CATEGORICAL FEATURES


    numerical_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    
    # 6. INITIAL STATE
    

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

    
    # 7. COLUMN INFORMATION
    

    for column in df.columns:

        series = df[column]

        # Missing values
        missing_count = int(
            series.isna().sum()
        )

        missing_percentage = (
            missing_count / rows * 100
            if rows > 0
            else 0
        )

        # Unique values
        unique_count = int(
            series.nunique(dropna=True)
        )

        # Non-null values
        non_null_count = int(
            series.notna().sum()
        )

        # Data type
        dtype = str(
            series.dtype
        )

    
        # BASIC INFORMATION
        

        state["missing_values"][column] = (
            missing_count
        )

        state["missing_percentage"][column] = round(
            missing_percentage,
            2
        )

        state["unique_values"][column] = (
            unique_count
        )

        
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

        
        # NUMERICAL Columns

        if column in numerical_columns:

            numeric_series = pd.to_numeric(
                series,
                errors="coerce"
            )

            
            # STATISTICS
            

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

            
            # SKEWNEss
            

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

                lower_bound = (
                    q1 - 1.5 * iqr
                )

                upper_bound = (
                    q3 + 1.5 * iqr
                )

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
        # CATEGORICAL FEATUREs

        if column in categorical_columns:

            value_counts = (
                series
                .value_counts(
                    dropna=False
                )
                .head(10)
                .to_dict()
            )

            state["column_details"][column][
                "top_values"
            ] = {
                str(k): int(v)
                for k, v in value_counts.items()
            }

    # 8. CORRELATION


    if len(numerical_columns) >= 2:

        correlation_matrix = df[
            numerical_columns
        ].corr(
            method="pearson"
        )

        for i, column1 in enumerate(
            numerical_columns
        ):

            for column2 in numerical_columns[
                i + 1:
            ]:

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

    # Missing value alerts

    for column in df.columns:

        percentage = state[
            "missing_percentage"
        ][column]

        if percentage > 50:

            state["alerts"].append(
                f"{column} has very high "
                f"missing values ({percentage}%)"
            )

        elif percentage > 10:

            state["alerts"].append(
                f"{column} has significant "
                f"missing values ({percentage}%)"
            )

    # Skewness alerts
    

    for column, skew in state[
        "skewness"
    ].items():

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
            f"Dataset contains "
            f"{duplicate_rows} duplicate rows "
            f"({duplicate_percentage:.2f}%)"
        )


    return state