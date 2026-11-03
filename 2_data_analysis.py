import pandas as pd
import time
import os

print("="*60)
print("📊 ANALYZING ADVERTISING DATA (Pandas)")
print("="*60)

# File name dhoondein (automatically latest wali utha lega)
csv_files = [f for f in os.listdir() if f.startswith('ad_data_') and f.endswith('.csv')]
latest_file = max(csv_files, key=os.path.getctime)

print(f"📂 Loading: {latest_file}")
start_time = time.time()

# Data load karein
df = pd.read_csv(latest_file)

# ============================================================
# CALCULATE METRICS
# ============================================================
print("⚙️ Calculating Metrics...")

# 1. CTR (Click Through Rate) = (Clicks / Impressions) * 100
df['CTR (%)'] = (df['clicks'] / df['impressions']) * 100

# 2. CPC (Cost Per Click) = Spend / Clicks
# Agar clicks 0 hain toh divide by zero error na aaye, isliye np.where use karenge
import numpy as np
df['CPC (Rs)'] = np.where(df['clicks'] > 0, df['spend'] / df['clicks'], 0)

# 3. CPA (Cost Per Acquisition) = Spend / Conversions
df['CPA (Rs)'] = np.where(df['conversions'] > 0, df['spend'] / df['conversions'], 0)

# 4. Conversion Rate (CVR) = (Conversions / Clicks) * 100
df['CVR (%)'] = np.where(df['clicks'] > 0, (df['conversions'] / df['clicks']) * 100, 0)

# 5. ROAS (Return on Ad Spend) = Revenue / Spend
df['ROAS'] = np.where(df['spend'] > 0, df['revenue'] / df['spend'], 0)

# ============================================================
# PLATFORM WISE SUMMARY
# ============================================================
print("\n" + "="*60)
print("📈 PLATFORM PERFORMANCE SUMMARY")
print("="*60)

platform_summary = df.groupby('platform').agg({
    'impressions': 'sum',
    'clicks': 'sum',
    'spend': 'sum',
    'conversions': 'sum',
    'revenue': 'sum'
}).reset_index()

# Summary ke metrics
platform_summary['CTR (%)'] = (platform_summary['clicks'] / platform_summary['impressions']) * 100
platform_summary['CPC (Rs)'] = platform_summary['spend'] / platform_summary['clicks']
platform_summary['CPA (Rs)'] = platform_summary['spend'] / platform_summary['conversions']
platform_summary['CVR (%)'] = (platform_summary['conversions'] / platform_summary['clicks']) * 100
platform_summary['ROAS'] = platform_summary['revenue'] / platform_summary['spend']

# Round karein
platform_summary = platform_summary.round(2)

print(platform_summary.to_string(index=False))

# Summary save karein
platform_summary.to_csv('platform_summary.csv', index=False)
print("\n✅ Saved: platform_summary.csv")

# ============================================================
# TIME TAKEN
# ============================================================
end_time = time.time()
print("\n" + "="*60)
print(f"⏱️ PANDAS EXECUTION TIME: {end_time - start_time:.2f} seconds")
print("="*60)
print("(Yeh time note kar lein, MapReduce/Spark se compare karne ke liye)")