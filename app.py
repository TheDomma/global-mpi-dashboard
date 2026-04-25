import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Global MPI Dashboard", page_icon="🌍", layout="wide")

# --- Title and Introduction ---
st.markdown("<h1 style='text-align: center;'>🌍 Global Multidimensional Poverty Index (MPI)</h1>", unsafe_allow_html=True)
st.image("2.png", use_container_width=True)
st.markdown("""
<p font-size: 18px;'>
<strong>Understanding global poverty patterns and identifying high-risk regions and drivers.</strong><br>
Designed for the Global Conference on Sustainability to provide policymakers and finance professionals with actionable insights.<br>
<em>Aligns with UN Sustainable Development Goal (SDG) 1: End poverty in all its forms everywhere.</em>
</p>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_global_mpi.csv')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🎛️ Dashboard Filters")

# Filter 1: Country Selection
country_list = ['All'] + sorted(df['Country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", country_list, help="Isolate data for a specific nation.")

if selected_country != 'All':
    filtered_df = df[df['Country'] == selected_country]
else:
    filtered_df = df.copy()

# Filter 2: Deprivation Slider
st.sidebar.markdown("### 🎚️ Advanced Filters")
min_intensity = float(df['Intensity of Deprivation'].min())
max_intensity = float(df['Intensity of Deprivation'].max())
selected_intensity = st.sidebar.slider(
    "Minimum Intensity of Deprivation (%)", 
    min_value=min_intensity, 
    max_value=max_intensity, 
    value=min_intensity,
    help="Filter out regions to focus only on extreme poverty intensity."
)

filtered_df = filtered_df[filtered_df['Intensity of Deprivation'] >= selected_intensity]

# Filter 3: Top N Selector
st.sidebar.markdown("### 📊 Chart Settings")
top_n = st.sidebar.slider("Top N Regions to Display", min_value=5, max_value=50, value=10, step=5, help="Change how many regions appear in the Bar Chart.")

st.sidebar.divider()
st.sidebar.info("Developed for the 5DATA004C Data Science Project Lifecycle coursework.")

# --- SECTION 1: Overview (Top KPIs) ---
st.subheader("🥇 High-Level Overview")
col1, col2, col3, col4 = st.columns(4)

total_regions = len(filtered_df)
avg_mpi = filtered_df['MPI'].mean() if not filtered_df.empty else 0
avg_severe = filtered_df['In Severe Poverty'].mean() if not filtered_df.empty else 0
avg_vuln = filtered_df['Vulnerable to Poverty'].mean() if not filtered_df.empty else 0

col1.metric("Total Regions Selected", f"{total_regions}")
col2.metric("Average MPI", f"{avg_mpi:.4f}")
col3.metric("Avg Severe Poverty", f"{avg_severe:.1f}%")
col4.metric("Avg Vulnerability", f"{avg_vuln:.1f}%")

st.divider()

# --- SECTION 2: Automated Insights Panel ---
st.subheader("💡 Policymaker Insights")
if not filtered_df.empty:
    worst_region = filtered_df.loc[filtered_df['MPI'].idxmax()]
    best_region = filtered_df.loc[filtered_df['MPI'].idxmin()]
    
    st.error(f"🔴 **Highest Risk:** **{worst_region['Admin 1 Name']}** ({worst_region['Country']}) has the highest extreme poverty risk with an MPI of **{worst_region['MPI']:.4f}**.")
    st.success(f"🟢 **Lowest Risk:** **{best_region['Admin 1 Name']}** ({best_region['Country']}) reports the lowest acute poverty metrics in this selection.")
else:
    st.warning("Adjust your filters to generate insights.")

st.divider()

# --- SECTION 3: Visualizations & Analysis ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Regional Breakdown", "🗺️ Global Heatmap", "📈 Scatter Plot", "🌡️ Driver Correlation", "🗄️ Raw Data"])

with tab1:
    st.subheader(f"Top {top_n} Most Deprived Regions")
    if not filtered_df.empty:
        top_regions = filtered_df.nlargest(top_n, 'MPI')
        fig_bar = px.bar(
            top_regions, 
            x='Admin 1 Name', 
            y='MPI', 
            color='Country',
            title=f'Highest MPI Regions (Top {top_n})',
            labels={'Admin 1 Name': 'Region', 'MPI': 'MPI Value'}
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")
    else:
        st.warning("No data available.")

with tab2:
    st.subheader("Geospatial Poverty Distribution")
    if not filtered_df.empty:
        map_data = filtered_df.groupby(['Country ISO3', 'Country'], as_index=False)['MPI'].mean()
        fig_map = px.choropleth(
            map_data,
            locations="Country ISO3",
            color="MPI",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Reds, 
            title="Average MPI by Country"
        )
        fig_map.update_geos(projection_type="natural earth", showcoastlines=True)
        fig_map.update_traces(hovertemplate='<b>%{hovertext}</b><br>Average MPI: %{z:.3f}')
        st.plotly_chart(fig_map, use_container_width=True, key="map_chart")
    else:
        st.warning("No data available.")

with tab3:
    st.subheader("Severe Poverty vs Vulnerability")
    if not filtered_df.empty:
        fig_scatter = px.scatter(
            filtered_df,
            x='Vulnerable to Poverty',
            y='In Severe Poverty',
            color='Country', # Now colored by full name
            hover_name='Admin 1 Name',
            title='Vulnerability vs Severe Poverty Percentages'
        )
        st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_chart")
    else:
        st.warning("No data available for these filter parameters.")

with tab4:
    st.subheader("Poverty Driver Correlation")
    st.markdown("Understand how different aspects of poverty (Vulnerability vs. Severe Poverty) interact.")
    if len(filtered_df) > 1:
        # Correlation Heatmap
        numeric_cols = ['MPI', 'Headcount Ratio', 'Intensity of Deprivation', 'Vulnerable to Poverty', 'In Severe Poverty']
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig_corr = px.imshow(
            corr_matrix, 
            text_auto=".2f", 
            aspect="auto", 
            color_continuous_scale='RdBu_r', 
            title="Statistical Correlation of Poverty Metrics"
        )
        st.plotly_chart(fig_corr, use_container_width=True, key="heatmap")
    else:
        st.warning("Not enough data to calculate correlations. Please select 'All' countries or adjust sliders.")

with tab5:
    st.subheader("Sortable Database")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.markdown("### Export Tools")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data for Excel",
        data=csv,
        file_name='policymaker_mpi_data.csv',
        mime='text/csv'
    )