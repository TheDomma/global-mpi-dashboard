import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Global MPI Dashboard", page_icon="🌍", layout="wide")

# --- Title and Introduction ---
st.title("🌍 Global Multidimensional Poverty Index (MPI) Dashboard")
st.markdown("""
This dashboard explores the Global MPI dataset. The MPI is an international measure of acute multidimensional poverty covering over 100 developing countries.
Use the sidebar to filter the data and explore different metrics.
""")

# --- Data Loading ---
@st.cache_data
def load_data():
    # Load the main dataset
    df = pd.read_csv('global_mpi.csv')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Filter by Country
country_list = ['All'] + sorted(df['Country ISO3'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country (ISO3)", country_list)

# Apply filters
if selected_country != 'All':
    filtered_df = df[df['Country ISO3'] == selected_country]
else:
    filtered_df = df.copy()

# --- Key Metrics ---
st.header("Overview Metrics")
col1, col2, col3 = st.columns(3)

avg_mpi = filtered_df['MPI'].mean()
avg_headcount = filtered_df['Headcount Ratio'].mean()
avg_intensity = filtered_df['Intensity of Deprivation'].mean()

col1.metric("Average MPI", f"{avg_mpi:.4f}")
col2.metric("Avg Headcount Ratio", f"{avg_headcount:.2f}%")
col3.metric("Avg Intensity of Deprivation", f"{avg_intensity:.2f}%")

# --- Visualizations ---
st.header("Data Explorations")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 Regions by MPI")
    # Sort by MPI and take top 10
    top_10_mpi = filtered_df.nlargest(10, 'MPI')
    fig_bar = px.bar(
        top_10_mpi, 
        x='Admin 1 Name', 
        y='MPI', 
        color='Country ISO3',
        title='Highest MPI Regions',
        labels={'Admin 1 Name': 'Region', 'MPI': 'MPI Value'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Severe Poverty vs Vulnerability")
    fig_scatter = px.scatter(
        filtered_df,
        x='Vulnerable to Poverty',
        y='In Severe Poverty',
        color='Country ISO3',
        hover_name='Admin 1 Name',
        title='Vulnerability vs Severe Poverty Percentages'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Raw Data Table ---
st.header("Raw Data")
if st.checkbox("Show Raw Dataset"):
    st.dataframe(filtered_df)