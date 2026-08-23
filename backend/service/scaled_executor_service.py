from pathlib import Path
from schema.state import MLState

import pandas as pd

from sklearn.preprocessing import (
StandardScaler,
RobustScaler,
MinMaxScaler,
MaxAbsScaler
)

SCALED_DIR = Path("uploads/scaled")
SCALED_DIR.mkdir(parents=True, exist_ok=True)

def scaling_executor_node(state:MLState):

    file_path = Path(state["encoded_file_path"])
    scaling_plan = state["scaling_plan"]

    if not file_path.exists():
      raise FileNotFoundError(
        f"Encoded dataset not found: {file_path}"
    )

    df = pd.read_csv(file_path)

    changes = []
    warnings = []

    actions = scaling_plan.get("actions", [])

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

    # Standard scaling
     if method == "standard":

        scaler = StandardScaler()

        df[[column]] = scaler.fit_transform(
            df[[column]]
        )

        changes.append({
            "column": column,
            "method": "standard"
        })

    # Robust scaling
     elif method == "robust":

        scaler = RobustScaler()

        df[[column]] = scaler.fit_transform(
            df[[column]]
        )

        changes.append({
            "column": column,
            "method": "robust"
        })

    # Min-max scaling
     elif method == "minmax":

        scaler = MinMaxScaler()

        df[[column]] = scaler.fit_transform(
            df[[column]]
        )

        changes.append({
            "column": column,
            "method": "minmax"
        })

    # Max-absolute scaling
     elif method == "maxabs":

        scaler = MaxAbsScaler()

        df[[column]] = scaler.fit_transform(
            df[[column]]
        )

        changes.append({
            "column": column,
            "method": "maxabs"
        })

    else:

        warnings.append(
            f"Skipped '{column}' because "
            f"scaling method '{method}' "
            f"is not supported."
        )

    scaled_name = f"{file_path.stem}_scaled.csv"

    scaled_path = SCALED_DIR / scaled_name

    df.to_csv(
    scaled_path,
    index=False
)

    return {
    "scaled_file_path": str(scaled_path),
    "changes": changes,
    "warnings": warnings,
    "original_columns": len(pd.read_csv(file_path).columns),
    "scaled_columns": len(df.columns)
}






