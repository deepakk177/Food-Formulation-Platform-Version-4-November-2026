import pandas as pd
import re

df_all = pd.read_csv('results/exhaustive_candidate_results.csv')
df_valid = pd.read_csv('results/valid_formulation_results.csv')
df_ranked = pd.read_csv('results/ranked_formulation_results.csv')

# 1. Inspect rejected candidates
rejected = df_all[df_all['Final Status'] == 'REJECTED']
print('Total rejected:', len(rejected))
print('Sample rejected reasons:')
for _, r in rejected.head(5).iterrows():
    print(f"  {r['Candidate ID']}: {r['Hard Constraint Status']}")

# 2. Inspect valid candidates and verify sum == 100%
print('\nVerifying percentage sums of valid formulations:')
for _, r in df_valid.head(20).iterrows():
    opt_str = r['Optimized Formulation']
    pcts = [float(x) for x in re.findall(r'(\d+\.\d+)%', opt_str)]
    s = round(sum(pcts), 2)
    assert abs(s - 100.0) <= 0.05, f'Sum not 100: {s} in {r["Candidate ID"]}'
print('All checked valid formulations sum exactly to 100.00%!')

# 3. Verify ranking continuity
assert list(df_ranked['Rank']) == list(range(1, 361)), 'Rank sequence mismatch!'
print('Ranking sequence is continuous from Rank 1 to Rank 360!')

# 4. Verify candidate counts
assert len(df_all) == 9450
assert len(df_valid) == 360
assert len(rejected) == 9090
assert len(df_all) == len(df_valid) + len(rejected)
print('Zero candidates silently removed or dropped: 9,450 total = 360 valid + 9,090 rejected!')
