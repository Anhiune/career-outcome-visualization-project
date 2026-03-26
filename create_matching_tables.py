import pandas as pd
from collections import defaultdict
import csv

# Source files
raw_data = r"c:\Users\hoang\Documents\project_test\data\career_outcomes_final.csv"
v4_jobs = r"c:\Users\hoang\Documents\project_test\csv_data\Major_Career_Analysis_v4__Job_Titles_by_Years.csv"

# Output files
out_major_ind = r"c:\Users\hoang\Documents\project_test\csv_exports\Major_to_Industry_Match_v3.csv"
out_job_ind = r"c:\Users\hoang\Documents\project_test\csv_exports\Job_to_Industry_Match_v4.csv"

def generate_matches():
    print("Loading raw outcome data...")
    df = pd.read_csv(raw_data)
    
    # 1. Match Major (Small Cluster) to Industry (Job Function / Career Cluster)
    # Using 'Major Subcluster' as Major, and 'Job Function' as Industry
    major_ind_counts = defaultdict(int)
    for _, row in df.iterrows():
        major = str(row.get('Major Subcluster', 'Unknown')).strip()
        industry = str(row.get('Job Function', 'Unknown')).strip()
        if major == 'nan' or not major:
            major = 'Unknown'
        if industry == 'nan' or not industry:
            industry = 'Unknown'
            
        major_ind_counts[(major, industry)] += 1
        
    with open(out_major_ind, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Major (Small Cluster)', 'Industry (Job Function)', 'Count'])
        for (m, i), count in sorted(major_ind_counts.items(), key=lambda x: (-x[1], x[0])):
            writer.writerow([m, i, count])
    print(f"Created Major -> Industry mapping (V3 logic) at {out_major_ind}")
    
    
    # 2. Match Job Title to Industry (Small Cluster) using V4 data
    # The actual V4 file has 'Job Title', 'Small Cluster', etc.
    print("Loading V4 job title data...")
    df_v4 = pd.read_csv(v4_jobs)
    
    with open(out_job_ind, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Industry (Small Cluster)'])
        
        # We just need the unique mapping of Job Title to Industry
        job_map = {}
        for _, row in df_v4.iterrows():
            job = str(row.get('Job Title', '')).strip()
            ind = str(row.get('Small Cluster', '')).strip()
            if job and job != 'nan' and ind and ind != 'nan':
                job_map[job] = ind
                
        for job, ind in sorted(job_map.items()):
            writer.writerow([job, ind])
            
    print(f"Created Job Title -> Industry mapping (V4 logic) at {out_job_ind}")

if __name__ == '__main__':
    generate_matches()
