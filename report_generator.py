import json
import os


def generate_report(metadata, output_file="reports/report.json"):

    # Create reports folder if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save metadata as JSON
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print("================================")
    print("REPORT GENERATED SUCCESSFULLY")
    print("================================")
    print(f"Report saved to: {output_file}")