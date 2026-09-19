# ============================================================
# MENTAL HEALTH IN TECH SURVEY - EXPLORATORY DATA ANALYSIS
# Internship Project
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. SETTINGS
# ============================================================

sns.set_theme(style="whitegrid")

# Create folder for EDA outputs
os.makedirs("eda_outputs", exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_csv("survey.csv")

print("=" * 70)
print("MENTAL HEALTH IN TECH SURVEY - EDA")
print("=" * 70)

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())


# ============================================================
# 3. DATASET INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

df.info()


# ============================================================
# 4. DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE CHECK")
print("=" * 70)

duplicates = df.duplicated().sum()

print("Number of duplicate rows:", duplicates)


# ============================================================
# 5. MISSING VALUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUE ANALYSIS")
print("=" * 70)

missing = df.isnull().sum()
missing_percentage = (missing / len(df)) * 100

missing_table = pd.DataFrame({
    "Missing Values": missing,
    "Percentage": missing_percentage.round(2)
})

print(missing_table[missing_table["Missing Values"] > 0])


# Missing-value chart
missing_plot = missing[missing > 0].sort_values(ascending=False)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=missing_plot.values,
    y=missing_plot.index
)

plt.title("Missing Values by Column")
plt.xlabel("Number of Missing Values")
plt.ylabel("Column")

plt.tight_layout()
plt.savefig("eda_outputs/01_missing_values.png", dpi=300)
plt.close()


# ============================================================
# 6. DATA CLEANING
# ============================================================

print("\n" + "=" * 70)
print("DATA CLEANING")
print("=" * 70)

df_clean = df.copy()

# Convert Age to numeric
df_clean["Age"] = pd.to_numeric(
    df_clean["Age"],
    errors="coerce"
)

# Remove clearly invalid age values
invalid_age = (
    (df_clean["Age"] < 18) |
    (df_clean["Age"] > 100)
)

print("Invalid age values:", invalid_age.sum())

df_clean.loc[invalid_age, "Age"] = np.nan

# Fill categorical missing values
df_clean["state"] = df_clean["state"].fillna("Not Applicable")

df_clean["self_employed"] = (
    df_clean["self_employed"]
    .fillna("Unknown")
)

df_clean["work_interfere"] = (
    df_clean["work_interfere"]
    .fillna("Not Answered")
)

# Keep comments unchanged because it is an optional text field


print("\nMissing values after cleaning:")

print(df_clean.isnull().sum()[df_clean.isnull().sum() > 0])


# Save cleaned dataset
df_clean.to_csv(
    "eda_outputs/cleaned_survey.csv",
    index=False
)


# ============================================================
# 7. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)

print(df_clean.describe())


# Age statistics
print("\nAge Statistics:")

print(
    df_clean["Age"].describe()
)


# ============================================================
# 8. AGE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df_clean,
    x="Age",
    bins=20,
    kde=True
)

plt.title("Age Distribution of Respondents")
plt.xlabel("Age")
plt.ylabel("Number of Respondents")

