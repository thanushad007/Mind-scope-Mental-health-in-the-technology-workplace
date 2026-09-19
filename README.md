# 🧠 MindScope – Mental Health in Tech

An interactive Exploratory Data Analysis and visualization dashboard built using Python and Streamlit to explore mental health patterns in the technology workplace.

## 📌 Project Overview

MindScope transforms a mental-health survey dataset into an interactive dashboard where users can explore treatment patterns, workplace experiences, family history, remote work, company size, and geographic trends.

The project combines data cleaning, exploratory data analysis, interactive visualization, and categorical association analysis.

## 🎯 Objectives

- Clean and prepare the mental-health survey dataset.
- Perform Exploratory Data Analysis (EDA).
- Identify patterns related to mental-health treatment.
- Analyze workplace and mental-health-related factors.
- Explore geographic distribution of respondents.
- Measure associations between categorical variables using Cramér's V.
- Build an interactive Streamlit dashboard.
- Provide filtered data and analysis results for download.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Cramér's V
- Jupyter / VS Code

## 📊 Dashboard Features

### 🔎 Interactive Filters

Users can filter the dashboard by:

- Mental Health Treatment
- Country
- Gender
- Remote Work
- Family History
- Age Range

### 📈 KPI Cards

The dashboard displays:

- Total Respondents
- Number of Countries
- Average Age
- Treatment Rate

### 📊 Visualizations

The dashboard includes analysis of:

- Mental Health Treatment
- Age Distribution
- Gender Distribution
- Family History
- Work Interference
- Family History vs Treatment
- Mental vs Physical Health
- Remote Work
- Technology Company
- Mental Health Benefits
- Company Size vs Treatment
- Country Treatment Rate

### 🌍 Geographic Analysis

A world map is used to visualize treatment rates across countries, along with a country-level summary table.

### 🔬 Association Analysis

Cramér's V is used to measure the strength of association between mental-health treatment and categorical variables such as:

- Work Interference
- Family History
- Care Options
- Benefits
- Leave
- Anonymity
- Mental Health Consequence
- Mental vs Physical Health
- Mental Health Interview

> *Note:* Association does not establish causation.

## 🧹 Data Preparation

The dataset was cleaned and prepared before visualization.

Major preprocessing steps included:

- Converting the Age column into numeric format.
- Handling unrealistic age values.
- Handling missing categorical values.
- Preparing the dataset for visualization and analysis.
- Checking duplicate records.

## 📁 Project Structure

```text
Mental_health_EDA/
│
├── app.py
├── EDA.py
├── survey.csv
├── cleaned_survey.csv
├── association_analysis.csv
├── requirements.txt
├── README.md
├── .gitignore
│
└── eda_outputs/
    ├── EDA visualizations
    ├── analysis outputs
    └── generated charts
