import os
import pandas as pd
import matplotlib.pyplot as plt


OUTPUT_DIR = "outputs/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_nypd_monthly_by_borough(input_csv: str):
    df = pd.read_csv(input_csv)
    df["Month"] = pd.to_numeric(df["Month"])
    df["Value"] = pd.to_numeric(df["Value"])
    df = df.sort_values(["Borough", "Month"])

    plt.figure(figsize=(12, 7))
    plt.style.use("ggplot")

    for borough in df["Borough"].unique():
        subset = df[df["Borough"] == borough]
        plt.plot(subset["Month"], subset["Value"], marker="o", linewidth=2, label=borough)

    plt.title("NYPD Monthly Complaint Counts by Borough")
    plt.xlabel("Month (January - December)")
    plt.ylabel("Total Complaints")
    plt.xticks(range(1, 13))
    plt.legend(title="Borough", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, "nypd_monthly_by_borough.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_crime_age_severity(input_csv: str):
    df = pd.read_csv(input_csv)

    age_order = ["<18", "18-24", "25-44", "45-64", "65+"]
    df["Age_Group"] = pd.Categorical(df["Age_Group"], categories=age_order, ordered=True)
    df = df.sort_values(["Age_Group", "Case_Type"])

    plt.figure(figsize=(14, 8))
    case_types = df["Case_Type"].unique()
    x_positions = range(len(age_order))
    width = 0.25

    for i, case_type in enumerate(case_types):
        subset = df[df["Case_Type"] == case_type]
        values = [subset[subset["Age_Group"] == age]["Count"].sum() for age in age_order]
        positions = [x + (i - 1) * width for x in x_positions]
        bars = plt.bar(positions, values, width=width, label=case_type)

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f"{int(height):,}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold"
                )

    plt.title("Crime Counts Distribution by Age and Severity")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Cases")
    plt.xticks(list(x_positions), age_order)
    plt.legend(title="Case Severity")
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, "crime_age_severity.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_crime_age_gender(input_csv: str):
    df = pd.read_csv(input_csv)

    age_order = ["<18", "18-24", "25-44", "45-64", "65+"]
    df["Age_Group"] = pd.Categorical(df["Age_Group"], categories=age_order, ordered=True)
    df = df.sort_values(["Age_Group", "Gender"])

    plt.figure(figsize=(14, 8))
    genders = ["M", "F"]
    x_positions = range(len(age_order))
    width = 0.35

    for i, gender in enumerate(genders):
        subset = df[df["Gender"] == gender]
        values = [subset[subset["Age_Group"] == age]["Count"].sum() for age in age_order]
        positions = [x + (i - 0.5) * width for x in x_positions]
        bars = plt.bar(positions, values, width=width, label=gender)

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f"{int(height):,}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold"
                )

    plt.title("Crime Counts by Age Group and Gender")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Cases")
    plt.xticks(list(x_positions), age_order)
    plt.legend(title="Gender")
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, "crime_age_gender.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_nypd_borough_pie(input_csv: str):
    df = pd.read_csv(input_csv)
    df["Value"] = pd.to_numeric(df["Value"])

    totals = df.groupby("Borough")["Value"].sum().sort_values(ascending=False)

    plt.figure(figsize=(9, 7))
    plt.pie(
        totals.values,
        labels=totals.index,
        autopct="%1.1f%%",
        startangle=140
    )

    plt.title("Annual NYPD Complaint Distribution by Borough")
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, "nypd_borough_distribution.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    print("NYPD visualization script.")
    print("Example usage:")
    print("plot_nypd_monthly_by_borough('data/nypd_monthly_data.csv')")
    print("plot_crime_age_severity('data/age_counts.csv')")
    print("plot_crime_age_gender('data/gender_age_counts.csv')")
    print("plot_nypd_borough_pie('data/nypd_monthly_data.csv')")
