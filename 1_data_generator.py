import pandas as pd
import sys
import numpy as np
import random
from datetime import datetime, timedelta

print("="*60)
print("📊 GENERATING DIGITAL ADVERTISING DATA")
print("="*60)

NUM_RECORDS = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000

platforms = ['Facebook', 'Instagram', 'Google', 'TikTok', 'YouTube']
campaigns = ['Summer_Sale', 'Winter_Sale', 'New_Launch', 'Brand_Awareness', 'Retargeting']
genders = ['Male', 'Female', 'Other']
cities = ['Karachi', 'Lahore', 'Islamabad', 'Rawalpindi', 'Faisalabad']
devices = ['Mobile', 'Desktop', 'Tablet']

print(f"⏳ Generating {NUM_RECORDS} records... (Thoda waqt lagega)")

# Base start date
start_date = datetime(2026, 1, 1)

data = []

for i in range(NUM_RECORDS):
    platform = random.choice(platforms)
    campaign = random.choice(campaigns)
    
    # Platform ke hisaab se realistic data generate karein
    if platform == 'Google':
        impressions = random.randint(1000, 50000)
        ctr = random.uniform(0.02, 0.08) # 2% - 8%
        cpc = random.uniform(20, 60) # Rs. 20 - 60
        cvr = random.uniform(0.02, 0.06) # 2% - 6%
        aov = random.uniform(1500, 5000) # Average Order Value
    elif platform == 'Facebook':
        impressions = random.randint(5000, 100000)
        ctr = random.uniform(0.01, 0.03)
        cpc = random.uniform(10, 30)
        cvr = random.uniform(0.01, 0.04)
        aov = random.uniform(1000, 3000)
    elif platform == 'Instagram':
        impressions = random.randint(5000, 80000)
        ctr = random.uniform(0.015, 0.04)
        cpc = random.uniform(15, 40)
        cvr = random.uniform(0.015, 0.045)
        aov = random.uniform(1200, 3500)
    elif platform == 'TikTok':
        impressions = random.randint(10000, 200000)
        ctr = random.uniform(0.005, 0.02)
        cpc = random.uniform(5, 15)
        cvr = random.uniform(0.005, 0.02)
        aov = random.uniform(500, 2000)
    else: # YouTube
        impressions = random.randint(10000, 150000)
        ctr = random.uniform(0.008, 0.025)
        cpc = random.uniform(8, 25)
        cvr = random.uniform(0.008, 0.03)
        aov = random.uniform(800, 2500)

    # Calculations based on rates
    clicks = int(impressions * ctr)
    spend = round(clicks * cpc, 2)
    conversions = int(clicks * cvr)
    revenue = round(conversions * aov, 2)
    
    # Random date
    random_date = start_date + timedelta(days=random.randint(0, 365))
    
    data.append([
        random_date.strftime("%Y-%m-%d"),
        campaign,
        platform,
        impressions,
        clicks,
        spend,
        conversions,
        revenue,
        random.randint(18, 65), # age
        random.choice(genders),
        random.choice(cities),
        random.choice(devices)
    ])

# DataFrame banayein
columns = ['date', 'campaign', 'platform', 'impressions', 'clicks', 'spend', 'conversions', 'revenue', 'age', 'gender', 'city', 'device']
df = pd.DataFrame(data, columns=columns)

# CSV mein save karein
filename = f"ad_data_{NUM_RECORDS}.csv"
df.to_csv(filename, index=False)

print("\n" + "="*60)
print(f"✅ DATA SAVED: {filename}")
print(f"Total Records: {len(df)}")
print("="*60)
print("\nFIRST 5 RECORDS:")
print(df.head())