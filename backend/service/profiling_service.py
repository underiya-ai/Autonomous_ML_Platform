from pathlib import Path
import pandas as pd
from ydata_profiling import ProfileReport

from service.profile_extractor import extract_profile_data


REPORT_DIR = Path("uploads/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_profile_report(file_path: str):

    file_path = Path(file_path)

    # Check file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    # Currently only CSV
    if file_path.suffix.lower() != ".csv":
        raise ValueError(
            "Only CSV files are supported."
        )

    # Load dataset
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

    report_path = REPORT_DIR / report_name

# Save HTML report
    profile.to_file(report_path)

# Extract structured dataset information
    profile_state = extract_profile_data(
    df,
    file_path.name
)

    return {
    "profile_state": profile_state,
    "report_name": report_name,
    "report_path": str(report_path)
}