import os
import pandas as pd
import matplotlib.pyplot as plt


OUTPUT_DIR = "outputs/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_311_monthly_by_borough(input_csv: str):

    df = pd.read_csv(input_csv)

    df["Month"] = pd.to_numeric(df["Month"])
    df["Complaints"] = pd.to_numeric(df["Complaints"])

    df = df.sort_values(["Borough", "Month"])

    plt.figure(figsize=(12, 7))
    plt.style.use("ggplot")

    for borough in df["Borough"].unique():

        subset = df[df["Borough"] == borough]

        plt.plot(
            subset["Month"],
            subset["Complaints"],
            marker="o",
            linewidth=2,
            label=borough
        )

    plt.title(
        "311 Monthly Complaint Counts by Borough (2025)"
    )

    plt.xlabel("Month (January - December)")
    plt.ylabel("Total Complaints")

    plt.xticks(range(1, 13))

    plt.legend(
        title="Borough",
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()

    output_path = os.path.join(
        OUTPUT_DIR,
        "311_monthly_by_borough.png"
    )

    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    plt.close()

    print(f"Saved: {output_path}")


def plot_311_department_bar():

    data = {
        "Department": [
            "NYPD",
            "HPD",
            "DSNY",
            "DOT",
            "DEP",
            "Parks",
            "DOB",
            "DOHMH",
            "DHS",
            "TLC",
            "NYCEDC",
            "DCWP",
            "DOE",
            "Sheriff",
            "OTI"
        ],

        "Complaints": [
            1717594,
            774457,
            326780,
            212108,
            197143,
            110855,
            103061,
            83396,
            51449,
            36225,
            20554,
            18278,
            1737,
            1111,
            214
        ]
    }

    df = pd.DataFrame(data)

    df = df.sort_values(
        "Complaints",
        ascending=True
    )

    plt.figure(figsize=(10, 8))

    bars = plt.barh(
        df["Department"],
        df["Complaints"]
    )

    for bar in bars:

        width = bar.get_width()

        plt.text(
            width + 20000,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width):,}",
            va="center",
            ha="left",
            fontsize=10
        )

    plt.title("311 Complaints by Department")

    plt.xlabel("Number of Complaints")

    plt.tight_layout()

    output_path = os.path.join(
        OUTPUT_DIR,
        "311_complaints_by_department.png"
    )

    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    plt.close()

    print(f"Saved: {output_path}")


def plot_311_borough_pie(input_csv: str):

    df = pd.read_csv(input_csv)

    df["Total"] = pd.to_numeric(df["Total"])

    totals = (
        df.groupby("Borough")["Total"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 7))

    plt.pie(
        totals.values,
        labels=totals.index,
        autopct="%1.0f%%",
        startangle=140
    )

    plt.title("311 Complaints in Each Borough")

    plt.tight_layout()

    output_path = os.path.join(
        OUTPUT_DIR,
        "311_borough_distribution.png"
    )

    plt.savefig(output_path, dpi=300, bbox_inches="tight")

    plt.close()

    print(f"Saved: {output_path}")


if __name__ == "__main__":

    plot_311_monthly_by_borough(
        "data/311_monthly_complaints.csv"
    )

    plot_311_department_bar()

    plot_311_borough_pie(
        "data/311_borough_counts.csv"
    )
