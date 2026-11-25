import pandas as pd

df = pd.read_csv("observation.csv")

insecta = df[df['iconic_taxon_name'] == 'Insecta']
insecta_research_grade = insecta[insecta['quality_grade'] == 'research']
insecta_research_grade = insecta_research_grade[insecta_research_grade['user_login'] != 'ganesh66491']

print(insecta_research_grade[['iconic_taxon_name','scientific_name','quality_grade','observed_on','user_name']])
print("Research Grade == ",len(insecta_research_grade))

S_obs = insecta_research_grade['scientific_name'].nunique()
print(f"Unique species = {S_obs}")

f1 = (insecta_research_grade['scientific_name'].value_counts() == 1).sum()
f2 = (insecta_research_grade['scientific_name'].value_counts() == 2).sum()

print(f"Singleton = {f1}")
print(f"Doubleton = {f2}")

S_Chao1 = S_obs + ((f1**2) / (2*f2))

print("Chao1 = ",round(S_Chao1))
print(insecta_research_grade.groupby(["user_login", "observed_on"]).ngroups)

observer = insecta_research_grade['user_login'].value_counts()
print(observer)

