import argparse
import os
import csv
import pandas as pd


def extract_311_2025(input_file: str, output_file: str, date_col: str = "Created Date", chunk_size: int = 100000) -> None:
    """
    Extract records from the full NYC 311 dataset that fall within year 2025.
    The script reads the large CSV file in chunks to reduce memory usage.
    """
    if os.path.exists(output_file):
        os.remove(output_file)

    first_chunk = True
    total_input_rows = 0
    total_output_rows = 0

    print("Start extracting 2025 records...")

    for chunk_index, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size, low_memory=False), start=1):
        total_input_rows += len(chunk)
        print(f"Processing chunk {chunk_index}, rows: {len(chunk)}")

        chunk.columns = chunk.columns.str.strip()

        if date_col not in chunk.columns:
            raise ValueError(f"Column '{date_col}' not found. Available columns: {chunk.columns.tolist()}")

        chunk[date_col] = pd.to_datetime(
            chunk[date_col].astype(str).str.strip(),
            format="%m/%d/%Y %I:%M:%S %p",
            errors="coerce"
        )

        filtered_chunk = chunk[
            (chunk[date_col] >= pd.Timestamp("2025-01-01")) &
            (chunk[date_col] < pd.Timestamp("2026-01-01"))
        ]

        total_output_rows += len(filtered_chunk)

        if len(filtered_chunk) > 0:
            filtered_chunk.to_csv(
                output_file,
                mode="w" if first_chunk else "a",
                index=False,
                header=first_chunk,
                encoding="utf-8-sig",
                quoting=csv.QUOTE_ALL
            )
            first_chunk = False

    print("Extraction finished.")
    print(f"Total input rows: {total_input_rows}")
    print(f"Total output rows: {total_output_rows}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract 2025 records from NYC 311 CSV.")
    parser.add_argument("--input", required=True, help="Path to the full NYC 311 CSV file.")
    parser.add_argument("--output", required=True, help="Path to save the filtered 2025 CSV file.")
    parser.add_argument("--date-col", default="Created Date", help="Date column name.")
    parser.add_argument("--chunk-size", type=int, default=100000, help="Chunk size for reading CSV.")
    args = parser.parse_args()

    extract_311_2025(args.input, args.output, args.date_col, args.chunk_size)
