from pathlib import Path
import pandas as pd
from ydata_profiling import ProfileReport

from service.profile_extractor import extract_profile_data


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
            "only CSV files are supported."
        )

    # Load CSV
    df = pd.read_csv(file_path)

    # Create YData profile
    profile = ProfileReport(
        df,
        title=f"Dataset Profile - {file_path.name}",
        explorative=True
    )

    # Save HTML report for client
    report_name = f"{file_path.stem}_profile.html"
    report_path = REPORT_DIR / report_name

    profile.to_file(report_path)

    # Extract structured data from YData profile
    profile_state = extract_profile_data(profile)

    # Add dataset name
    profile_state["dataset_name"] = file_path.name

    return profile_state