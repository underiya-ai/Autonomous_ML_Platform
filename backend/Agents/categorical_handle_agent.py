from pathlib import Path

import pandas as pd

from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder
)


ENCODED_DIR = Path("uploads/encoded")
ENCODED_DIR.mkdir(parents=True, exist_ok=True)


def categorical_handling_node(state):

    file_path = Path(state["cleaned_file_path"])
    encoding_plan = state["categorical_encoding_plan"]

    if not file_path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    changes = []
    warnings = []

    actions = encoding_plan.get("actions", [])

    for action in actions:

        column = action.get("column")
        method = action.get("method")

        if column not in df.columns:

            warnings.append(
                f"Skipped '{column}' because "
                f"the column does not exist."
            )

            continue

        if method == "keep":
            continue

        # One-hot encoding
        if method == "one_hot":

            encoder = OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )

            encoded = encoder.fit_transform(
                df[[column]]
            )

            encoded_columns = encoder.get_feature_names_out(
                [column]
            )

            encoded_df = pd.DataFrame(
                encoded,
                columns=encoded_columns,
                index=df.index
            )

            df = pd.concat(
                [
                    df.drop(columns=[column]),
                    encoded_df
                ],
                axis=1
            )

            changes.append({
                "column": column,
                "method": "one_hot",
                "new_columns": encoded_columns.tolist()
            })

        # Ordinal encoding
        elif method == "ordinal":

            encoder = OrdinalEncoder(
                handle_unknown="use_encoded_value",
                unknown_value=-1
            )

            df[column] = encoder.fit_transform(
                df[[column]]
            )

            changes.append({
                "column": column,
                "method": "ordinal"
            })

        else:

            warnings.append(
                f"Skipped '{column}' because "
                f"encoding method '{method}' "
                f"is not supported."
            )

    encoded_name = (
        f"{file_path.stem}_encoded.csv"
    )

    encoded_path = (
        ENCODED_DIR / encoded_name
    )

    df.to_csv(
        encoded_path,
        index=False
    )

    return {
        "encoded_file_path": str(
            encoded_path
        ),
        "changes": changes,
        "warnings": warnings,
        "original_columns": len(
            pd.read_csv(file_path).columns
        ),
        "encoded_columns": len(
            df.columns
        )
    }