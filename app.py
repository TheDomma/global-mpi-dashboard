import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Global MPI Dashboard", page_icon="🌍", layout="wide")

# --- Title and Introduction ---
st.title("🌍 Global Multidimensional Poverty Index (MPI) Dashboard")
st.markdown("""
Explore the Global MPI dataset, an international measure of acute multidimensional poverty covering over 100 developing countries.
Use the sidebar to filter specific countries and explore the regional disparities.
""")

# --- Data Loading ---
@st.cache_data
def load_data():
    # Load the CLEANED dataset from your Jupyter Notebook output
    df = pd.read_csv('cleaned_global_mpi.csv')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")

# Filter by Country
country_list = ['All'] + sorted(df['Country ISO3'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country (ISO3)", country_list)

# Apply filters
if selected_country != 'All':
    filtered_df = df[df['Country ISO3'] == selected_country]
else:
    filtered_df = df.copy()

# --- Key Metrics ---
st.header("Key Poverty Metrics")
col1, col2, col3 = st.columns(3)

# Calculate metrics safely
avg_mpi = filtered_df['MPI'].mean() if not filtered_df.empty else 0
avg_headcount = filtered_df['Headcount Ratio'].mean() if not filtered_df.empty else 0
avg_intensity = filtered_df['Intensity of Deprivation'].mean() if not filtered_df.empty else 0

col1.metric("Average MPI", f"{avg_mpi:.4f}")
col2.metric("Avg Headcount Ratio", f"{avg_headcount:.2f}%")
col3.metric("Avg Intensity of Deprivation", f"{avg_intensity:.2f}%")

st.divider()

# --- Tabs for Visualizations ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Regional Analysis", "📈 Poverty Correlation", "🗺️ Global Map", "🗄️ Raw Data"])

with tab1:
    st.subheader("Top 10 Regions by MPI")
    if not filtered_df.empty:
        # Sort by MPI and take top 10
        top_10_mpi = filtered_df.nlargest(10, 'MPI')
        fig_bar = px.bar(
            top_10_mpi, 
            x='Admin 1 Name', 
            y='MPI', 
            color='Country ISO3',
            title='Highest MPI Regions in Selection',
            labels={'Admin 1 Name': 'Region', 'MPI': 'MPI Value'}
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")
    else:
        st.warning("No data available for this selection.")

with tab2:
    st.subheader("Severe Poverty vs Vulnerability")
    if not filtered_df.empty:
        fig_scatter = px.scatter(
            filtered_df,
            x='Vulnerable to Poverty',
            y='In Severe Poverty',
            color='Country ISO3',
            hover_name='Admin 1 Name',
            title='Vulnerability vs Severe Poverty Percentages'
        )
        st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_chart")
    else:
        st.warning("No data available for this selection.")

with tab3:
    st.subheader("Global MPI Distribution")
    if not filtered_df.empty:
        # Calculate the average MPI per country for the map
        map_data = filtered_df.groupby('Country ISO3', as_index=False)['MPI'].mean()
        
        # Create the choropleth map
        fig_map = px.choropleth(
            map_data,
            locations="Country ISO3",
            color="MPI",
            hover_name="Country ISO3",
            color_continuous_scale=px.colors.sequential.YlOrRd, 
            title="Average MPI by Country (Hover for details)"
        )
        fig_map.update_geos(projection_type="natural earth", showcoastlines=True)
        st.plotly_chart(fig_map, use_container_width=True, key="map_chart")
    else:
        st.warning("No data available for this selection.")

with tab4:
    st.subheader("Cleaned Dataset Viewer")
    st.dataframe(filtered_df, use_container_width=True)