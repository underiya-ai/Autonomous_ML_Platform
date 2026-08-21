from pathlib import Path

import numpy as np
import pandas as pd


CLEANED_DIR = Path("uploads/cleaned")
CLEANED_DIR.mkdir(parents=True, exist_ok=True)


def clean_dataset(
    file_path: str,
    cleaning_plan: dict,
    column_identifier: dict
) -> dict:

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    original_rows = len(df)
    original_columns = len(df.columns)

    changes = []
    warnings = []

    # Get column roles
    column_roles = {
        item["column"]: item["role"]
        for item in column_identifier.get("columns", [])
    }

    actions = cleaning_plan.get("actions", [])

    for action in actions:

        column = action.get("column")
        action_type = action.get("action")
        method = action.get("method")

        # Nothing to do
        if action_type == "keep":
            continue

        # Check column exists
        if (
            column is not None
            and column not in df.columns
            and action_type != "drop_duplicates"
        ):
            warnings.append(
                f"Skipped '{column}' because the column does not exist."
            )
            continue

        # Drop duplicates
        if action_type == "drop_duplicates":

            before = len(df)

            df = df.drop_duplicates()

            rows_removed = before - len(df)

            changes.append({
                "action": "drop_duplicates",
                "rows_removed": rows_removed
            })

        # Drop column
        elif action_type == "drop_column":

            if column in df.columns:

                role = column_roles.get(column)

                # User-approved column removal
                df = df.drop(columns=[column])

                changes.append({
                    "column": column,
                    "action": "drop_column",
                    "role": role,
                    "reason": action.get("reason")
                })

        # Remove constant column
        elif action_type == "remove_constant_column":

            if df[column].nunique(dropna=False) <= 1:

                df = df.drop(columns=[column])

                changes.append({
                    "column": column,
                    "action": "remove_constant_column"
                })

        # Standardize text
        elif action_type == "standardize_text":

            if df[column].dtype == "object":

                df[column] = (
                    df[column]
                    .astype("string")
                    .str.strip()
                )

                changes.append({
                    "column": column,
                    "action": "standardize_text"
                })

        # Fill missing values
        elif action_type == "fill_missing":

            if method == "median":

                value = df[column].median()
                df[column] = df[column].fillna(value)

            elif method == "mean":

                value = df[column].mean()
                df[column] = df[column].fillna(value)

            elif method == "mode":

                mode = df[column].mode()

                if not mode.empty:
                    df[column] = df[column].fillna(mode.iloc[0])

            elif method == "constant":

                value = action.get("value")
                df[column] = df[column].fillna(value)

            changes.append({
                "column": column,
                "action": "fill_missing",
                "method": method
            })

        # Drop rows with missing values
        elif action_type == "drop_missing_rows":

            before = len(df)

            df = df.dropna(subset=[column])

            rows_removed = before - len(df)

            changes.append({
                "column": column,
                "action": "drop_missing_rows",
                "rows_removed": rows_removed
            })

        # Convert data type
        elif action_type == "convert_dtype":

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

        # Remove invalid values
        elif action_type == "remove_invalid_values":

            before = len(df)

            df = df.dropna(subset=[column])

            rows_removed = before - len(df)

            changes.append({
                "column": column,
                "action": "remove_invalid_values",
                "rows_removed": rows_removed
            })

        # Handle outliers
        elif action_type == "handle_outliers":

            role = column_roles.get(column)

            # Only numerical features
            if role != "numerical_feature":

                warnings.append(
                    f"Skipped outlier handling for '{column}' "
                    f"because its role is '{role}'."
                )
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

        # Transform skewness
        elif action_type == "transform_skewness":

            role = column_roles.get(column)

            # Only numerical features
            if role != "numerical_feature":

                warnings.append(
                    f"Skipped skewness transformation for "
                    f"'{column}' because its role is '{role}'."
                )
                continue

            if method == "log1p":

                numeric = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

                valid_values = numeric.dropna()

                if valid_values.empty:
                    continue

                # log1p does not work with negative values
                if (valid_values >= 0).all():

                    df[column] = np.log1p(numeric)

                    changes.append({
                        "column": column,
                        "action": "transform_skewness",
                        "method": "log1p"
                    })

                else:

                    warnings.append(
                        f"Skipped log1p for '{column}' "
                        f"because negative values exist."
                    )

    # Save cleaned dataset
    cleaned_name = f"{file_path.stem}_cleaned.csv"
    cleaned_path = CLEANED_DIR / cleaned_name

    df.to_csv(cleaned_path, index=False)

    # Return cleaning report
    return {
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "rows_removed": original_rows - len(df),
        "original_columns": original_columns,
        "cleaned_columns": len(df.columns),
        "columns_removed": original_columns - len(df.columns),
        "cleaned_file_path": str(cleaned_path),
        "changes": changes,
        "warnings": warnings
    } 