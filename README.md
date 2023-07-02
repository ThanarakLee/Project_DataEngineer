# Data Engineer Project

This project demonstrates the workflow of a Data Engineer. It utilizes the Google Cloud Platform and Google Colab as the main tools.

## Table of Contents
* Data Collection with Python & Pandas
* Data Cleansing with Spark
* Upload files to Data Lake
* Automated Data Pipeline with Airflow
* Big Data Warehouse with Google BigQuery
* Report & Dashboard with Google Data Studio

## Data Collection with Python & Pandas
Data collection is performed using Python, where data is gathered from databases and REST APIs.

### Input:
- Reading data from MySQL
- Reading data from REST API using the Requests package

### Output:
- Consolidated dataset (CSV)

## Data Cleansing with Spark
Data cleansing aims to ensure data cleanliness and usability. In this workshop, PySpark, Spark, and Pandas are used to enhance data quality.

### Input:
- Previously gathered data (CSV)
- Notebook supporting PySpark, Spark, and Pandas (e.g., Google Colab)

### Output:
- Cleaned data (CSV)

## Upload files to Data Lake
This section covers uploading files to a Data Lake using the Google Cloud Platform. Specifically, files are uploaded to Google Cloud Storage.

## Automated Data Pipeline with Airflow
Create a data pipeline in Airflow to automate data extraction. Google Cloud Composer is used for this purpose.

## Big Data Warehouse with Google BigQuery
Use Apache Airflow to load data into BigQuery automatically.

## Report & Dashboard with Google Data Studio
Create a dashboard that retrieves data from BigQuery for reporting purposes. View the [Sarah Gift World Dashboard](https://datastudio.google.com/embed/u/0/reporting/6805ef50-0d56-4531-9cc3-7ec34a8843ea/page/O2KNC) as an example.

## Summary
This project involves creating a pipeline to extract data from databases and APIs, storing it in a Data Lake, and then loading it into a Data Warehouse. The process is automated, and the data can be visualized for analysis.