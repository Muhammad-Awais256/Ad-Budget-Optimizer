# Project 2 — Digital Advertising Budget Optimizer

# Project 2 — Digital Advertising Budget Optimizer

## 📌 Problem Statement
A company spends money on 5 digital platforms (Facebook, Instagram, Google, TikTok, YouTube). Management asks: **"Where should we spend the next Rs. 1 million?"**

This project analyzes historical ad performance to calculate metrics (CTR, CPC, CPA, CVR, ROAS) and recommends the optimal budget allocation. It also simulates a Big Data environment (10K to 10M records) to compare the performance of Pandas vs MapReduce vs Spark.

## 📁 Project Files
- `1_data_generator.py` : Generates synthetic advertising data.
- `2_data_analysis.py` : Calculates metrics using Pandas.
- `3_budget_optimizer.py` : Recommends budget based on ROAS/CPA (with 5%-40% constraints).
- `4_dashboard.py` : Tkinter GUI to visualize results.
- `5_mapreduce_analysis.py` : MapReduce (mrjob) implementation of the metrics.
- `6_spark_analysis.py` : PySpark implementation of the metrics.
- `7_benchmark.py` : Compares Pandas, MapReduce, and Spark execution times.
- `benchmark_chart.png` : Visual chart comparing execution times.
- `optimized_budget.csv` : Final budget recommendations.

## 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Generate data: `python 1_data_generator.py 1000000`
3. Run analysis: `python 2_data_analysis.py`
4. Get budget recommendations: `python 3_budget_optimizer.py`
5. Run GUI Dashboard: `python 4_dashboard.py`
6. To run the benchmark: `python 7_benchmark.py`

## 📊 Big Data Comparison Results (Local Windows Machine)

| Records | Pandas (Time) | MapReduce (mrjob) | Spark (PySpark) |
| :--- | :--- | :--- | :--- |
| 10,000 | 0.05 sec | 1.76 sec | 20.47 sec |
| 100,000 | 0.18 sec | 0.94 sec | 16.94 sec |
| 1,000,000 | 1.40 sec | 1.01 sec | 21.91 sec |
| 10,000,000 | 12.44 sec | 1.20 sec | 40.96 sec |

### 💡 Key Observations:
- **Pandas** is very fast for small datasets but slows down significantly as data grows to 10M records due to memory limitations.
- **MapReduce** shows remarkably stable execution times, scaling well even on a single machine for aggregation tasks.
- **Spark** has a high startup overhead (JVM initialization) locally, but its in-memory processing makes it the industry standard for massive clusters.

## 💰 Budget Recommendation Output (Rs. 1,000,000 Target)
Based on the historical performance (ROAS & CPA), the optimized budget allocation is:

- **Google:** Rs. 248,100 (24.8%) - *Best platform with 3.22x ROAS*
- **Facebook:** Rs. 233,700 (23.4%) - *Lowest CPA at Rs. 815*
- **Instagram:** Rs. 211,700 (21.2%)
- **YouTube:** Rs. 163,100 (16.3%)
- **TikTok:** Rs. 143,300 (14.3%)

**💡 Business Insight:** The engine recommends allocating the highest budget to Google due to its superior ROAS, while maintaining a minimum 14%+ allocation across all platforms to ensure brand visibility.