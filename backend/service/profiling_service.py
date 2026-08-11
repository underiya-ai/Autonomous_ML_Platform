from pathlib import Path

import pandas as pd
from ydata_profiling import ProfileReport


REPORT_DIR = Path("uploads/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_profile_report(file_path: str):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    if file_path.suffix.lower() != ".csv":
        raise ValueError(
            "Currently only CSV files are supported."
        )

    # Load CSV
    df = pd.read_csv(file_path)

    # Generate profile
    profile = ProfileReport(
        df,
        title=f"Dataset Profile - {file_path.name}",
        explorative=True
    )

    # Save report
    report_name = f"{file_path.stem}_profile.html"
    report_path = REPORT_DIR / report_name

    profile.to_file(report_path)

    return {
        "dataset": file_path.name,
        "rows": len(df),
        "columns": len(df.columns),
        "report_name": report_name,
        "report_path": str(report_path)
    }