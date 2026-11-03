import pandas as pd

print("="*60)
print("💰 BUDGET RECOMMENDATION ENGINE")
print("="*60)

# Load summary
try:
    df = pd.read_csv('platform_summary.csv')
except FileNotFoundError:
    print("❌ Error: Pehle '2_data_analysis.py' chalayein!")
    exit()

# Maan lijiye company ka naya budget 1 Million (1,000,000) hai
NEW_BUDGET = 1000000 

print(f"\n🎯 Target Budget to Allocate: Rs. {NEW_BUDGET:,}")

# ============================================================
# LOGIC: Kis platform par kitna paisa lagayein?
# ============================================================
# Hum ROAS aur CPA dekh kar decide karenge.
# High ROAS = Zyada paisa do. High CPA = Kam paisa do.

# Hum ek simple "Score" nikaalenge: (ROAS / CPA)
# Jiska score zyada, usay zyada budget milega.
df['Score'] = df['ROAS'] / df['CPA (Rs)']

# Score ke hisaab se % nikaalein
total_score = df['Score'].sum()
df['Recommended Allocation (%)'] = (df['Score'] / total_score) * 100

# Actual rupees mein budget
df['Recommended Budget (Rs)'] = (df['Recommended Allocation (%)'] / 100) * NEW_BUDGET

# Sort karein (Highest allocation sabse upar)
df = df.sort_values(by='Recommended Budget (Rs)', ascending=False)

# ============================================================
# PRINT RESULTS
# ============================================================
print("\n" + "="*70)
print("🏆 OPTIMIZED BUDGET ALLOCATION")
print("="*70)

print(f"{'Platform':<12} | {'Current ROAS':<12} | {'Current CPA':<12} | {'Allocation %':<12} | {'New Budget (Rs)':<15}")
print("-" * 75)

for index, row in df.iterrows():
    print(f"{row['platform']:<12} | {row['ROAS']:<12.2f} | {row['CPA (Rs)']:<12.2f} | {row['Recommended Allocation (%)']:<11.1f}% | Rs. {row['Recommended Budget (Rs)']:,.0f}")

print("-" * 75)
print(f"TOTAL BUDGET ALLOCATED: Rs. {df['Recommended Budget (Rs)'].sum():,.0f}")

# Save results
df.to_csv('optimized_budget.csv', index=False)
print("\n✅ Saved: optimized_budget.csv")

# ============================================================
# INSIGHTS
# ============================================================
best_platform = df.iloc[0]
print("\n💡 BUSINESS INSIGHT:")
print(f"Sabse behtar platform '{best_platform['platform']}' hai kyunke iska ROAS {best_platform['ROAS']:.2f}x hai.")
print(f"Aapko apne agle Rs. 1 Million ka {best_platform['Recommended Allocation (%)']:.1f}% is platform par lagana chahiye!")