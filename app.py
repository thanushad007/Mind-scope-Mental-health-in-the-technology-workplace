# ============================================================
# MENTAL HEALTH IN TECH SURVEY
# INTERACTIVE STREAMLIT DASHBOARD
# INTERNSHIP PROJECT
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION 
# ============================================================

st.set_page_config(
    page_title="MindScope | Mental Health in Tech",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ==========================================================
   MAIN BACKGROUND
   ========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(124, 58, 237, 0.14),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(14, 165, 233, 0.14),
            transparent 25%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(236, 72, 153, 0.10),
            transparent 30%
        ),
        #0b1020;
}

/* ==========================================================
   MAIN CONTAINER
   ========================================================== */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #17112b 50%,
            #101827 100%
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {
    padding: 35px;
    border-radius: 25px;
    margin-bottom: 25px;

    background:
        linear-gradient(
            135deg,
            rgba(124, 58, 237, 0.96),
            rgba(37, 99, 235, 0.94),
            rgba(14, 165, 233, 0.90)
        );

    box-shadow:
        0 20px 50px rgba(0,0,0,0.35);

    border: 1px solid rgba(255,255,255,0.15);
}

.hero-title {
    color: white;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: rgba(255,255,255,0.94);
    font-size: 19px;
    font-weight: 600;
    margin-bottom: 10px;
}

.hero-description {
    color: rgba(255,255,255,0.82);
    font-size: 14px;
    line-height: 1.7;
}


/* ==========================================================
   SECTION TITLES
   ========================================================== */

.section-title {
    color: #f8fafc;
    font-size: 25px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 15px;
}


/* ==========================================================
   KPI CARDS
   ========================================================== */

.kpi-card {
    padding: 22px;
    min-height: 135px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.96),
            rgba(15,23,42,0.96)
        );

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.20);
}

.kpi-icon {
    font-size: 28px;
}

.kpi-label {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 600;
    margin-top: 8px;
}

.kpi-value {
    color: white;
    font-size: 30px;
    font-weight: 800;
    margin-top: 4px;
}


/* ==========================================================
   INFO CARD
   ========================================================== */

.info-card {
    padding: 22px;
    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,59,0.92),
            rgba(17,24,39,0.92)
        );

    border: 1px solid rgba(255,255,255,0.08);

    color: #e2e8f0;
}

