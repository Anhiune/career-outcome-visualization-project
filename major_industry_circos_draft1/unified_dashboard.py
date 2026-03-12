import pandas as pd
import holoviews as hv
from holoviews import opts, dim
import json
import os

# Initialize HoloViews
hv.extension('bokeh')
renderer = hv.renderer('bokeh')

# Load analysis results
with open('data_analysis_results.json', 'r') as f:
    data = json.load(f)

# --- Defines ---
large_clusters = {
    "BUSINESS & MANAGEMENT": ["Accounting", "Actuarial Science", "Financial Management", "Risk Management and Insurance", "Gen Business Mgmt", "Entrepreneurship", "Family Business", "Marketing Management", "Bus Admin - Communication", "Business Communication", "Operations Management", "Data Analytics", "International Business", "Real Estate Studies", "Human Resources Management", "Law & Compliance", "Org. Ethics & Compliance"],
    "ENGINEERING & TECHNOLOGY": ["Computer Science", "Computer Engineering", "Software Engineering", "Data Science", "Information Technology", "Quant Methods - Computer Sci", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Manufacturing Engineering", "Systems Engineering"],
    "NATURAL & HEALTH SCIENCES": ["Biology", "Biochemistry", "Neuroscience", "Biology of Global Health", "Chemistry", "Physics", "Geology", "Environmental Science", "Environmental Studies", "Geography", "Geography - Geo Info Sys (GIS)", "Nursing", "Exercise Science", "Public Health", "Health Promotion & Wellness"],
    "SOCIAL SCIENCES & HUMANITIES": ["Psychology", "Sociology", "Political Science", "Economics", "Economics - Business", "Economics - International", "Economics - Mathematical", "Economics - Public Policy", "Criminal Justice", "Justice & Peace Studies", "History", "Philosophy", "Art History", "Classical Civilization", "Intl Studies - Economics", "Intl Studies - History", "Intl Studies - Pol Sci"],
    "COMMUNICATION & MEDIA": ["Journalism", "COJO Journalism", "Digital Media Arts", "COJO Creative Multimedia", "Communication Studies", "Communication and Journalism", "COJO Interpersonal Comm", "COJO Persuasion/Soc Influence", "COJO Strategic Communications", "Strategic Comm: Ad and PR", "Strategic Communication", "English - Creative Writing", "Creative Writing & Publishing"],
    "EDUCATION & SOCIAL SERVICES": ["Elementary Education (K-6)", "Middle/Secondary Education", "K-12 Music Education", "K-12 World Lang. & Cultures", "Teacher Preparation - K-12", "Teacher Preparation-Elem K-6", "Teacher Preparation-Secondary", "Music Education", "Educational Studies", "Early Childhood Special Educ", "Autism Spectrum Disorders", "Acad Behavioral Strategist", "Social Work"],
    "ARTS, LANGUAGES & THEOLOGY": ["French", "German", "Spanish", "Spanish Cultural/Literary St.", "Spanish Linguistics/Lang. St.", "English", "English - Professional Writing", "Music", "Music - Business", "Music - Performance", "Mathematics (Applied Track)", "Mathematics (Education Track)", "Mathematics (Pure Track)", "Mathematics (Statistics Track)", "Statistics", "Theology", "Catholic Studies", "Pastoral Leadership", "Pastoral Ministry", "Legal Studies", "Individualized", "Family Studies"]
}

small_clusters = {
    "Finance & Accounting": ["Accounting", "Actuarial Science", "Financial Management", "Risk Management and Insurance"],
    "General Business": ["Gen Business Mgmt", "Entrepreneurship", "Family Business"],
    "Marketing & Communication": ["Marketing Management", "Bus Admin - Communication", "Business Communication"],
    "Operations & Analytics": ["Operations Management", "Data Analytics"],
    "Specialized Business": ["International Business", "Real Estate Studies", "Human Resources Management", "Law & Compliance", "Org. Ethics & Compliance"],
    "Computer Science & IT": ["Computer Science", "Software Engineering", "Data Science", "Information Technology", "Quant Methods - Computer Sci"],
    "Engineering Disciplines": ["Mechanical Engineering", "Electrical Engineering", "Civil Engineering", "Manufacturing Engineering", "Systems Engineering", "Computer Engineering"],
    "Biological Sciences": ["Biology", "Biochemistry", "Neuroscience", "Biology of Global Health"],
    "Physical Sciences": ["Chemistry", "Physics", "Geology"],
    "Environmental Sciences": ["Environmental Science", "Environmental Studies", "Geography", "Geography - Geo Info Sys (GIS)"],
    "Health & Wellness": ["Nursing", "Exercise Science", "Public Health", "Health Promotion & Wellness"],
    "Economics": ["Economics", "Economics - Business", "Economics - International", "Economics - Mathematical", "Economics - Public Policy"],
    "Social Sciences": ["Psychology", "Sociology", "Political Science", "Criminal Justice", "Justice & Peace Studies"],
    "Humanities": ["History", "Philosophy", "Art History", "Classical Civilization"],
    "International Studies": ["Intl Studies - Economics", "Intl Studies - History", "Intl Studies - Pol Sci"],
    "Journalism & Media": ["Journalism", "COJO Journalism", "Digital Media Arts", "COJO Creative Multimedia"],
    "Communication Studies": ["Communication Studies", "Communication and Journalism", "COJO Interpersonal Comm", "COJO Persuasion/Soc Influence", "COJO Strategic Communications", "Strategic Comm: Ad and PR", "Strategic Communication"],
    "Creative Writing": ["English - Creative Writing", "Creative Writing & Publishing"],
    "Teacher Education": ["Elementary Education (K-6)", "Middle/Secondary Education", "K-12 Music Education", "K-12 World Lang. & Cultures", "Teacher Preparation - K-12", "Teacher Preparation-Elem K-6", "Teacher Preparation-Secondary", "Music Education"],
    "Educational Leadership": ["Educational Studies"],
    "Special Education & Counseling": ["Early Childhood Special Educ", "Autism Spectrum Disorders", "Acad Behavioral Strategist"],
    "Social Work": ["Social Work"],
    "Languages": ["French", "German", "Spanish", "Spanish Cultural/Literary St.", "Spanish Linguistics/Lang. St."],
    "English & Writing": ["English", "English - Professional Writing"],
    "Arts & Music": ["Music", "Music - Business", "Music - Performance"],
    "Mathematics": ["Mathematics (Applied Track)", "Mathematics (Education Track)", "Mathematics (Pure Track)", "Mathematics (Statistics Track)", "Statistics"],
    "Theology": ["Theology", "Catholic Studies", "Pastoral Leadership", "Pastoral Ministry"],
    "Legal & Other": ["Legal Studies"],
    "Miscellaneous": ["Individualized", "Family Studies"]
}


# --- Prepare DataFrames ---

# 1. Large Clusters
large_cluster_data = []
for cluster, majors in large_clusters.items():
    count = sum(data['major_counts'].get(m, 0) for m in majors)
    large_cluster_data.append((cluster, count))
df_large = pd.DataFrame(large_cluster_data, columns=['Cluster', 'Students']).sort_values('Students', ascending=True)

# 2. Small Clusters
small_cluster_data = []
for cluster, majors in small_clusters.items():
    count = sum(data['major_counts'].get(m, 0) for m in majors)
    # Find parent
    parent = "Unknown"
    for p_name, p_majors in large_clusters.items():
        if any(m in p_majors for m in majors):
            parent = p_name
            break
    small_cluster_data.append((cluster, count, parent))
df_small = pd.DataFrame(small_cluster_data, columns=['Cluster', 'Students', 'Parent']).sort_values('Students', ascending=True)

# 3. Top 20 Majors
top_majors_data = [(m, data['major_counts'][m]) for m in data['majors']]
df_majors = pd.DataFrame(top_majors_data, columns=['Major', 'Students']).sort_values('Students', ascending=False).head(20).iloc[::-1]

# --- Visualization Objects ---

# 1. Large Cluster Bar Chart
bars_large = hv.Bars(df_large, 'Cluster', 'Students').opts(
    title="Students by Large Cluster (Tier 3)",
    color='Students', cmap='Viridis',
    invert_axes=True, 
    width=800, height=400,
    tools=['hover'],
    fontsize={'labels': 10, 'xticks': 10, 'yticks': 10},
    show_legend=False
)

# 2. Small Cluster Bar Chart
bars_small = hv.Bars(df_small, 'Cluster', 'Students').opts(
    title="Students by Small Cluster (Tier 2)",
    color='Students', cmap='Plasma',
    invert_axes=True,
    width=800, height=600,
    tools=['hover'],
    fontsize={'labels': 9, 'xticks': 9, 'yticks': 9},
    show_legend=False
)

# 3. Top 20 Majors Bar Chart
bars_majors = hv.Bars(df_majors, 'Major', 'Students').opts(
    title="Top 20 Individual Majors (Tier 1)",
    color='Students', cmap='Cool',
    invert_axes=True,
    width=800, height=600,
    tools=['hover'],
    show_legend=False
)

# 4. Hierarchical Sunburst (Approximate with HoloViews)
# We need to construct a hierarchy mapping. 
# Holoviews doesn't have a direct Sunburst in the main API easily without creating complex data structures, 
# but we can simulate a hierarchy view or just use the layout of bars.
# For simplicity and robustness in this environment, we will stick to the Bar charts as they are clearest.

# Layout
layout = (bars_large + bars_small + bars_majors).cols(1)
layout.opts(
    opts.Bars(shared_axes=False)
)

# Save to HTML
output_path = os.path.join(os.path.dirname(__file__), "unified_analysis_dashboard.html")
hv.save(layout, output_path)

print(f"Dashboard generated at: {output_path}")
