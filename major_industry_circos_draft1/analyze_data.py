import pandas as pd
import json

# Load the Excel file
df = pd.read_excel('Ire Anh Data 1.22.26 (1).xlsx')

print("=== DATASET OVERVIEW ===")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"\nColumn names:")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

print("\n=== MAJOR ANALYSIS ===")
majors = df['Program Name/Major'].dropna()
unique_majors = sorted(majors.unique())
print(f"Total unique majors: {len(unique_majors)}")
print(f"\nAll majors:")
for i, major in enumerate(unique_majors, 1):
    count = (majors == major).sum()
    print(f"{i}. {major} ({count} students)")

print("\n=== CAREER-RELATED COLUMNS ===")
career_keywords = ['job', 'employer', 'career', 'position', 'title', 'company', 'organization', 'industry']
career_cols = [c for c in df.columns if any(kw in c.lower() for kw in career_keywords)]
print(f"Found {len(career_cols)} career-related columns:")
for col in career_cols:
    print(f"  - {col}")
    non_null = df[col].dropna()
    print(f"    Non-null entries: {len(non_null)}")
    if len(non_null) > 0:
        print(f"    Sample values: {non_null.head(5).tolist()}")

# Save results to JSON for easier parsing
results = {
    'majors': unique_majors,
    'major_counts': {major: int((majors == major).sum()) for major in unique_majors},
    'career_columns': career_cols,
    'total_students': len(df)
}

with open('data_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n=== Results saved to data_analysis_results.json ===")
