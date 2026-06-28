import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- Page Config ----------
st.set_page_config(
    page_title="India Data Job Market Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Load Data ----------
@st.cache_data
def load_data():
    df = pd.read_csv("jobs_final_cleaned.csv")
    return df

df = load_data()
skill_columns = [col for col in df.columns if col.startswith("skill_")]
skill_display_names = [col.replace("skill_", "").replace("_", " ").title() for col in skill_columns]
skill_map = dict(zip(skill_display_names, skill_columns))

# ---------- Header ----------
st.title("📊 India Data Job Market Explorer")
st.caption("Live analysis of 480+ real job postings across 20 Indian cities, powered by the Adzuna Jobs API")

st.divider()

# ---------- Sidebar Filters ----------
st.sidebar.header("🔍 Filters")

selected_cities = st.sidebar.multiselect(
    "Select Cities",
    options=sorted(df["search_city"].str.title().unique()),
    default=sorted(df["search_city"].str.title().unique())
)

selected_skills_display = st.sidebar.multiselect(
    "Select Skills to Compare",
    options=skill_display_names,
    default=["Python", "Sql", "Machine Learning", "Excel"]
)
selected_skills = [skill_map[s] for s in selected_skills_display]

role_filter = st.sidebar.radio(
    "Role Type",
    options=["All Roles", "Data Analyst", "Data Scientist"],
    index=0
)

# ---------- Apply Filters ----------
filtered_df = df[df["search_city"].str.title().isin(selected_cities)]

# ---------- Empty Filter Safety Check ----------
if filtered_df.empty:
    st.warning("⚠️ No jobs match your current filters. Please select at least one city.")
    st.stop()

if role_filter == "Data Analyst":
    filtered_df = filtered_df[filtered_df["search_title"] == "data analyst"]
elif role_filter == "Data Scientist":
    filtered_df = filtered_df[filtered_df["search_title"] == "data scientist"]

# ---------- Key Metrics Row ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs", len(filtered_df))
col2.metric("Cities Covered", filtered_df["search_city"].nunique())
col3.metric("With Salary Info", filtered_df["salary_max"].notna().sum())
if filtered_df["salary_max"].notna().sum() > 0:
    avg_sal = filtered_df["salary_max"].dropna().mean()
    col4.metric("Avg Max Salary", f"₹{avg_sal/100000:.1f}L")
else:
    col4.metric("Avg Max Salary", "N/A")

st.divider()

# ---------- Smart Insight (auto-generated text) ----------
if len(filtered_df) > 0:
    skill_totals_pct = (filtered_df[skill_columns].mean() * 100).sort_values(ascending=False)
    top_skill_name = skill_totals_pct.index[0].replace("skill_", "").replace("_", " ").title()
    top_skill_pct = skill_totals_pct.iloc[0]

    top_city = filtered_df["search_city"].str.title().value_counts().idxmax()
    top_city_count = filtered_df["search_city"].str.title().value_counts().max()

    st.markdown(f"""
    <div style="background-color:#1A1F2B; padding:20px; border-radius:12px; border-left: 4px solid #00D9C0;">
    <h4 style="color:#00D9C0; margin-top:0;">💡 Smart Insight</h4>
    <p style="font-size:16px; color:#FAFAFA;">
    Based on current filters, <b>{top_skill_name}</b> is the most in-demand skill, 
    appearing in <b>{top_skill_pct:.0f}%</b> of matching job postings. 
    <b>{top_city}</b> leads with the highest number of openings ({top_city_count} jobs).
    </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")  # chhota spacing

# ---------- Charts Section ----------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("🎯 Skill Demand (Selected Skills)")
    if selected_skills:
        skill_pct = (filtered_df[selected_skills].mean() * 100).sort_values(ascending=False)
        skill_pct.index = [s.replace("skill_", "").replace("_", " ").title() for s in skill_pct.index]

        fig1 = px.bar(
            x=skill_pct.values,
            y=skill_pct.index,
            orientation="h",
            color=skill_pct.index,
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"x": "% of Jobs", "y": ""}
        )
        fig1.update_layout(
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="#FAFAFA",
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Select at least one skill from the sidebar.")

with chart_col2:
    st.subheader("🏙️ Jobs by City")
    city_counts = filtered_df["search_city"].str.title().value_counts().head(10)

    fig2 = px.bar(
        x=city_counts.index,
        y=city_counts.values,
        color=city_counts.index,
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"x": "", "y": "Number of Jobs"}
    )
    fig2.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="#FAFAFA",
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------- City vs Skill Heatmap ----------
st.subheader("🔥 City vs Skill Heatmap")
if selected_skills:
    # Sirf wahi cities rakho jisme kam se kam 15 jobs hain (reliable %)
    city_job_counts = filtered_df["search_city"].str.title().value_counts()
    reliable_cities = city_job_counts[city_job_counts >= 15].index

    heatmap_df = filtered_df[filtered_df["search_city"].str.title().isin(reliable_cities)]
    heatmap_data = heatmap_df.groupby(heatmap_df["search_city"].str.title())[selected_skills].mean() * 100
    heatmap_data.columns = [s.replace("skill_", "").replace("_", " ").title() for s in heatmap_data.columns]

    fig3 = px.imshow(
        heatmap_data,
        color_continuous_scale="Viridis",
        labels=dict(x="Skill", y="City", color="% Demand"),
        aspect="auto",
        text_auto=".0f"
    )
    fig3.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="#FAFAFA",
        height=500,
        xaxis_tickangle=-30
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Select at least one skill from the sidebar to see the heatmap.")