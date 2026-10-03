-- HIVE DDL, PARTITIONING, AND COLUMNAR FORMAT

-- 1. creating raw table (schema on read)
CREATE TABLE tb_sensor_raw (
    id_sensor INT,
    nama_area STRING,
    suhu DOUBLE,
    kelembapan DOUBLE,
    waktu_log STRING
) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE;

-- loading data from HDFS staging to Hive table
LOAD DATA INPATH '/user/hadoop/input_p4/dataset_sensor.csv' INTO TABLE tb_sensor_raw;

-- 2. creating partitioned table
CREATE TABLE tb_sensor_partitioned (
    id_sensor INT,
    suhu DOUBLE,
    kelembapan DOUBLE,
    waktu_log STRING
) 
PARTITIONED BY (nama_area STRING) 
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE;

-- enabling dynamic partitioning
SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

-- 3. inserting overwrite to partitioned table (data migration & routing)
INSERT OVERWRITE TABLE tb_sensor_partitioned PARTITION(nama_area)
SELECT id_sensor, suhu, kelembapan, waktu_log, nama_area FROM tb_sensor_raw;

-- 4. creating optimized columnar table (parquet/ORC)
CREATE TABLE tb_sensor_optimized (
    id_sensor INT,
    suhu DOUBLE,
    kelembapan DOUBLE,
    waktu_log STRING
) 
PARTITIONED BY (nama_area STRING) 
STORED AS PARQUET; -- or STORED AS ORC

-- inserting into optimized table (format conversion)
INSERT OVERWRITE TABLE tb_sensor_optimized PARTITION(nama_area)
SELECT id_sensor, suhu, kelembapan, waktu_log, nama_area FROM tb_sensor_raw;

-- 5. benchmarking / query aggregation testing
SELECT nama_area, COUNT(*) as total_log, AVG(suhu) as rata_suhu 
FROM tb_sensor_raw 
GROUP BY nama_area 
HAVING AVG(suhu) > 25;

SELECT nama_area, COUNT(*) as total_log, AVG(suhu) as rata_suhu 
FROM tb_sensor_partitioned 
WHERE nama_area = 'Surabaya'
GROUP BY nama_area;
