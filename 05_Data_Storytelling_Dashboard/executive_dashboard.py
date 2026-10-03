import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession

#1. initializing Spark & extracting raw data (EDA format) from Hive
spark = SparkSession.builder.appName("ExecutiveDashboard").config("hive.metastore.uris", "thrift://hive-server:9083").enableHiveSupport().getOrCreate()

print("Extracting raw data from Hive for EDA purposes...")
#extracting data with contextual meaning (city, monthly_income, clicked_ad)
df_hive = spark.sql("SELECT city, monthly_income, clicked_ad FROM ext_transactions WHERE city != 'Unknown'")

#converting distributed DataFrame (Spark) to local DataFrame (pandas) for visualization
df = df_hive.toPandas()

#chart 1 : bar chart (demographic evaluation)
plt.figure(figsize=(10, 6))

#aggregating average income per city (in million Rupiah)
income_by_city = df.groupby('city')['monthly_income'].mean().sort_values(ascending=False) / 1000000

bars = plt.bar(income_by_city.index, income_by_city.values, color='#2980b9')

#principle 2 : high data-ink ratio (remove top and right borders)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

#principle 1 : declarative title (directly point to the conclusion)
plt.title("Jakarta Leads: Highest Average User Income (In Million Rp)", fontsize=14, fontweight='bold', loc='left', pad=20)
plt.ylabel("Million Rupiah")

plt.savefig('/opt/spark/demografi_bar.png', bbox_inches='tight', dpi=300)
plt.close()

#chart 2 : pie chart (campaign evaluation)
plt.figure(figsize=(8, 8))

clicked_counts = df['clicked_ad'].value_counts()
labels = ['Did Not Click Campaign (0)', 'Clicked Campaign (1)']
colors = ['#e74c3c', '#2ecc71'] #red for negative, green for positive

plt.pie(clicked_counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.1, 0))

#principle 1 : declarative title 
plt.title("Evaluation: Ad Campaign Runs Slow, Fails to Attract Majority Users", fontsize=14, fontweight='bold', pad=20)

plt.savefig('/opt/spark/konversi_pie.png', bbox_inches='tight', dpi=300)
plt.close()

print("Execution Complete: 2 Dashboard Files successfully generated in /opt/spark/")
