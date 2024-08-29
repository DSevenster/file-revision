import os
import re

# Set directory path (absolute or relative if nested in revision_app directory
directory_path = "revisions"


def ingest_files(
    directory_path: str = "revisions",
) -> dict[str, dict[str, str]]:
    """
    Ingests .py files in a given directory provided they conform to the following
    content structure:
    'revision_id = '<text>''
    'revises_id = '<text>''
    """
    ingested_files = {}

    try:
        file_list = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Directory path {directory_path} does not exist")

    for filename in file_list:
        if filename.endswith(".py"):
            try:
                with open(os.path.join(directory_path, filename), "r") as file:
                    contents = []
                    for line in file:
                        contents.append(content_extraction(line))

                revision_id = contents[0]
                revises_id = contents[1]
                ingested_files[filename] = {
                    "revision_id": revision_id,
                    "revises_id": revises_id,
                }
            except IndexError:
                print(f"{filename} is missing an entry")
    return ingested_files


def content_extraction(content_line: str) -> str:
    """
    Extracts the vale from a given string '= ' and encapsulated in
    ''. If not found, returns None

    """
    match = re.search(r"= '(.*)'", content_line)
    if match:
        id_value = match.group(1)
    else:
        id_value = None

    return id_value


def determine_revision_sequence(ingested_files: dict) -> list:
    """
    Determines the file sequence using the following method:
    - Determine first file where `revises_id` is None

    Takes revision_id from that file
    Determine where revision_id matches revises_id.
    On match, we take the new revision_id and repeat
    """
    file_sequence = []
    first_file = next(
        filename
        for filename, contents in ingested_files.items()
        if contents["revises_id"] is None
    )
    file_sequence.append(first_file)

    while ingested_files[first_file]["revision_id"] is not None:
        current_revision_id = ingested_files[first_file]["revision_id"]

        consecutive_file = next(
            (
                filename
                for filename, content in ingested_files.items()
                if content["revises_id"] == current_revision_id
            ),
            None,
        )

        if not consecutive_file:
            break

        file_sequence.append(consecutive_file)
        first_file = consecutive_file

    return file_sequence


def rename_files(file_sequence: list, directory_path: str):
    """
    Renames files based on the given sequence using the index as numbering, starting at `1`
    """
    for index, filename in enumerate(file_sequence, start=1):
        try:
            corrected_filename = f"{index}_{filename}"
            current_filepath = os.path.join(directory_path, filename)
            renamed_filepath = os.path.join(directory_path, corrected_filename)
            os.rename(current_filepath, renamed_filepath)
        except FileNotFoundError:
            print(f"{filename} not found in {directory_path}")
        except Exception as e:
            print(f"Unexpected error {e} has occurred")


def main(directory_path: str):
    file_contents = ingest_files(directory_path=directory_path)
    ordered_file_sequence = determine_revision_sequence(ingested_files=file_contents)
    rename_files(file_sequence=ordered_file_sequence, directory_path=directory_path)


if __name__ == "__main__":
    main(directory_path)
