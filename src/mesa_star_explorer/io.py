from pathlib import Path
import pandas as pd


def validate_file(filepath):
    """
    Check file exists.
    """

    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(
            f"{filepath} not found"
        )
    return filepath


def load_mesa_table(filepath):
    """
    Read MESA table.
    """
    filepath = validate_file(filepath)
    with open(filepath) as f:
        lines = f.readlines()
    metadata = {}

    # Metadata block
    metadata_keys = lines[1].split()
    metadata_values = lines[2].split()
    for key, value in zip(
        metadata_keys,
        metadata_values
    ):
        metadata[key] = value.strip('"')

    # Column names
    columns = lines[5].split()

    # Numerical table
    data = pd.read_csv(
        filepath,
        skiprows=6,
        sep=r"\s+",
        names=columns,
        engine="python"
    )
    return metadata, data

def load_multiple(files):

    models = []
    for file in files:
        meta, data = load_mesa_table(file)
        models.append(
            {
                "metadata": meta,
                "data": data
            }
        )
    return models