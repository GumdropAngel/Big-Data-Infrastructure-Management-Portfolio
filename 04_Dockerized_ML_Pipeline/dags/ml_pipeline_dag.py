from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

#1. defining basic DAG parameters
default_args = {
    'owner': 'lab_big_data',
    'depends_on_past': False,
    'start_date': datetime(2026, 5, 17),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'automated_ml_feature_pipeline',
    default_args=default_args,
    description='Automated Pipeline: Sqoop -> Hive -> Spark MLlib',
    schedule_interval=None, #executed manually via trigger
    catchup=False,
)

#2. defining task 1 : data ingestion via Sqoop (targeting Sqoop container)
task_sqoop_ingest = BashOperator(
    task_id='sqoop_ingest_from_mysql',
    bash_command='''
docker exec sqoop sqoop import \
--connect "jdbc:mysql://mysql-db:3306/retail_db?useSSL=false" \
--username retail_user \
--password retail_pass \
--table transactions \
--target-dir /user/hadoop/raw_transactions \
--delete-target-dir \
--m 1
    ''',
    dag=dag,
)

#3. defining task 2 : schema / partition update via Hive (targeting Hive container)
#note : MSCK REPAIR TABLE command is used to register new structures/partitions
task_hive_staging = BashOperator(
    task_id='hive_metadata_staging',
    bash_command='''
docker exec hive-server hive -e "MSCK REPAIR TABLE ext_transactions;"
    ''',
    dag=dag,
)

#4. defining task 3 : feature engineering execution via Spark (targeting Spark container)
task_spark_feature_eng = BashOperator(
    task_id='spark_mllib_feature_engineering',
    bash_command='''
docker exec spark-master /opt/spark/bin/spark-submit \
--master spark://spark-master:7077 \
/opt/spark/ml_feature_pipeline.py
    ''',
    dag=dag,
)

#5. determining data flow execution sequence (dependency pipeline)
task_sqoop_ingest >> task_hive_staging >> task_spark_feature_eng
