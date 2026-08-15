from pathlib import Path

import pandas as pd
import numpy as np


CLEANED_DIR = Path("uploads/cleaned")
CLEANED_DIR.mkdir(parents=True, exist_ok=True)


def clean_dataset(file_path: str,cleaning_plan: dict) -> dict:

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}" )

    df = pd.read_csv(file_path)

    original_rows = len(df)
    original_columns = len(df.columns)

    changes = []

    actions = cleaning_plan.get(
        "actions",
        []
    )

    for action in actions:

        column = action.get("column")
        action_type = action.get("action")
        method = action.get("method")

        # drop duplicate

        if action_type == "drop_duplicates":

            before = len(df)

            df = df.drop_duplicates()

            removed = before - len(df)

            changes.append({
                "action": "drop_duplicates",
                "rows_removed": removed
            })

      
        # drop column 
       

        elif action_type == "drop_column":

            if column in df.columns:

                df = df.drop(columns=[column])

                changes.append({
                    "column": column,
                    "action": "drop_column"
                })

        
        # constant column
    

        elif action_type == "remove_constant_column":

            if column in df.columns:

                if df[column].nunique(
                    dropna=False
                ) <= 1:

                    df = df.drop(
                        columns=[column]
                    )

                    changes.append({
                        "column": column,
                        "action": "remove_constant_column"
                    })

        
   # standardize text
        

        elif action_type == "standardize_text":

            if column in df.columns:

                if (df[column].dtype == "object"):

                    df[column] = (
                        df[column]
                        .astype("string")
                        .str.strip()
                    )

                    changes.append({
                        "column": column,
                        "action": "standardize_text"
                    })

        
        # FILL MISSING
        

        elif action_type == "fill_missing":

            if column not in df.columns:
                continue

            if method == "median":

                value = df[column].median()

                df[column] = df[column].fillna(
                    value
                )

            elif method == "mean":

                value = df[column].mean()

                df[column] = df[column].fillna(
                    value
                )

            elif method == "mode":

                mode = df[column].mode()

                if not mode.empty:

                    df[column] = df[column].fillna(
                        mode.iloc[0]
                    )

            elif method == "constant":

                value = action.get("value")

                df[column] = df[column].fillna(
                    value
                )

            changes.append({
                "column": column,
                "action": "fill_missing",
                "method": method
            })

        
        # DROP MISSING ROWS
        

        elif action_type == "drop_missing_rows":

            if column in df.columns:

                before = len(df)

                df = df.dropna(
                    subset=[column]
                )

                removed = before - len(df)

                changes.append({
                    "column": column,
                    "action": "drop_missing_rows",
                    "rows_removed": removed
                })

        
        # CONVERT NUMERIC
        

        elif action_type == "convert_dtype":

            if column not in df.columns:
                continue

            if method == "numeric":

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

            elif method == "datetime":

                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

            changes.append({
                "column": column,
                "action": "convert_dtype",
                "method": method
            })

        
        # OUTLIERS - IQR CLIPPING
        

        elif action_type == "handle_outliers":

            if column not in df.columns:
                continue

            if method == "iqr_clip":

                numeric = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

                q1 = numeric.quantile(0.25)
                q3 = numeric.quantile(0.75)

                iqr = q3 - q1

                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr

                df[column] = numeric.clip(
                    lower=lower,
                    upper=upper
                )

                changes.append({
                    "column": column,
                    "action": "handle_outliers",
                    "method": "iqr_clip"
                })

        
        # SKEWNESS TRANSFORMATION
        

        elif action_type == "transform_skewness":

            if column not in df.columns:
                continue

            if method == "log1p":

                numeric = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

                if (numeric >= 0).all():

                    df[column] = np.log1p(
                        numeric
                    )

                    changes.append({
                        "column": column,
                        "action": "transform_skewness",
                        "method": "log1p"
                    })

    
    # SAVE CLEANED DATASET


    cleaned_name = (f"{file_path.stem}_cleaned.csv")

    cleaned_path = (CLEANED_DIR / cleaned_name)

    df.to_csv(cleaned_path,index=False)

    
    # FINAL REPORT
    

    return {

        "original_rows": original_rows,

        "cleaned_rows": len(df),

        "rows_removed": (
            original_rows - len(df)
        ),

        "original_columns": original_columns,

        "cleaned_columns": len(df.columns),

        "columns_removed": (
            original_columns - len(df.columns)
        ),

        "cleaned_file_path": str(
            cleaned_path
        ),

        "changes": changes
    }