.info-card h3 {
    color: #f8fafc;
    margin-top: 0;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {
    margin-top: 50px;
    padding: 25px;
    text-align: center;

    color: #94a3b8;

    border-top: 1px solid rgba(255,255,255,0.08);
}


/* ==========================================================
   TABS
   ========================================================== */

button[data-baseweb="tab"] {
    font-weight: 700;
}


/* ==========================================================
   DOWNLOAD BUTTON
   ========================================================== */

.stDownloadButton button {
    border-radius: 12px;
    font-weight: 700;
}


/* ==========================================================
   SELECT BOXES
   ========================================================== */

div[data-baseweb="select"] > div {
    border-radius: 10px;
}


/* ==========================================================
   HIDE STREAMLIT DEFAULT FOOTER
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD + CLEAN DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv("survey.csv")

    # --------------------------------------------------------
    # Clean Age
    # --------------------------------------------------------

    data["Age"] = pd.to_numeric(
        data["Age"],
        errors="coerce"
    )

    # Remove unrealistic ages
    data.loc[
        (data["Age"] < 18) |
        (data["Age"] > 80),
        "Age"
    ] = np.nan

    # --------------------------------------------------------
    # Clean categorical missing values
    # --------------------------------------------------------

    if "state" in data.columns:
        data["state"] = data["state"].fillna(
            "Not Applicable"
        )

    if "self_employed" in data.columns:
        data["self_employed"] = data[
            "self_employed"
        ].fillna("Unknown")

    if "work_interfere" in data.columns:
        data["work_interfere"] = data[
            "work_interfere"
        ].fillna("Not Answered")

    return data


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎛️ Dashboard Filters")

    st.caption(
        "Use the filters below to explore different "
        "segments of the survey."
    )

    st.divider()

    # --------------------------------------------------------
    # Treatment
    # --------------------------------------------------------

    treatment_options = sorted(
        df["treatment"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_treatment = st.multiselect(
        "🧠 Mental Health Treatment",
        treatment_options,
        default=treatment_options
    )

    # --------------------------------------------------------
    # Country
    # --------------------------------------------------------

    country_options = sorted(
        df["Country"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_countries = st.multiselect(
        "🌍 Country",
        country_options,
        default=[],
        help="Leave empty to include all countries."
    )

    # --------------------------------------------------------
    # Gender
    # --------------------------------------------------------

    gender_options = sorted(
        df["Gender"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_gender = st.multiselect(
        "👤 Gender",
        gender_options,
        default=[]
    )

    # --------------------------------------------------------
    # Remote Work
    # --------------------------------------------------------

    remote_options = sorted(
        df["remote_work"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_remote = st.multiselect(
        "🏠 Remote Work",
        remote_options,
        default=[]
    )

    # --------------------------------------------------------
    # Family History
    # --------------------------------------------------------

    family_options = sorted(
        df["family_history"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_family = st.multiselect(
        "👨‍👩‍👧 Family History",
        family_options,
        default=[]
    )

    # --------------------------------------------------------
    # Age
    # --------------------------------------------------------

    valid_ages = df["Age"].dropna()

    if not valid_ages.empty:

        min_age = int(valid_ages.min())
        max_age = int(valid_ages.max())

        age_range = st.slider(
            "🎂 Age Range",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age)
        )

    else:

        age_range = (18, 80)

    st.divider()

    st.markdown("### 💡 About MindScope")

    st.caption(
        """
        MindScope explores mental health experiences,
        treatment patterns, workplace attitudes,
        support systems and geographic variation
        within the survey dataset.
        """
    )

    st.caption(
        "🐍 Python • Pandas • Plotly • Streamlit"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_treatment:

    filtered_df = filtered_df[
        filtered_df["treatment"].isin(
            selected_treatment
        )
    ]


if selected_countries:

    filtered_df = filtered_df[
        filtered_df["Country"].isin(
            selected_countries
        )
    ]


if selected_gender:

    filtered_df = filtered_df[
        filtered_df["Gender"].isin(
            selected_gender
        )
    ]


if selected_remote:

    filtered_df = filtered_df[
        filtered_df["remote_work"].isin(
            selected_remote
        )
    ]


if selected_family:

    filtered_df = filtered_df[
        filtered_df["family_history"].isin(
            selected_family
        )
    ]


filtered_df = filtered_df[
    filtered_df["Age"].between(
        age_range[0],
        age_range[1]
    )
]


# ============================================================
# HANDLE EMPTY FILTER RESULT
# ============================================================

if filtered_df.empty:

    st.error(
        "⚠️ No respondents match the selected filters."
    )

    st.info(
        "Try changing the filters in the sidebar."
    )

    st.stop()


# ============================================================
# MAIN HERO
# ============================================================
st.html("""
<div style="
    padding:35px;
    border-radius:25px;
    margin-bottom:25px;
    background:linear-gradient(135deg,#7c3aed,#2563eb,#06b6d4);
    box-shadow:0 20px 50px rgba(0,0,0,0.35);
    border:1px solid rgba(255,255,255,0.15);
">
    <div style="
        color:white;
        font-size:42px;
        font-weight:800;
        margin-bottom:8px;
    ">
        🧠 MindScope
    </div>

    <div style="
        color:white;
        font-size:19px;
        font-weight:600;
        margin-bottom:10px;
    ">
        Exploring Mental Health in the Technology Workplace
    </div>

    <div style="
        color:rgba(255,255,255,0.88);
        font-size:14px;
        line-height:1.7;
    ">
        An interactive journey through treatment,
        workplace experiences, support systems,
        attitudes and geographic patterns.
    </div>
</div>
""")


# ============================================================
# FILTER STATUS
# ============================================================

st.info(
    f"🔎 Showing *{len(filtered_df):,}* respondents "
    f"out of *{len(df):,}* total respondents based on your filters."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_respondents = len(filtered_df)

countries = filtered_df[
    "Country"
].nunique()

average_age = filtered_df[
    "Age"
].mean()

treatment_rate = (
    filtered_df["treatment"]
    .eq("Yes")
    .mean() * 100
)


# ============================================================
# KPI CARDS
# ============================================================
st.markdown(
    '<div class="section-title">📊 At a Glance</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.html(f"""
    <div style="
        padding:22px;
        min-height:120px;
        border-radius:20px;
        background:linear-gradient(145deg,#1e293b,#0f172a);
        border:1px solid rgba(139,92,246,0.35);
        box-shadow:0 10px 30px rgba(0,0,0,0.25);
    ">
        <div style="font-size:28px;">👥</div>
        <div style="color:#94a3b8;font-size:13px;font-weight:600;">
            RESPONDENTS
        </div>
        <div style="color:white;font-size:30px;font-weight:800;">
            {total_respondents:,}
        </div>
    </div>
    """)

with k2:
    st.html(f"""
    <div style="
        padding:22px;
        min-height:120px;
        border-radius:20px;
        background:linear-gradient(145deg,#1e293b,#0f172a);
        border:1px solid rgba(34,211,238,0.35);
        box-shadow:0 10px 30px rgba(0,0,0,0.25);
    ">
        <div style="font-size:28px;">🌍</div>
        <div style="color:#94a3b8;font-size:13px;font-weight:600;">
            COUNTRIES
        </div>
        <div style="color:white;font-size:30px;font-weight:800;">
            {countries:,}
        </div>
    </div>
    """)

with k3:
    st.html(f"""
    <div style="
        padding:22px;
        min-height:120px;
        border-radius:20px;
        background:linear-gradient(145deg,#1e293b,#0f172a);
        border:1px solid rgba(244,114,182,0.35);
        box-shadow:0 10px 30px rgba(0,0,0,0.25);
    ">
        <div style="font-size:28px;">🎂</div>
        <div style="color:#94a3b8;font-size:13px;font-weight:600;">
            AVERAGE AGE
        </div>
        <div style="color:white;font-size:30px;font-weight:800;">
            {average_age:.1f}
        </div>
    </div>
    """)

with k4:
    st.html(f"""
    <div style="
        padding:22px;
        min-height:120px;
        border-radius:20px;
        background:linear-gradient(145deg,#1e293b,#0f172a);
        border:1px solid rgba(249,115,22,0.35);
        box-shadow:0 10px 30px rgba(0,0,0,0.25);
    ">
        <div style="font-size:28px;">💙</div>
        <div style="color:#94a3b8;font-size:13px;font-weight:600;">
            TREATMENT RATE
        </div>
        <div style="color:white;font-size:30px;font-weight:800;">
            {treatment_rate:.1f}%
        </div>
    </div>
    """)


# ============================================================
# DASHBOARD TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏠 Overview",
        "🧠 Mental Health",
        "💼 Workplace",
        "🌍 Geography",
        "🔬 Deep Dive"
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">✨ Survey Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Treatment
    # --------------------------------------------------------

    with col1:

        treatment_counts = (
            filtered_df["treatment"]
            .value_counts()
            .reset_index()
        )

        treatment_counts.columns = [
            "Treatment",
            "Count"
        ]

        fig = px.pie(
            treatment_counts,
            names="Treatment",
            values="Count",
            hole=0.58,
            title="🧠 Mental Health Treatment",
            color_discrete_sequence=[
                "#8b5cf6",
                "#22d3ee",
                "#f472b6"
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            height=430,
            legend_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Age Distribution
    # --------------------------------------------------------

    with col2:

        fig = px.histogram(
            filtered_df,
            x="Age",
            nbins=20,
            marginal="box",
            title="🎂 Age Distribution",
            color_discrete_sequence=[
                "#38bdf8"
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            height=430,
            xaxis_title="Age",
            yaxis_title="Respondents"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Gender
    # --------------------------------------------------------

    gender_counts = (
        filtered_df["Gender"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    gender_counts.columns = [
        "Gender",
        "Count"
    ]

    fig = px.bar(
        gender_counts,
        x="Count",
        y="Gender",
        orientation="h",
        title="👤 Respondents by Gender",
        color="Count",
        color_continuous_scale="Turbo"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TAB 2 — MENTAL HEALTH
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">🧠 Mental Health Patterns</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Family History
    # --------------------------------------------------------

    with col1:

        family_counts = (
            filtered_df["family_history"]
            .value_counts()
            .reset_index()
        )

        family_counts.columns = [
            "Family History",
            "Count"
        ]

        fig = px.bar(
            family_counts,
            x="Family History",
            y="Count",
            title="👨‍👩‍👧 Family History",
            color="Count",
            color_continuous_scale="Plasma"
        )

        fig.update_layout(
            template="plotly_dark",
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Work Interference
    # --------------------------------------------------------

    with col2:

        work_counts = (
            filtered_df["work_interfere"]
            .value_counts()
            .reset_index()
        )

        work_counts.columns = [
            "Work Interference",
            "Count"
        ]

        fig = px.bar(
            work_counts,
            x="Work Interference",
            y="Count",
            title="💼 Mental Health & Work Interference",
            color="Count",
            color_continuous_scale="Viridis"
        )

        fig.update_layout(
            template="plotly_dark",
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Family History vs Treatment
    # --------------------------------------------------------

    family_treatment = pd.crosstab(
        filtered_df["family_history"],
        filtered_df["treatment"],
        normalize="index"
    ) * 100

    family_treatment = (
        family_treatment
        .reset_index()
        .melt(
            id_vars="family_history",
            var_name="Treatment",
            value_name="Percentage"
        )
    )

    fig = px.bar(
        family_treatment,
        x="family_history",
        y="Percentage",
        color="Treatment",
        barmode="group",
        title="🔎 Treatment Distribution by Family History",
        labels={
            "family_history": "Family History",
            "Percentage": "Percentage (%)"
        },
        color_discrete_sequence=[
            "#a78bfa",
            "#22d3ee"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        height=470
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Mental vs Physical
    # --------------------------------------------------------

    mental_physical = (
        filtered_df["mental_vs_physical"]
        .value_counts()
        .reset_index()
    )

    mental_physical.columns = [
        "Response",
        "Count"
    ]

    fig = px.bar(
        mental_physical,
        x="Response",
        y="Count",
        title="⚖️ Mental Health vs Physical Health",
        color="Count",
        color_continuous_scale="RdPu"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TAB 3 — WORKPLACE
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">💼 Workplace Experience</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Remote Work
    # --------------------------------------------------------

    with col1:

        remote_counts = (
            filtered_df["remote_work"]
            .value_counts()
            .reset_index()
        )

        remote_counts.columns = [
            "Remote Work",
            "Count"
        ]

        fig = px.pie(
            remote_counts,
            names="Remote Work",
            values="Count",
            hole=0.55,
            title="🏠 Remote Work",
            color_discrete_sequence=[
                "#06b6d4",
                "#f97316"
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Tech Company
    # --------------------------------------------------------

    with col2:

        tech_counts = (
            filtered_df["tech_company"]
            .value_counts()
            .reset_index()
        )

        tech_counts.columns = [
            "Tech Company",
            "Count"
        ]

        fig = px.bar(
            tech_counts,
            x="Tech Company",
            y="Count",
            title="💻 Technology Company",
            color="Count",
            color_continuous_scale="Tealgrn"
        )

        fig.update_layout(
            template="plotly_dark",
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Benefits vs Treatment
    # --------------------------------------------------------

    benefits_table = pd.crosstab(
        filtered_df["benefits"],
        filtered_df["treatment"],
        normalize="index"
    ) * 100

    benefits_table = (
        benefits_table
        .reset_index()
        .melt(
            id_vars="benefits",
            var_name="Treatment",
            value_name="Percentage"
        )
    )

    fig = px.bar(
        benefits_table,
        x="benefits",
        y="Percentage",
        color="Treatment",
        barmode="group",
        title="🎁 Mental Health Benefits & Treatment",
        labels={
            "benefits": "Benefits",
            "Percentage": "Percentage (%)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=480
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Company Size vs Treatment
    # --------------------------------------------------------

    company_table = pd.crosstab(
        filtered_df["no_employees"],
        filtered_df["treatment"],
        normalize="index"
    ) * 100

    company_table = (
        company_table
        .reset_index()
        .melt(
            id_vars="no_employees",
            var_name="Treatment",
            value_name="Percentage"
        )
    )

    fig = px.bar(
        company_table,
        x="no_employees",
        y="Percentage",
        color="Treatment",
        barmode="group",
        title="🏢 Company Size & Treatment",
        labels={
            "no_employees": "Company Size",
            "Percentage": "Percentage (%)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_tickangle=-35
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TAB 4 — GEOGRAPHY
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">🌍 Geographic Exploration</div>',
        unsafe_allow_html=True
    )

    country_summary = (
        filtered_df
        .groupby("Country")
        .agg(
            Respondents=("Country", "size"),
            Treatment_Rate=(
                "treatment",
                lambda x:
                (x == "Yes").mean() * 100
            )
        )
        .reset_index()
    )

    min_country_count = st.slider(
        "Minimum respondents required for country comparison",
        min_value=1,
        max_value=30,
        value=5
    )

    country_map = country_summary[
        country_summary["Respondents"]
        >= min_country_count
    ].copy()

    if not country_map.empty:

        fig = px.choropleth(
            country_map,
            locations="Country",
            locationmode="country names",
            color="Treatment_Rate",
            hover_name="Country",
            hover_data={
                "Respondents": True,
                "Treatment_Rate": ":.1f"
            },
            color_continuous_scale="Turbo",
            title="🌎 Treatment Rate Across Countries"
        )

        fig.update_layout(
            template="plotly_dark",
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                bgcolor="rgba(0,0,0,0)"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "Not enough data for the selected threshold."
        )

    # --------------------------------------------------------
    # Top Countries
    # --------------------------------------------------------

    top_countries = (
        country_summary
        .sort_values(
            "Respondents",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        top_countries,
        x="Respondents",
        y="Country",
        orientation="h",
        color="Treatment_Rate",
        color_continuous_scale="Turbo",
        title="🌍 Countries With the Most Respondents",
        hover_data=[
            "Treatment_Rate"
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Country Table
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Country Summary</div>',
        unsafe_allow_html=True
    )

    country_display = (
        country_summary
        .sort_values(
            "Respondents",
            ascending=False
        )
        .copy()
    )

    country_display["Treatment_Rate"] = (
        country_display["Treatment_Rate"]
        .round(1)
    )

    st.dataframe(
        country_display,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 5 — DEEP DIVE
# ============================================================

with tab5:

    st.markdown(
        '<div class="section-title">🔬 Deeper Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">

        <h3>🔎 What is association analysis?</h3>

        Cramér's V measures the strength of association
        between two categorical variables.

        <br><br>

        <b>Important:</b> Association does not establish
        causation.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # Predictor Variables
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Cramer's V
    # --------------------------------------------------------

    def cramers_v(x, y):

        table = pd.crosstab(
            x,
            y
        )

        if (
            table.shape[0] < 2 or
            table.shape[1] < 2
        ):
            return np.nan

        observed = table.values

        total = observed.sum()

        if total == 0:
            return np.nan

        row_totals = observed.sum(
            axis=1
        )

        col_totals = observed.sum(
            axis=0
        )

        expected = np.outer(
            row_totals,
            col_totals
        ) / total

        expected = np.where(
            expected == 0,
            1e-10,
            expected
        )

        chi_square = (
            (observed - expected) ** 2
            / expected
        ).sum()

        n = observed.sum()

        if n <= 1:
            return np.nan

        phi2 = chi_square / n

        rows, cols = observed.shape

        phi2_corrected = max(
            0,
            phi2 -
            (
                (cols - 1) *
                (rows - 1)
            ) / (n - 1)
        )

        rows_corrected = (
            rows -
            ((rows - 1) ** 2) /
            (n - 1)
        )

        cols_corrected = (
            cols -
            ((cols - 1) ** 2) /
            (n - 1)
        )

        denominator = min(
            cols_corrected - 1,
            rows_corrected - 1
        )

        if denominator <= 0:
            return np.nan

        return np.sqrt(
            phi2_corrected /
            denominator
        )

    # --------------------------------------------------------
    # Calculate associations
    # --------------------------------------------------------

    association_results = []

    for column in predictor_columns:

        value = cramers_v(
            filtered_df[column],
            filtered_df["treatment"]
        )

        association_results.append(
            {
                "Variable": column,
                "Cramers_V": value
            }
        )

    association_df = pd.DataFrame(
        association_results
    ).dropna()

    association_df = (
        association_df
        .sort_values(
            "Cramers_V",
            ascending=False
        )
    )

    # --------------------------------------------------------
    # Association Chart
    # --------------------------------------------------------

    top_associations = (
        association_df
        .head(12)
        .sort_values(
            "Cramers_V",
            ascending=True
        )
    )

    fig = px.bar(
        top_associations,
        x="Cramers_V",
        y="Variable",
        orientation="h",
        color="Cramers_V",
        color_continuous_scale="Turbo",
        title="📈 Variables Associated With Treatment"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_title="Cramér's V",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Association Table
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Association Table</div>',
        unsafe_allow_html=True
    )

    association_display = (
        association_df.copy()
    )

    association_display[
        "Cramers_V"
    ] = (
        association_display[
            "Cramers_V"
        ].round(3)
    )

    st.dataframe(
        association_display,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DATA EXPLORER
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🔎 Explore the Data</div>',
    unsafe_allow_html=True
)

with st.expander(
    "Open interactive respondent-level data"
):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=450
    )


# ============================================================
# DOWNLOAD SECTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📥 Download</div>',
    unsafe_allow_html=True
)

download_col1, download_col2 = st.columns(2)


with download_col1:

    csv_data = (
        filtered_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📥 Download Filtered Dataset",
        data=csv_data,
        file_name="filtered_mental_health_data.csv",
        mime="text/csv",
        use_container_width=True
    )


with download_col2:

    association_csv = (
        association_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📊 Download Association Analysis",
        data=association_csv,
        file_name="treatment_association_analysis.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <div style="font-size:25px;">
            🧠 ✨ 📊 🌍
        </div>

        <b>MindScope — Mental Health in Tech</b>

        <br>

        Interactive Exploratory Data Analysis Dashboard

        <br><br>

        Built with Python • Pandas • Plotly • Streamlit

    </div>
    """,
    unsafe_allow_html=True
)