#!/bin/bash
#executing Mapreduce wordcount using Hadoop CLI

#1. creating input directory and upload dataset to HDFS
hdfs dfs -mkdir -p /user/hadoop/input_p3
hdfs dfs -put dataset_pertemuan3.txt /user/hadoop/input_p3/

#2. executing Mapreduce wordcount engine
hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/hadoop/input_p3/dataset_pertemuan3.txt /user/hadoop/output_p3_hasil

#3. validating output
hdfs dfs -ls /user/hadoop/output_p3_hasil
hdfs dfs -cat /user/hadoop/output_p3_hasil/part-r-00000 | head -n 20
