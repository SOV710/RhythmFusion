#!/usr/bin/env python3

# convert.py
from pathlib import Path
from csv2json import csv_to_json  # 复用你已有的函数

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def infer_school(csv_file: Path) -> str:
    """blues_1.csv -> blues   classical.csv -> classical"""
    stem = csv_file.stem  # 去掉 .csv
    return stem.split("_", 1)[0]  # 取第一个下划线前的部分


def main() -> None:
    for csv_file in sorted(INPUT_DIR.glob("*.csv")):
        school = infer_school(csv_file)
        json_fn = OUTPUT_DIR / (csv_file.stem + ".json")
        csv_to_json(csv_file, school=school, output=json_fn)
        print(f"✓ {csv_file.name}  →  {json_fn.name}  (School={school})")


if __name__ == "__main__":
    main()