plt.tight_layout()
plt.savefig(
    "eda_outputs/02_age_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 9. GENDER DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("GENDER DISTRIBUTION")
print("=" * 70)

print(
    df_clean["Gender"].value_counts()
)


gender_counts = (
    df_clean["Gender"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=gender_counts.values,
    y=gender_counts.index
)

plt.title("Gender Distribution")
plt.xlabel("Number of Respondents")
plt.ylabel("Gender")

plt.tight_layout()
plt.savefig(
    "eda_outputs/03_gender_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 10. COUNTRY DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("TOP COUNTRIES")
print("=" * 70)

country_counts = (
    df_clean["Country"]
    .value_counts()
)

print(country_counts.head(15))


top_countries = country_counts.head(10)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=top_countries.values,
    y=top_countries.index
)

plt.title("Top 10 Countries by Number of Respondents")
plt.xlabel("Number of Respondents")
plt.ylabel("Country")

plt.tight_layout()
plt.savefig(
    "eda_outputs/04_top_countries.png",
    dpi=300
)

plt.close()


# ============================================================
# 11. TREATMENT DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("MENTAL HEALTH TREATMENT")
print("=" * 70)

print(
    df_clean["treatment"].value_counts()
)

treatment_counts = (
    df_clean["treatment"]
    .value_counts()
)

plt.figure(figsize=(7, 5))

sns.barplot(
    x=treatment_counts.index,
    y=treatment_counts.values
)

plt.title("Mental Health Treatment Distribution")
plt.xlabel("Sought Treatment")
plt.ylabel("Number of Respondents")

plt.tight_layout()
plt.savefig(
    "eda_outputs/05_treatment_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 12. FAMILY HISTORY
# ============================================================

print("\n" + "=" * 70)
print("FAMILY HISTORY OF MENTAL ILLNESS")
print("=" * 70)

print(
    df_clean["family_history"].value_counts()
)

plt.figure(figsize=(7, 5))

sns.countplot(
    data=df_clean,
    x="family_history"
)

plt.title("Family History of Mental Illness")
plt.xlabel("Family History")
plt.ylabel("Number of Respondents")

plt.tight_layout()
plt.savefig(
    "eda_outputs/06_family_history.png",
    dpi=300
)

plt.close()


# ============================================================
# 13. FAMILY HISTORY VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("FAMILY HISTORY VS TREATMENT")
print("=" * 70)

family_treatment = pd.crosstab(
    df_clean["family_history"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    family_treatment.round(2)
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    family_treatment,
    annot=True,
    fmt=".1f",
    cmap="Blues"
)

plt.title(
    "Treatment Rate by Family History (%)"
)

plt.xlabel("Treatment")
plt.ylabel("Family History")

plt.tight_layout()
plt.savefig(
    "eda_outputs/07_family_history_vs_treatment.png",
    dpi=300
)

plt.close()


# ============================================================
# 14. WORK INTERFERENCE
# ============================================================

print("\n" + "=" * 70)
print("WORK INTERFERENCE")
print("=" * 70)

print(
    df_clean["work_interfere"].value_counts()
)

plt.figure(figsize=(9, 6))

order = [
    "Never",
    "Rarely",
    "Sometimes",
    "Often",
    "Not Answered"
]

sns.countplot(
    data=df_clean,
    y="work_interfere",
    order=[
        x for x in order
        if x in df_clean["work_interfere"].unique()
    ]
)

plt.title("Mental Health Impact on Work")
plt.xlabel("Number of Respondents")
plt.ylabel("Work Interference")

plt.tight_layout()
plt.savefig(
    "eda_outputs/08_work_interference.png",
    dpi=300
)

plt.close()


# ============================================================
# 15. WORK INTERFERENCE VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("WORK INTERFERENCE VS TREATMENT")
print("=" * 70)

work_treatment = pd.crosstab(
    df_clean["work_interfere"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    work_treatment.round(2)
)

plt.figure(figsize=(9, 6))

sns.heatmap(
    work_treatment,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu"
)

plt.title(
    "Treatment Distribution by Work Interference (%)"
)

plt.xlabel("Treatment")
plt.ylabel("Work Interference")

plt.tight_layout()
plt.savefig(
    "eda_outputs/09_work_interference_vs_treatment.png",
    dpi=300
)

plt.close()


# ============================================================
# 16. REMOTE WORK VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("REMOTE WORK VS TREATMENT")
print("=" * 70)

remote_treatment = pd.crosstab(
    df_clean["remote_work"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    remote_treatment.round(2)
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    remote_treatment,
    annot=True,
    fmt=".1f",
    cmap="Purples"
)

plt.title(
    "Treatment Distribution by Remote Work Status (%)"
)

plt.xlabel("Treatment")
plt.ylabel("Remote Work")

plt.tight_layout()
plt.savefig(
    "eda_outputs/10_remote_work_vs_treatment.png",
    dpi=300
)

plt.close()


# ============================================================
# 17. TECH COMPANY VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("TECH COMPANY VS TREATMENT")
print("=" * 70)

tech_treatment = pd.crosstab(
    df_clean["tech_company"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    tech_treatment.round(2)
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    tech_treatment,
    annot=True,
    fmt=".1f",
    cmap="Oranges"
)

plt.title(
    "Treatment Distribution by Tech Company Status (%)"
)

plt.xlabel("Treatment")
plt.ylabel("Tech Company")

plt.tight_layout()
plt.savefig(
    "eda_outputs/11_tech_company_vs_treatment.png",
    dpi=300
)

plt.close()


# ============================================================
# 18. COMPANY SIZE VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("COMPANY SIZE VS TREATMENT")
print("=" * 70)

company_treatment = pd.crosstab(
    df_clean["no_employees"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    company_treatment.round(2)
)

plt.figure(figsize=(10, 6))

sns.heatmap(
    company_treatment,
    annot=True,
    fmt=".1f",
    cmap="Greens"
)

plt.title(
    "Treatment Distribution by Company Size (%)"
)

plt.xlabel("Treatment")
plt.ylabel("Company Size")

plt.tight_layout()
plt.savefig(
    "eda_outputs/12_company_size_vs_treatment.png",
    dpi=300
)

plt.close()


# ============================================================
# 19. BENEFITS VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("MENTAL HEALTH BENEFITS VS TREATMENT")
print("=" * 70)

benefits_treatment = pd.crosstab(
    df_clean["benefits"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    benefits_treatment.round(2)
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    benefits_treatment,
    annot=True,
    fmt=".1f",
    cmap="coolwarm"
)

plt.title(
    "Treatment Distribution by Mental Health Benefits (%)"
)

plt.xlabel("Treatment")
plt.ylabel("Benefits")

plt.tight_layout()
plt.savefig(
    "eda_outputs/13_benefits_vs_treatment.png",
    dpi=300
)

plt.close()


# ============================================================
# 20. MENTAL HEALTH CONSEQUENCE
# ============================================================

print("\n" + "=" * 70)
print("MENTAL HEALTH CONSEQUENCES")
print("=" * 70)

print(
    df_clean["mental_health_consequence"].value_counts()
)

plt.figure(figsize=(8, 6))

sns.countplot(
    data=df_clean,
    x="mental_health_consequence"
)

plt.title(
    "Perceived Negative Consequences of Discussing Mental Health"
)

plt.xlabel("Mental Health Consequence")
plt.ylabel("Number of Respondents")

plt.tight_layout()
plt.savefig(
    "eda_outputs/14_mental_health_consequence.png",
    dpi=300
)

plt.close()


# ============================================================
# 21. MENTAL VS PHYSICAL HEALTH
# ============================================================

print("\n" + "=" * 70)
print("MENTAL HEALTH VS PHYSICAL HEALTH")
print("=" * 70)

print(
    df_clean["mental_vs_physical"].value_counts()
)

plt.figure(figsize=(8, 6))

sns.countplot(
    data=df_clean,
    x="mental_vs_physical"
)

plt.title(
    "Is Mental Health Taken as Seriously as Physical Health?"
)

plt.xlabel("Mental vs Physical Health")
plt.ylabel("Number of Respondents")

plt.tight_layout()
plt.savefig(
    "eda_outputs/15_mental_vs_physical.png",
    dpi=300
)

plt.close()


# ============================================================
# 22. COWORKERS VS SUPERVISORS
# ============================================================

print("\n" + "=" * 70)
print("DISCUSSING MENTAL HEALTH AT WORK")
print("=" * 70)

coworker_counts = df_clean["coworkers"].value_counts()
supervisor_counts = df_clean["supervisor"].value_counts()

discussion_table = pd.DataFrame({
    "Coworkers": coworker_counts,
    "Supervisors": supervisor_counts
})

print(discussion_table)


# ============================================================
# 23. OBSERVED NEGATIVE CONSEQUENCES
# ============================================================

print("\n" + "=" * 70)
print("OBSERVED NEGATIVE CONSEQUENCES")
print("=" * 70)

print(
    df_clean["obs_consequence"].value_counts()
)

plt.figure(figsize=(8, 6))

sns.countplot(
    data=df_clean,
    x="obs_consequence"
)

plt.title(
    "Observed Negative Consequences for Coworkers"
)

plt.xlabel("Observed Consequence")
plt.ylabel("Number of Respondents")

plt.tight_layout()
plt.savefig(
    "eda_outputs/16_observed_consequences.png",
    dpi=300
)

plt.close()


# ============================================================
# 24. GEOGRAPHIC ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("GEOGRAPHIC ANALYSIS")
print("=" * 70)

country_summary = (
    df_clean
    .groupby("Country")
    .agg(
        Respondents=("Country", "size"),
        Treatment_Rate=(
            "treatment",
            lambda x: (x == "Yes").mean() * 100
        )
    )
    .sort_values(
        "Respondents",
        ascending=False
    )
)

print(
    country_summary.head(15).round(2)
)

# Only countries with at least 10 respondents
country_filtered = country_summary[
    country_summary["Respondents"] >= 10
].sort_values(
    "Treatment_Rate",
    ascending=False
)

print("\nCountries with at least 10 respondents:")
print(
    country_filtered.round(2)
)


# Geographic treatment rate chart
top_country_rates = (
    country_filtered
    .sort_values(
        "Treatment_Rate",
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=top_country_rates,
    x="Treatment_Rate",
    y=top_country_rates.index
)

plt.title(
    "Treatment Rate by Country\n(Minimum 10 Respondents)"
)

plt.xlabel("Treatment Rate (%)")
plt.ylabel("Country")

plt.tight_layout()
plt.savefig(
    "eda_outputs/17_country_treatment_rate.png",
    dpi=300
)

plt.close()


# ============================================================
# 25. CARE OPTIONS VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("CARE OPTIONS VS TREATMENT")
print("=" * 70)

care_treatment = pd.crosstab(
    df_clean["care_options"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    care_treatment.round(2)
)


# ============================================================
# 26. WELLNESS PROGRAM VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("WELLNESS PROGRAM VS TREATMENT")
print("=" * 70)

wellness_treatment = pd.crosstab(
    df_clean["wellness_program"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    wellness_treatment.round(2)
)


# ============================================================
# 27. ANONYMITY VS TREATMENT
# ============================================================

print("\n" + "=" * 70)
print("ANONYMITY VS TREATMENT")
print("=" * 70)

anonymity_treatment = pd.crosstab(
    df_clean["anonymity"],
    df_clean["treatment"],
    normalize="index"
) * 100

print(
    anonymity_treatment.round(2)
)


# ============================================================
# 28. SELECTED ASSOCIATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("ASSOCIATION ANALYSIS")
print("=" * 70)

# Cramer's V measures association between categorical variables.
# It does NOT establish causation.

def cramers_v(x, y):

    table = pd.crosstab(x, y)

    observed = table.values

    row_totals = observed.sum(axis=1)
    col_totals = observed.sum(axis=0)
    total = observed.sum()

    expected = np.outer(
        row_totals,
        col_totals
    ) / total

    chi_square = (
        (observed - expected) ** 2 / expected
    ).sum()

    n = observed.sum()

    phi2 = chi_square / n

    rows, cols = observed.shape

    phi2_corrected = max(
        0,
        phi2 - ((cols - 1) * (rows - 1)) / (n - 1)
    )

    rows_corrected = rows - (
        ((rows - 1) ** 2) / (n - 1)
    )

    cols_corrected = cols - (
        ((cols - 1) ** 2) / (n - 1)
    )

    denominator = min(
        cols_corrected - 1,
        rows_corrected - 1
    )

    if denominator <= 0:
        return np.nan

    return np.sqrt(
        phi2_corrected / denominator
    )


predictor_columns = [
    "family_history",
    "work_interfere",
    "remote_work",
    "tech_company",
    "benefits",
    "care_options",
    "wellness_program",
    "seek_help",
    "anonymity",
    "leave",
    "mental_health_consequence",
    "phys_health_consequence",
    "coworkers",
    "supervisor",
    "mental_health_interview",
    "mental_vs_physical",
    "obs_consequence"
]

association_results = []

for column in predictor_columns:

    value = cramers_v(
        df_clean[column],
        df_clean["treatment"]
    )

    association_results.append({
        "Variable": column,
        "Cramers_V": value
    })


association_df = pd.DataFrame(
    association_results
).sort_values(
    "Cramers_V",
    ascending=False
)

print(
    association_df.round(3)
)

association_df.to_csv(
    "eda_outputs/association_analysis.csv",
    index=False
)


# ============================================================
# 29. TOP ASSOCIATIONS CHART
# ============================================================

top_associations = (
    association_df
    .head(10)
    .sort_values(
        "Cramers_V",
        ascending=True
    )
)

plt.figure(figsize=(10, 7))

sns.barplot(
    data=top_associations,
    x="Cramers_V",
    y="Variable"
)

plt.title(
    "Top Variables Associated with Treatment"
)

plt.xlabel("Cramer's V")
plt.ylabel("Variable")

plt.tight_layout()
plt.savefig(
    "eda_outputs/18_top_treatment_associations.png",
    dpi=300
)

plt.close()


# ============================================================
# 30. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nDataset:")
print("Rows:", len(df_clean))
print("Columns:", len(df_clean.columns))

print("\nDuplicates:", df_clean.duplicated().sum())

print("\nRemaining missing values:")
print(
    df_clean.isnull().sum().sum()
)

print("\nTreatment distribution:")
print(
    df_clean["treatment"].value_counts()
)

print("\nTop variables associated with treatment:")
print(
    association_df.head(10).round(3)
)

print("\nAll charts and analysis files have been saved in:")
print("eda_outputs/")

print("\nEDA completed.")