import ast
import json
from pathlib import Path


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "applications"
OUTPUT_DIR = BASE_DIR / "processed"


def transform_application(file_path):
    """Convert one application log into the required JSON structure."""
    content = file_path.read_text(encoding="utf-8").strip()

    fields = content.split("|", maxsplit=3)

    if len(fields) != 4:
        raise ValueError(f"Invalid application log format: {file_path.name}")

    application = {}

    for field in fields[:3]:
        key, value = field.split("=", maxsplit=1)
        application[key] = value

    site_text = fields[3].split("=", maxsplit=1)[1]
    site_data = ast.literal_eval(site_text)

    site_name = site_data.get("name") or site_data.get("site_name")

    if not site_name or not site_data.get("site_category"):
        raise ValueError(f"Invalid site data: {file_path.name}")

    application["site"] = {
        "name": site_name,
        "category": site_data["site_category"],
    }

    return application


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(INPUT_DIR.iterdir())
    files = [file for file in files if file.is_file()]

    if not files:
        raise FileNotFoundError(f"No application files found in {INPUT_DIR}")

    processed_count = 0

    for file_path in files:
        application = transform_application(file_path)

        output_path = OUTPUT_DIR / f"application-{application['id']}.json"

        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(application, output_file, indent=4, ensure_ascii=False)
            output_file.write("\n")

        processed_count += 1

    print(f"Successfully processed {processed_count} application files.")
    print(f"JSON files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()