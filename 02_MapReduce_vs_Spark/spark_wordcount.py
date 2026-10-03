from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col

#initializing SparkSession
spark = SparkSession.builder.appName("SparkWordCount").getOrCreate()

#1. reading dataset from HDFS
df = spark.read.text("hdfs:///user/hadoop/input_p3/dataset_pertemuan3.txt")

#2. starting transformation : splitting sentences into words, then count frequency (wordcount)
word_counts = df.select(explode(split(col("value"), " ")).alias("word")) \
    .groupBy("word") \
    .count()

#3. action : executing and showing top 20 rows
word_counts.show(20)

#caching data to RAM (memory RDD concept)
# df.cache()
# df.count() # Trigger cache to memory
