# 3_budget_optimizer.py (UPDATED)
import pandas as pd
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*60)
print("💰 BUDGET RECOMMENDATION ENGINE")
print("="*60)

try:
    df = pd.read_csv('platform_summary.csv')
except FileNotFoundError:
    print("❌ Error: Pehle '2_data_analysis.py' chalayein!")
    exit()

NEW_BUDGET = 1_000_000
print(f"\n🎯 Target Budget: Rs. {NEW_BUDGET:,}")

# ---- Scoring ----
# Score = ROAS / CPA  (zyada ROAS achha, kam CPA achha)
# Agar CPA 0 hai to usko chhota epsilon dein (0 se divide na ho)
df['CPA_safe'] = df['CPA (Rs)'].apply(lambda x: x if x > 0 else 0.01)
df['Score'] = df['ROAS'] / df['CPA_safe']

# Normalize to percentages
df['Raw %'] = (df['Score'] / df['Score'].sum()) * 100

# ---- Constraints: Min 5% aur Max 40% per platform ----
MIN_PCT = 5.0
MAX_PCT = 40.0

# Step 1: Sab ko min 5% do
df['Recommended Allocation (%)'] = df['Raw %'].clip(lower=MIN_PCT)

# Step 2: Kisi ko 40% se zyada na do
df['Recommended Allocation (%)'] = df['Recommended Allocation (%)'].clip(upper=MAX_PCT)

# Step 3: Total ko 100% par normalize karein (iteratively)
for _ in range(20):
    total = df['Recommended Allocation (%)'].sum()
    if abs(total - 100) < 0.1:
        break
    # Jinko max/min hit ho chuka hai unko fix rakhein, baqi ko scale karein
    free = df[(df['Recommended Allocation (%)'] > MIN_PCT) &
              (df['Recommended Allocation (%)'] < MAX_PCT)]
    if len(free) == 0:
        break
    df.loc[free.index, 'Recommended Allocation (%)'] *= (100 / total)

df['Recommended Allocation (%)'] = df['Recommended Allocation (%)'].round(2)
df['Recommended Budget (Rs)'] = (df['Recommended Allocation (%)'] / 100 * NEW_BUDGET).round(0)

df = df.sort_values('Recommended Budget (Rs)', ascending=False)

print("\n" + "="*85)
print("🏆 OPTIMIZED BUDGET ALLOCATION (5%–40% constraints ke saath)")
print("="*85)
print(f"{'Platform':<12} | {'ROAS':<8} | {'CPA':<10} | {'Alloc %':<9} | {'Budget (Rs)':<15}")
print("-" * 85)
for _, row in df.iterrows():
    print(f"{row['platform']:<12} | {row['ROAS']:<8.2f} | "
          f"{row['CPA (Rs)']:<10.2f} | {row['Recommended Allocation (%)']:<8.1f}% | "
          f"Rs. {row['Recommended Budget (Rs)']:,.0f}")
print("-" * 85)
print(f"{'TOTAL':<12} | {'':<8} | {'':<10} | {'100.0%':<9} | Rs. {df['Recommended Budget (Rs)'].sum():,.0f}")

df.to_csv('optimized_budget.csv', index=False)
print("\n✅ Saved: optimized_budget.csv")

best = df.iloc[0]
print(f"\n💡 Best platform: {best['platform']} (ROAS {best['ROAS']:.2f}x, "
      f"allocation {best['Recommended Allocation (%)']:.1f}%)")