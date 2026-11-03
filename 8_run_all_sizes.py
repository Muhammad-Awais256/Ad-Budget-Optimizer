# 8_run_all_sizes.py
import subprocess
import sys

# 1_data_generator.py mein NUM_RECORDS hardcoded hai.
# Isliye hum ek choti trick use karenge: file ke andar replace karke chalayenge.
# Behtar solution: 1_data_generator.py ko update karein (neeche note dekhein)

sizes = [10000, 100000, 1000000, 10000000]

for n in sizes:
    print(f"\n{'='*60}")
    print(f"📦 Generating {n:,} records...")
    print('='*60)

    # Temporary runner: 1_data_generator ko inject karke chalao
    runner_code = f"""
import runpy, sys
sys.argv = ['1_data_generator.py']
# NUM_RECORDS ko override karne ke liye file patch
src = open('1_data_generator.py').read()
src = src.replace('NUM_RECORDS = 1000000', 'NUM_RECORDS = {n}')
exec(compile(src, '1_data_generator.py', 'exec'))
"""
    subprocess.run([sys.executable, "-c", runner_code], check=True)

print("\n✅ Saare sizes generate ho gaye!")
print("Ab `python 7_benchmark.py` chalayein comparison ke liye.")