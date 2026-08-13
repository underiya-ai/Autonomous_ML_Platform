from pathlib import Path
import pandas as pd
from ydata_profiling import ProfileReport

REPORT_DIR = Path("uploads/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_profile_report(file_path: str) -> dict:

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    if file_path.suffix.lower() != ".csv":
        raise ValueError(
            "Only CSV files are supported."
        )

    # Load dataset
    df = pd.read_csv(file_path)

    # Generate YData profiling report
    profile = ProfileReport(
        df,
        title=f"Dataset Profile - {file_path.name}",
        explorative=True
    )

    # Report filename
    report_name = f"{file_path.stem}_profile.html"

    # Report path
    report_path = REPORT_DIR / report_name

    # Save HTML report
    profile.to_file(report_path)

    return {
        "report_name": report_name,
        "report_path": str(report_path)
    }

#  profile_state = extract_profile_data(
#     df,
#     file_path.name
# )