"""
Insect species richness at CUK from iNaturalist records.

Reads observation.csv (an iNaturalist export of the project's observations),
keeps research-grade insect records, estimates species richness with Chao1
(with a 95% confidence interval) and plots a species accumulation curve.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- 1. Load and filter ----------
df = pd.read_csv("observation.csv")

insecta = df[df['iconic_taxon_name'] == 'Insecta']
insecta_research_grade = insecta[insecta['quality_grade'] == 'research']

print(insecta_research_grade[['iconic_taxon_name', 'scientific_name', 'quality_grade', 'observed_on']])
print("Research Grade == ", len(insecta_research_grade))

# ---------- 2. Counts ----------
S_obs = insecta_research_grade['scientific_name'].nunique()
print(f"Unique species == {S_obs}")

species_counts = insecta_research_grade['scientific_name'].value_counts()
f1 = (species_counts == 1).sum()   # species seen exactly once (singletons)
f2 = (species_counts == 2).sum()   # species seen exactly twice (doubletons)

print(f"Singleton = {f1}")
print(f"Doubleton = {f2}")

observer = insecta_research_grade['user_login'].value_counts()
print("Top observer share = ", round(observer.iloc[0] / len(insecta_research_grade), 2))

# ---------- 3. Chao1 estimate and 95% interval ----------
if f2 > 0:
    T = (f1**2) / (2 * f2)   # estimated number of unseen species
    variance = f2 * (
        0.25 * (f1 / f2)**4
        + (f1 / f2)**3
        + 0.5 * (f1 / f2)**2
    )
else:
    # bias-corrected Chao1 when there are no doubletons
    # (the interval below is only valid for f2 > 0)
    T = f1 * (f1 - 1) / 2
    variance = np.nan

S_Chao1 = S_obs + T
print("Chao1 = ", round(S_Chao1))

z = 1.96
if f2 > 0 and T > 0:
    K = np.exp(z * np.sqrt(np.log(1 + variance / T**2)))

    lower = S_obs + T / K
    upper = S_obs + T * K

    print("T = ", T)
    print("Variance = ", variance)
    print("z = ", z)
    print("K = ", K)
    print("Lower = ", lower)
    print("Upper = ", upper)
else:
    print("95% interval not computed: it needs at least one singleton and one doubleton.")

# ---------- 4. Species accumulation curve ----------
observation = insecta_research_grade['scientific_name'].dropna().to_numpy()

B = 500                       # number of random orderings
n = len(observation)

rng = np.random.default_rng(42)   # fixed seed so the curve is the same on every run
curves = np.zeros((B, n))

for b in range(B):
    shuffled_arr = rng.permutation(observation)

    seen_species = set()
    cumulative_richness = []
    for elements in shuffled_arr:
        seen_species.add(elements)
        cumulative_richness.append(len(seen_species))

    curves[b, :] = cumulative_richness

print(curves.shape)

mean_curve = curves.mean(axis=0)
print("Final average richness", mean_curve[-1])

x = np.arange(1, n + 1)

plt.figure(figsize=(10, 6))
plt.plot(x, mean_curve, linewidth=2)

plt.xlabel("Number of observations")
plt.ylabel("Cumulative Species Richness")
plt.title("Species Accumulation Curve - CUK Insecta (research grade)")
plt.grid(alpha=0.3)

plt.savefig("accumulation_curve.png", dpi=200)
plt.show()
