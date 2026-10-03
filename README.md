# Big Data Infrastructure & Management Portfolio

This repository contains my projects and practical implementations from the **Big Data Infrastructure and Management** course (or "Infrastruktur dan Manajemen Big Data" in Indonesian) taken during my 4th semester of college. It showcases a progression from basic Hadoop cluster setup to building a fully automated, dockerized Machine Learning Feature Pipeline using modern Data Engineering tools.

##  Technologies Used
- **Hadoop Ecosystem:** HDFS, YARN, MapReduce
- **Processing Engines:** Apache Spark (PySpark, MLlib), Hive
- **Data Ingestion:** Apache Sqoop, MySQL
- **Orchestration:** Apache Airflow
- **Containerization:** Docker & Docker Compose, LXC (Linux Containers)
- **Data Visualization:** Pandas, Matplotlib

##  Dataset Information
Unlike traditional data science projects that rely on static CSV files, the primary dataset for the automated ML pipeline is **synthetically generated**. 

Using the `forge_data.py` script, we simulated a live operational database (MySQL) by generating 100,000 rows of e-commerce transaction data. To test the robustness of our data cleansing pipeline, we deliberately injected 15% `Null` values into critical numerical columns, forcing our PySpark engine to handle real-world "dirty data" scenarios via median imputation.

##  Project Structure

### 1. `01_Hadoop_HDFS_YARN`
- **Goal:** Set up a foundational Big Data cluster.
- **Details:** Configured a Hadoop Mini Cluster using LXC (Linux Containers) with 1 NameNode and 2 DataNodes. Managed HDFS directories, user permissions, and performed YARN resource tuning and stress testing (Simulating Out of Memory and Race Conditions).

### 2. `02_MapReduce_vs_Spark`
- **Goal:** Compare processing engines.
- **Details:** Developed a WordCount program to benchmark the execution speed and resource consumption between traditional disk-based **MapReduce** and modern in-memory **Apache Spark**.

### 3. `03_Data_Warehouse_Hive`
- **Goal:** Implement Data Warehousing solutions.
- **Details:** Managed large datasets using **Apache Hive**. Implemented Data Definition Language (DDL), dynamic partitioning, and converted data into optimized columnar storage formats (**Parquet** & **ORC**) to significantly improve query performance.

### 4. `04_Dockerized_ML_Pipeline`
- **Goal:** Build an automated end-to-end Machine Learning data pipeline.
- **Details:** Orchestrated a complete data workflow using **Apache Airflow**:
  - Extracted operational data from **MySQL** using **Apache Sqoop**.
  - Loaded data into **HDFS** and staged it via **Hive**.
  - Processed and cleaned data using **PySpark MLlib** (Handling Nulls, StringIndexer, VectorAssembler, and Feature Scaling).

### 5. `05_Data_Storytelling_Dashboard`
- **Goal:** Transform data into actionable business insights.
- **Details:** Bridged the gap between technical metrics and business decisions by creating an Executive Dashboard. Used **Pandas** and **Matplotlib** inside PySpark to generate High Data-Ink Ratio charts for stakeholders.

---
*This repository serves as a reproducible codebase for Big Data Engineering practices.*
