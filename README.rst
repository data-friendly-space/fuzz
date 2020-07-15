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
python fuzz/cli.py -i "input.csv" -o "output.csv" -v "sc_name" -iv "sc_name_bad"
```
