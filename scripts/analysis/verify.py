"""Run the preserved independent forensic checks with release-local input paths."""
import argparse
import json
import subprocess
import sys

from evidence import ROOT, checkpoints, derived_destination, verify_copies


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=ROOT / "results")
    args = parser.parse_args()
    output = derived_destination(args.output)
    copied = verify_copies()
    with checkpoints() as paths:
        completed = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/analysis/forensic_checks.py"),
                                    str(paths["assisted-experiment"]), str(paths["preliminary-experiment"])],
                                   capture_output=True, text=True, check=True)
        result = json.loads(completed.stdout)
    assert result["assertions"] == 10953 and not result["anomalies"]
    result["release_immutable_files_verified"] = copied
    (output / "verification.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", "utf-8")
    print(json.dumps({"record_checks": result["assertions"], "anomalies": result["anomalies"], "preserved_files": copied}, indent=2))


if __name__ == "__main__":
    main()
