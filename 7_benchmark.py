# 7_benchmark.py
import os
import time
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import sys  # <-- Yeh zaroori hai

def time_pandas(filename):
    start = time.time()
    df = pd.read_csv(filename)
    summary = df.groupby("platform").agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'spend': 'sum',
        'conversions': 'sum',
        'revenue': 'sum'
    }).reset_index()
    end = time.time()
    return end - start

def time_mapreduce(filename):
    start = time.time()
    try:
        # "python" ki jagah sys.executable use kiya hai taake exact Python version chale
        subprocess.run(
            [sys.executable, "5_mapreduce_analysis.py", filename],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        return time.time() - start
    except subprocess.CalledProcessError:
        return -1  # Agar fail ho to -1 return karega

def time_spark(filename):
    start = time.time()
    try:
        subprocess.run(
            [sys.executable, "6_spark_analysis.py", filename],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        return time.time() - start
    except subprocess.CalledProcessError:
        return -1

if __name__ == "__main__":
    files = [
        "ad_data_10000.csv",
        "ad_data_100000.csv",
        "ad_data_1000000.csv",
        "ad_data_10000000.csv"
    ]

    results = []

    for f in files:
        if not os.path.exists(f):
            print(f"⚠️ Skip: {f} (file nahi mili)")
            continue

        size = int(f.replace("ad_data_", "").replace(".csv", ""))
        print(f"\n🚀 Benchmarking {size:,} records ...")

        p = time_pandas(f)
        print(f"   Pandas:    {p:.2f} sec" if p != -1 else "   Pandas: FAILED")

        m = time_mapreduce(f)
        print(f"   MapReduce: {m:.2f} sec" if m != -1 else "   MapReduce: FAILED")

        s = time_spark(f)
        print(f"   Spark:     {s:.2f} sec" if s != -1 else "   Spark: FAILED")

        results.append({
            'records': size,
            'Pandas (s)': round(p, 2) if p != -1 else "Error",
            'MapReduce (s)': round(m, 2) if m != -1 else "Error",
            'Spark (s)': round(s, 2) if s != -1 else "Error"
        })

    bench_df = pd.DataFrame(results)
    bench_df.to_csv("benchmark_results.csv", index=False)
    print("\n" + "="*70)
    print("🏆 FINAL COMPARISON TABLE")
    print("="*70)
    print(bench_df.to_string(index=False))

    # Chart (Error handling ke sath)
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(bench_df['records'], pd.to_numeric(bench_df['Pandas (s)'], errors='coerce'), marker='o', label='Pandas')
        plt.plot(bench_df['records'], pd.to_numeric(bench_df['MapReduce (s)'], errors='coerce'), marker='s', label='MapReduce')
        plt.plot(bench_df['records'], pd.to_numeric(bench_df['Spark (s)'], errors='coerce'), marker='^', label='Spark')
        plt.xlabel('Number of Records')
        plt.ylabel('Execution Time (seconds)')
        plt.title('Pandas vs MapReduce vs Spark — Execution Time Comparison')
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig('benchmark_chart.png', dpi=150)
        print("\n✅ Saved: benchmark_results.csv + benchmark_chart.png")
    except Exception as e:
        print(f"\n⚠️ Chart banane mein error aya: {e}")