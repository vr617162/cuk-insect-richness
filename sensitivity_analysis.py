"""
Sensitivity check: does the richness estimate depend on one observer?

Same filtering as analysis.py, but the most active observer's records are
removed before counting species and computing Chao1. The top observer is
found from the data, so no name is stored in this file.
"""

import pandas as pd

df = pd.read_csv("observation.csv")

insecta = df[df['iconic_taxon_name'] == 'Insecta']
insecta_research_grade = insecta[insecta['quality_grade'] == 'research']

# remove the most active observer
n_before = len(insecta_research_grade)
top_observer = insecta_research_grade['user_login'].value_counts().idxmax()
insecta_research_grade = insecta_research_grade[insecta_research_grade['user_login'] != top_observer]

print("Records removed (top observer) = ", n_before - len(insecta_research_grade))
print("Research Grade == ", len(insecta_research_grade))

S_obs = insecta_research_grade['scientific_name'].nunique()
print(f"Unique species = {S_obs}")

species_counts = insecta_research_grade['scientific_name'].value_counts()
f1 = (species_counts == 1).sum()   # singletons
f2 = (species_counts == 2).sum()   # doubletons

print(f"Singleton = {f1}")
print(f"Doubleton = {f2}")

if f2 > 0:
    S_Chao1 = S_obs + (f1**2) / (2 * f2)
else:
    # bias-corrected Chao1 when there are no doubletons
    S_Chao1 = S_obs + f1 * (f1 - 1) / 2

print("Chao1 = ", round(S_Chao1))

print("Observer-days = ", insecta_research_grade.groupby(["user_login", "observed_on"]).ngroups)
print("Observers remaining = ", insecta_research_grade['user_login'].nunique())
