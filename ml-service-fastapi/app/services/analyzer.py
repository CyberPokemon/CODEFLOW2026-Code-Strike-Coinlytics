import pandas as pd
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

def analyze_transactions(records):
    """
    Analyze transactions by passing data to ML runner via command line.
    Creates a temporary CSV, runs the ML pipeline, and returns results.
    """
    df = pd.DataFrame(records)

    # Get ML directory path
    ml_dir = Path(__file__).resolve().parents[3] / "ML"

    # Rename columns to match ML pipeline expectations
    df = df.rename(columns={
        "particulars": "transaction_statement",
        "txn_date": "Date",
        "credit": "Credit",
        "debit": "Debit",
        "balance": "Balance",
    })

    # Create temporary CSV in system temp directory
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        csv_path = tmp_file.name
        df.to_csv(csv_path, index=False)

    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        # Run ML runner with the CSV path
        runner_result = subprocess.run(
            [sys.executable, str(ml_dir / "runner.py"), csv_path],
            capture_output=True,
            encoding="utf-8",
            text=True,
            cwd=str(ml_dir),
            env=env,
        )

        if runner_result.returncode != 0:
            return {
                "status": "error",
                "message": "ML analysis pipeline failed",
                "runner_output": runner_result.stdout,
                "runner_errors": runner_result.stderr,
            }

        # Extract results from runner output and return
        return {
            "status": "success",
            "runner_output": runner_result.stdout,
            "runner_errors": runner_result.stderr,
        }

    finally:
        # Clean up temporary CSV file
        if os.path.exists(csv_path):
            os.remove(csv_path)
