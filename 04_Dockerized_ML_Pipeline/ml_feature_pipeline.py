import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import Imputer
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.feature import StandardScaler #StandardScaler for ODD groups

#initializing Spark with Hive metastore support
spark = SparkSession.builder \
    .appName("ML_Feature_Engineering_Pipeline") \
    .master("spark://spark-master:7077") \
    .config("hive.metastore.uris", "thrift://hive-server:9083") \
    .enableHiveSupport() \
    .getOrCreate()

#reading data directly from Hive data warehouse
print("=== Step 2.1: Reading data from Apache Hive ===")
start_read = time.time()
df_hive = spark.sql("SELECT * FROM ext_transactions")
df_hive.cache() #locking data in memory for experimental purposes
print(f"Number of rows loaded: {df_hive.count()}")
print(f"Hive read duration: {time.time() - start_read:.4f} seconds\n")

print("=== Step 2.2: Data Cleansing Process (Imputation) ===")
#1. imputing null values in numeric columns using median strategy
imputer = Imputer(
    inputCols=["age", "monthly_income"],
    outputCols=["age_imputed", "income_imputed"]
).setStrategy("median")

df_imputed = imputer.fit(df_hive).transform(df_hive)

#2. filling null values in categorical column (city) with 'Unknown' label
df_clean = df_imputed.fillna({"city": "Unknown"})

print("=== Step 2.3: Text to Vector Feature Transformation ===")
#1. converting categorical text (city) to numeric index
indexer = StringIndexer(inputCol="city", outputCol="city_index", handleInvalid="keep")
df_indexed = indexer.fit(df_clean).transform(df_clean)

#2. assemble all independent features into a single vector column named 'raw_features'
assembler = VectorAssembler(
    inputCols=["city_index", "age_imputed", "income_imputed"],
    outputCol="raw_features"
)
df_assembled = assembler.transform(df_indexed)

print("=== Step 2.4: Execute StandardScaler (Odd Group) ===")
start_scale = time.time()
scaler = StandardScaler(inputCol="raw_features", outputCol="final_features", withStd=True, withMean=False)
df_scaled = scaler.fit(df_assembled).transform(df_assembled)
print(f"SCALER_EXECUTION_DURATION: {time.time() - start_scale:.4f} seconds\n")

print("=== Step 2.5: Save Final Results to HDFS (Parquet Format) ===")
#selecting essential columns and save to HDFS
final_data = df_scaled.select("final_features", "clicked_ad")
final_data.write.mode("overwrite").parquet("hdfs://namenode:8020/user/hadoop/preprocessed_ml_data")

print("Export Process Successful! Data pipeline executed completely.")
