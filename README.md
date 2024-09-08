# Weather-Data-ETL-Pipeline

![Weather ETL Pipeline Architecture](https://github.com/desininja/Weather-Data-ETL-Pipeline/blob/main/Project%20Snapshots/Weather%20ETL%20Pipeline%20Architecture.png)

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [ETL Process](#etl-process)
- [Technologies Used](#technologies-used)
- [Repository Structure](#repository-structure)
- [DAG Details](#dag-details)
- [Glue Script Details](#glue-script-details)
- [CICD Pipeline](#cicd-pipeline)
- [How to Run](#how-to-run)
- [Future Enhancements](#future-enhancements)

## Overview

This repository contains a project that demonstrates an ETL (Extract, Transform, Load) pipeline using AWS services. The pipeline retrieves weather forecast data from the OpenWeather API, stores it in an S3 bucket, transforms it using AWS Glue, and loads the processed data into an Amazon Redshift table for further analysis. 

The entire orchestration of the pipeline is managed using Amazon Managed Workflows for Apache Airflow (MWAA). This project showcases how AWS services can be integrated to build a scalable, reliable, and automated ETL pipeline.

## Architecture

The architecture of the ETL pipeline is depicted in the diagram above. It involves the following AWS components:

1. **Amazon MWAA (Managed Workflows for Apache Airflow):** Used to orchestrate the entire ETL process by triggering and managing the data pipeline tasks.
2. **Amazon S3:** Serves as the data lake, storing the raw weather data fetched from the OpenWeather API.
3. **AWS Glue:** Used for data transformation. The Glue job reads the data from S3, performs necessary transformations, and writes the processed data to Amazon Redshift.
4. **Amazon Redshift:** A data warehouse that stores the transformed data for analysis and reporting.
5. **AWS CodeBuild:** Manages the CI/CD pipeline for deploying DAGs and scripts.

## ETL Process

1. **Extraction:** An Airflow DAG (`openweather_api_dag`) calls the OpenWeather API to fetch weather forecast data for a specified location (Toronto, Canada). The extracted data is normalized into a tabular format using Pandas and then stored as a CSV file in an S3 bucket.

2. **Loading to S3:** The transformed data is uploaded to an S3 bucket (`weather-data-landing-zone-zn`) using `S3CreateObjectOperator`.

3. **Triggering Glue Job:** Once the data is available in S3, another Airflow DAG (`transform_redshift_dag`) is triggered using the `TriggerDagRunOperator`. This DAG triggers an AWS Glue job that reads the raw data from S3, performs data transformation, and loads the data into an Amazon Redshift table (`public.weather_data`).

4. **Transformation and Loading to Redshift:** The AWS Glue job performs schema mapping and transformation on the weather data, making it ready for analysis. The transformed data is then loaded into Amazon Redshift for further querying and analysis.

## Technologies Used

- **AWS MWAA (Managed Workflows for Apache Airflow)**
- **Amazon S3**
- **AWS Glue**
- **Amazon Redshift**
- **AWS CodeBuild**
- **Python (Airflow DAGs, Glue ETL Script)**
- **Pandas (Data Manipulation)**
- **OpenWeather API (Data Source)**

## Repository Structure

```plaintext
Weather-Data-ETL-Pipeline/
│
├── Project Snapshots/
│   ├── airflow_dags.png
│   ├── redshift_result.png
│   └── Weather ETL Pipeline Architecture.png
│
├── dags/
│   ├── transform_redshift_load.py
│   └── weather_api.py
│
├── scripts/
│   └── weather_data_ingestion.py
│
├── buildspec.yml
│
└── requirements.txt
```

### Description

1. **Project Snapshots:** Contains snapshots of Airflow DAGs, Redshift results, and the architecture diagram.
2. **dags:** Contains the Airflow DAGs for fetching data from the OpenWeather API and triggering Glue jobs.
3. **scripts:** Contains the Glue ETL script (`weather_data_ingestion.py`) used for data transformation.
4. **buildspec.yml:** Configuration file for CI/CD using AWS CodeBuild. It places the DAGs and requirements.txt in their respective locations.
5. **requirements.txt:** Lists the Python dependencies (e.g., Pandas, Requests) required for the Airflow DAGs.

## DAG Details

### `transform_redshift_load.py`

This DAG handles the transformation of data and its loading into Amazon Redshift. The DAG uses `GlueJobOperator` to start a Glue job that processes the data. 

Key components:

- **GlueJobOperator:** Runs the Glue job `glue_transform_task`.
- **ExternalTaskSensor:** Ensures the DAG waits for the completion of the previous DAG (`openweather_api_dag`).

### `weather_api.py`

This DAG is responsible for extracting weather data from the OpenWeather API and storing it in S3.

Key components:

- **PythonOperator:** Fetches data from the OpenWeather API and processes it using Pandas.
- **S3CreateObjectOperator:** Stores the processed data in an S3 bucket.
- **TriggerDagRunOperator:** Triggers the `transform_redshift_dag` once data is loaded into S3.

## Glue Script Details

The Glue script (`weather_data_ingestion.py`) reads the raw weather data from S3, transforms it by applying schema mappings, and loads the processed data into Amazon Redshift. The script uses the AWS Glue library for ETL processes such as data extraction, transformation, and loading.

Key components:

- **DynamicFrame Creation:** Reads the data from S3 as a DynamicFrame.
- **Schema Transformation:** Applies a schema to the data.
- **Data Load to Redshift:** Loads the transformed data into a Redshift table (`public.weather_data`).

## CICD Pipeline

The CI/CD pipeline is managed by AWS CodeBuild. The `buildspec.yml` file contains the build and deploy steps, which automate the placement of DAGs and scripts into their respective Airflow and Glue locations.

## How to Run

1. **Set Up AWS Environment:**
   - Create S3 buckets, Glue jobs, and Redshift clusters as specified.
   - Ensure that the necessary IAM roles and permissions are in place.

2. **Deploy Airflow DAGs:**
   - Use AWS CodeBuild and `buildspec.yml` for automatic deployment.
   
3. **Install Requirements:**
   - Install dependencies listed in `requirements.txt` in the MWAA environment.

4. **Run the DAGs:**
   - Trigger the `openweather_api_dag` manually or set it to run on a schedule.
   - The DAG will automatically trigger the `transform_redshift_dag` after loading the data to S3.

5. **Monitor the Pipeline:**
   - Use Airflow UI, AWS Glue Console, and Redshift Console to monitor each stage of the ETL pipeline.

## Future Enhancements

- **Error Handling and Logging:** Improve error handling and logging mechanisms in Airflow and Glue jobs.
- **Data Validation:** Implement data validation steps to ensure data quality before loading into Redshift.
- **Automated Alerts:** Add monitoring and alerting for data pipeline failures or anomalies.
- **Expand Data Sources:** Integrate additional data sources to enrich the analysis.

---

This README provides a comprehensive guide to your repository, covering the objectives, architecture, implementation details, and future enhancements of your ETL pipeline project. Feel free to customize it further based on your specific needs!
