#!/usr/bin/env python3

# csv2json.py
import csv
import json
import argparse
from pathlib import Path


def csv_to_json(
    csv_path: str | Path,
    *,
    school: str,
    output: str | Path | None = None,
    encoding: str = "utf-8",
) -> list[dict]:
    """Convert the CSV at *csv_path* to the target JSON list."""
    keep = ("Track name", "Artist name")  # 仅保留这两列
    result: list[dict] = []

    with open(csv_path, newline="", encoding=encoding) as f:
        for row in csv.DictReader(f):
            record = {k: row[k] for k in keep}
            record["School"] = school  # 新增字段
            result.append(record)

    if output:  # 写文件；否则直接返回
        with open(output, "w", encoding=encoding) as out:
            json.dump(result, out, ensure_ascii=False, indent=2)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Convert a Spotify-like CSV to slim JSON (Track name, Artist name, School)."
    )
    ap.add_argument("csvfile", help="input CSV file")
    ap.add_argument(
        "school", help="value to insert into the School field of every item"
    )
    ap.add_argument(
        "-o", "--output", help="output JSON file (default: print to stdout)"
    )
    args = ap.parse_args()

    data = csv_to_json(args.csvfile, school=args.school, output=args.output)
    if args.output is None:  # 未指定 -o 时，打印到 stdout
        print(json.dumps(data, ensure_ascii=False, indent=2))
