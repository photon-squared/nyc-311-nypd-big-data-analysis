import argparse
import pandas as pd


def merge_precinct_week(complaint_file: str, crime_file: str, output_file: str) -> None:
    """
    Merge 311 complaint counts and NYPD crime counts at the precinct-week level.

    Inputs are expected to be wide-format pivot tables:
    precinct, week_1, week_2, ...

    Output is a long-format table:
    precinct, week, complaint_count, crime_count
    """
    df_311 = pd.read_csv(complaint_file)
    df_nypd = pd.read_csv(crime_file)

    df_311["precinct"] = df_311["precinct"].astype(int)
    df_nypd["precinct"] = df_nypd["precinct"].astype(int)

    df_311_long = df_311.melt(
        id_vars="precinct",
        var_name="week",
        value_name="complaint_count"
    )

    df_nypd_long = df_nypd.melt(
        id_vars="precinct",
        var_name="week",
        value_name="crime_count"
    )

    df_311_long["week"] = df_311_long["week"].astype(str).str.extract(r"(\d+)").astype(int)
    df_nypd_long["week"] = df_nypd_long["week"].astype(str).str.extract(r"(\d+)").astype(int)

    df_311_long["complaint_count"] = pd.to_numeric(
        df_311_long["complaint_count"],
        errors="coerce"
    ).fillna(0).astype(int)

    df_nypd_long["crime_count"] = pd.to_numeric(
        df_nypd_long["crime_count"],
        errors="coerce"
    ).fillna(0).astype(int)

    merged_df = pd.merge(
        df_311_long,
        df_nypd_long,
        on=["precinct", "week"],
        how="inner"
    )

    merged_df = merged_df.sort_values(["precinct", "week"]).reset_index(drop=True)

    merged_df.to_csv(output_file, index=False)

    print("Merge completed.")
    print(f"Saved to: {output_file}")
    print("Shape:", merged_df.shape)
    print(merged_df.head())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge 311 and NYPD precinct-week pivot tables.")
    parser.add_argument("--complaints", required=True, help="311 precinct-week pivot CSV.")
    parser.add_argument("--crimes", required=True, help="NYPD precinct-week pivot CSV.")
    parser.add_argument("--output", required=True, help="Output merged CSV file.")
    args = parser.parse_args()

    merge_precinct_week(args.complaints, args.crimes, args.output)
