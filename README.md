# NYC 311 & NYPD Big Data Analysis

## Project Overview

This project analyzes urban issues and public safety in New York City by integrating NYC 311 service requests and NYPD crime data. The goal is to explore spatial and temporal patterns and investigate potential relationships between complaint activity and crime trends.

## Data Sources

NYC 311 Service Requests
https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9/about_data

NYPD Complaint Data
https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/5uac-w243/about_data

Due to the large size of the datasets, raw data is not included in this repository.

## Technologies Used

* Hadoop / HDFS
* Hive (SQL-based distributed processing)
* Python (Pandas, NumPy)
* Scikit-learn / PyTorch
* Jupyter Notebook

## Data Processing Pipeline

The project follows a multi-stage data processing workflow:

1. Extract 2025 records from raw datasets
2. Perform data cleaning and standardization
3. Aggregate data at the precinct-week level
4. Convert long-format data into pivot tables
5. Merge 311 and NYPD datasets for modeling

## Analysis

The analysis focuses on:

* Spatial distribution (borough and precinct level)
* Temporal patterns (monthly and weekly trends)
* Complaint type distribution
* Crime category distribution
* Hotspot identification

All analysis results and visualizations are presented in the final report.

## Machine Learning

Multiple machine learning models were implemented and compared:

* Random Forest
* Multi-Layer Perceptron (MLP)
* Support Vector Machine (SVM)
* Convolutional Neural Network (CNN)

Model selection is based on comparative performance across evaluation metrics. Detailed results are included in the report.

## Project Structure

```
├── data/                # Data source description (no raw data)
├── hive/                # Hive SQL queries
├── scripts/             # Data preprocessing scripts
├── notebooks/           # Machine learning models
├── report/              # Final project report
```

## How to Run

1. Download datasets from the provided links
2. Run preprocessing scripts:

```
python scripts/extract_311_2025.py
python scripts/pivot_precinct_week.py
python scripts/merge_precinct_week.py
```

3. Execute Hive queries in the hive directory
4. Run the notebook in notebooks for machine learning

## Report

All analysis results and model evaluations are documented in:

```
report/Final_Project_Report.pdf
```

## Notes

* Raw datasets are excluded due to size constraints
* Some notebooks may not render on GitHub; please download and open locally
