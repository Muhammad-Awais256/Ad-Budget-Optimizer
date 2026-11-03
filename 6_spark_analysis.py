# 6_spark_analysis.py
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import time

# ==========================================================
# ⚠️ SAB SE ZAROORI SETTINGS (VS CODE KE LIYE)
# ==========================================================
# Aap ke PC mein Java yahan install hai:
os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot"
# Hadoop ka path (Agar aapne winutils setup ki hai to):
os.environ["HADOOP_HOME"] = r"C:\hadoop"
# PySpark ko force karein ke aapka Python use kare
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
# ==========================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, round as _round

def main(filename):
    start = time.time()

    spark = SparkSession.builder \
        .appName("AdMetricsSpark") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # CSV load
    df = spark.read.csv(filename, header=True, inferSchema=True)

    # Platform-wise aggregation
    result = df.groupBy("platform").agg(
        _sum("impressions").alias("impressions"),
        _sum("clicks").alias("clicks"),
        _sum("spend").alias("spend"),
        _sum("conversions").alias("conversions"),
        _sum("revenue").alias("revenue")
    )

    # Metrics
    result = result \
        .withColumn("CTR",  _round((col("clicks") / col("impressions")) * 100, 2)) \
        .withColumn("CPC",  _round(col("spend") / col("clicks"), 2)) \
        .withColumn("CPA",  _round(col("spend") / col("conversions"), 2)) \
        .withColumn("CVR",  _round((col("conversions") / col("clicks")) * 100, 2)) \
        .withColumn("ROAS", _round(col("revenue") / col("spend"), 2))

    print("\n" + "="*80)
    print(f"📊 SPARK PLATFORM PERFORMANCE SUMMARY — {filename}")
    print("="*80)
    result.show(truncate=False)

    # Save
    result.toPandas().to_csv("spark_summary.csv", index=False)
    print("✅ Saved: spark_summary.csv")

    end = time.time()
    print("\n" + "="*60)
    print(f"⏱️ SPARK EXECUTION TIME: {end - start:.2f} seconds")
    print("="*60)

    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python 6_spark_analysis.py <csv_file>")
        sys.exit(1)
    main(sys.argv[1])