# Fuzz

## Getting Started

1. Install poetry

```bash
pip install poetry --user
```

2. Install dependencies

```bash
poetry install
```

3. Activate shell

```bash
poetry shell
```

4. Run cli

```bash
python fuzz/cli.py -i "input.csv" -o "output.csv" -v "sc_name" -iv "sc_name_bad" --unique
```

## Usage

```
usage: fuzz [-h] -i input file -v VALID_COLUMN_NAME -iv INVALID_COLUMN_NAME -o output file [-u]

Match with some fuzz

optional arguments:
  -h, --help            show this help message and exit
  -i input file, --input-file input file
                        Path to input file
  -v VALID_COLUMN_NAME, --valid-column-name VALID_COLUMN_NAME
                        Name of the column with valid values
  -iv INVALID_COLUMN_NAME, --invalid-column-name INVALID_COLUMN_NAME
                        Name of the column with invalid values
  -o output file, --output-file output file
                        Path to output file
  -u, --unique          Only include unique values on output
```
