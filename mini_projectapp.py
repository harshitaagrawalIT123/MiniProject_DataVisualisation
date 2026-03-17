import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Farm Dashboard", layout="wide")

# --- BACKGROUND IMAGE ---
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef");
    background-size: cover;
    background-attachment: fixed;
}
.block-container {
    background-color: rgba(255,255,255,0.85);
    padding: 2rem;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("🌾 Chhattisgarh Farm Success Dashboard")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_excel("products_cleaned.xlsx")

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎 Filters")

state_filter = st.sidebar.multiselect("State", sorted(df["state"].unique()))
crop_filter = st.sidebar.multiselect("Crop Category", sorted(df["crop_category"].unique()))
owner_filter = st.sidebar.multiselect("Ownership", sorted(df["owner"].unique()))
process_filter = st.sidebar.multiselect("Processing", sorted(df["processing_type"].unique()))

# --- APPLY FILTERS ---
filtered_df = df.copy()

if state_filter:
    filtered_df = filtered_df[filtered_df["state"].isin(state_filter)]
if crop_filter:
    filtered_df = filtered_df[filtered_df["crop_category"].isin(crop_filter)]
if owner_filter:
    filtered_df = filtered_df[filtered_df["owner"].isin(owner_filter)]
if process_filter:
    filtered_df = filtered_df[filtered_df["processing_type"].isin(process_filter)]

# --- TOP METRIC ---
st.metric("Total Cases", len(filtered_df))

# =======================
# 📊 ROW 1: PIE + BAR
# =======================
col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(filtered_df, names="crop_category", title="Crop Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    fig_bar = px.bar(
        filtered_df["processing_type"].value_counts().reset_index(),
        x="count",
        y="processing_type",
        orientation="h",
        title="Processing Methods"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# =======================
# 🌳 ROW 2: SUNBURST
# =======================
st.subheader("🌳 Hierarchy View")

fig_sunburst = px.sunburst(
    filtered_df,
    path=["crop_category", "owner", "state"]
)

st.plotly_chart(fig_sunburst, use_container_width=True)

# =======================
# 🗺️ ROW 3: INDIA MAP
# =======================
st.subheader("🗺️ Location Map")

# If lat-long not present, skip
if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:
    fig_map = px.scatter_geo(
        filtered_df,
        lat="latitude",
        lon="longitude",
        hover_name="name"
    )

    fig_map.update_geos(
        scope="asia",
        center={"lat": 22, "lon": 80},
        projection_scale=4
    )

    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("Latitude/Longitude not found in dataset")

# =======================
# 📈 ROW 4: TIMELINE + FUNDING
# =======================
st.subheader("📈 Project Plan")

timeline_df = pd.DataFrame({
    "Phase": ["Phase 1", "Phase 2", "Phase 3"],
    "Year": [2026, 2027, 2028],
    "Funding": [100, 200, 50]
})

col3, col4 = st.columns(2)

with col3:
    fig_timeline = px.scatter(
        timeline_df,
        x="Year",
        y="Phase",
        size="Funding",
        color="Phase",
        title="Timeline"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

with col4:
    fig_funding = px.pie(
        timeline_df,
        names="Phase",
        values="Funding",
        title="Funding Distribution"
    )
    st.plotly_chart(fig_funding, use_container_width=True)

# =======================
# 📚 RESULTS SECTION
# =======================
st.subheader("💡 Success Stories")

if len(filtered_df) > 0:
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['name']} ({row['state']})"):
            st.write(f"**Crop:** {row['crops']}")
            st.write(f"**Key Learning:** {row['key_learning']}")
            st.write(f"**Innovation:** {row['innovation_and_practice_uses']}")
            st.info(f"**Applicability:** {row['applicability_in_chhattisgarh']}")
else:
    st.warning("No data found")