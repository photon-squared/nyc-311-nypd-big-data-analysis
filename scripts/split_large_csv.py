import argparse
import os
import math


def split_csv(input_file: str, output_dir: str, num_parts: int = 5) -> None:
    """
    Split a large CSV file into multiple smaller CSV files while preserving the header.
    """
    os.makedirs(output_dir, exist_ok=True)

    print("Counting total rows...")
    with open(input_file, "r", encoding="utf-8-sig", errors="replace") as f:
        header = f.readline()
        total_rows = sum(1 for _ in f)

    rows_per_part = math.ceil(total_rows / num_parts)

    print(f"Total data rows: {total_rows}")
    print(f"Rows per part: {rows_per_part}")

    print("Splitting file...")

    with open(input_file, "r", encoding="utf-8-sig", errors="replace", newline="") as infile:
        header = infile.readline()

        part_index = 1
        row_count_in_part = 0

        out_path = os.path.join(output_dir, f"part_{part_index}.csv")
        outfile = open(out_path, "w", encoding="utf-8-sig", newline="")
        outfile.write(header)

        for line_num, line in enumerate(infile, start=1):
            if row_count_in_part >= rows_per_part and part_index < num_parts:
                outfile.close()
                print(f"Saved: {out_path}")

                part_index += 1
                row_count_in_part = 0

                out_path = os.path.join(output_dir, f"part_{part_index}.csv")
                outfile = open(out_path, "w", encoding="utf-8-sig", newline="")
                outfile.write(header)

            outfile.write(line)
            row_count_in_part += 1

            if line_num % 100000 == 0:
                print(f"Processed {line_num} rows...")

        outfile.close()
        print(f"Saved: {out_path}")

    print("Done.")
    print(f"Output folder: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a large CSV file into multiple parts.")
    parser.add_argument("--input", required=True, help="Input CSV file path.")
    parser.add_argument("--output-dir", required=True, help="Output directory for split files.")
    parser.add_argument("--num-parts", type=int, default=5, help="Number of output parts.")
    args = parser.parse_args()

    split_csv(args.input, args.output_dir, args.num_parts)
