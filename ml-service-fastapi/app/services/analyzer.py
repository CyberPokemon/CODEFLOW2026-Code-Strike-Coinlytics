import pandas as pd
import json
import os
import subprocess
import sys
from pathlib import Path

def analyze_transactions(records):

    df = pd.DataFrame(records)

    ml_dir = Path(__file__).resolve().parents[3] / "ML"
    infer_dir = ml_dir / "infer"
    results_dir = ml_dir / "results"
    infer_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    df = df.rename(columns={
        "particulars": "transaction_statement",
        "txn_date": "Date",
        "credit": "Credit",
        "debit": "Debit",
        "balance": "Balance",
    })

    csv_path = infer_dir / "transactions.csv"
    df.to_csv(csv_path, index=False)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    runner_result = subprocess.run(
        [sys.executable, str(ml_dir / "runner.py"), str(csv_path)],
        capture_output=True,
        encoding="utf-8",
        text=True,
        cwd=ml_dir,
        env=env,
    )

    if runner_result.returncode != 0:
        return {
            "status": "error",
            "message": "ML analysis pipeline failed",
            "runner_output": runner_result.stdout,
            "runner_errors": runner_result.stderr,
        }

    results_path = results_dir / "analysis_results.json"
    with open(results_path, "r", encoding="utf-8") as f:
        return json.load(f)
