import argparse
import pandas as pd


def pivot_precinct_week(input_file: str, output_file: str) -> None:
    """
    Convert a long-format precinct-week-count table into a wide-format pivot table.

    Expected input columns without header:
    precinct, week, count

    Example:
    Precinct 44, 1, 100

    Output:
    precinct, week_1, week_2, ...
    """
    df = pd.read_csv(
        input_file,
        header=None,
        names=["precinct", "week", "count"]
    )

    df["precinct"] = df["precinct"].astype(str).str.extract(r"(\d+)")
    df["precinct"] = pd.to_numeric(df["precinct"], errors="coerce")
    df["week"] = pd.to_numeric(df["week"], errors="coerce")
    df["count"] = pd.to_numeric(df["count"], errors="coerce")

    df = df.dropna(subset=["precinct", "week", "count"])

    df["precinct"] = df["precinct"].astype(int)
    df["week"] = df["week"].astype(int)
    df["count"] = df["count"].astype(int)

    df = df.groupby(["precinct", "week"], as_index=False)["count"].sum()

    pivot_df = df.pivot_table(
        index="precinct",
        columns="week",
        values="count",
        aggfunc="sum",
        fill_value=0
    )

    pivot_df = pivot_df.sort_index(axis=1)
    pivot_df.columns = [f"week_{col}" for col in pivot_df.columns]
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.sort_values(by="precinct").reset_index(drop=True)

    pivot_df.to_csv(output_file, index=False)

    print("Pivot completed.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert precinct-week long table to pivot table.")
    parser.add_argument("--input", required=True, help="Input long-format CSV file.")
    parser.add_argument("--output", required=True, help="Output pivot CSV file.")
    args = parser.parse_args()

    pivot_precinct_week(args.input, args.output)
