import glob
import os
from typing import Dict


github_output = []
service_map = {
    "cf-template": "aws-cloudformation",
    "lambda-code": "aws-lambda",
    "state-machine": "aws-stepfunction",
    "glue-code": "aws-glue",
    "ecs-code": "aws-ecs",
}


def load_text_to_dict(file_path) -> Dict:
    """Reads a text file and loads it into a dictionary."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                entry = f"{service_map.get(line.strip().split('/')[0])}='true'"
                if (
                    not line.startswith(".")
                    and entry not in github_output
                    and line.split("/")[0] in service_map
                ):
                    github_output.append(entry)

            for service in service_map.values():
                print(f"Checking for {service}")
                if service not in [x.split("=")[0] for x in github_output]:
                    entry = f"{service}='false'"
                    github_output.append(entry)

        return github_output
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except RuntimeError as e:
        print(f"An error occurred: {e}")


def inspect_files(pattern):
    """Reads multiple text files matching a pattern and loads them into a dictionary."""
    try:
        combined_dict = {}
        for file_path in glob.glob(pattern):
            print(f"Processing file: {file_path}")
            combined_dict = load_text_to_dict(file_path)

        return combined_dict
    except RuntimeError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    FILE_PATTERN = "*-files.txt"
    github_output = inspect_files(pattern=FILE_PATTERN)

    print(github_output)

    output_file_path = os.getenv("GITHUB_OUTPUT", "/dev/null")
    with open(output_file_path, "a", encoding="utf-8") as output_file:
        for output in github_output:
            output_file.write(f"{output}\n")
