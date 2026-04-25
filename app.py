import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(page_title="Global MPI Dashboard", page_icon="🌍", layout="wide")

# --- Title and Introduction ---
st.markdown("<h1 style='text-align: center;'>Global Multidimensional Poverty Index (MPI)</h1>", unsafe_allow_html=True)
st.image("2.png", use_container_width=True)
st.markdown("""
<p font-size: 18px;'>
<strong>Understanding global poverty patterns and identifying high-risk regions and drivers.</strong><br>
Designed for the Global Conference on Sustainability to provide policymakers and finance professionals with actionable insights.<br>
<em>Aligns with UN Sustainable Development Goal (SDG) 1: End poverty in all its forms everywhere.</em>
</p>
""", unsafe_allow_html=True)

# --- Data Loading & Preprocessing ---
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_global_mpi.csv')
    df['Poverty Risk Level'] = df['MPI'].apply(
        lambda x: 'Extreme' if x > 0.4 else ('High' if x > 0.2 else 'Moderate')
    )
    return df

df = load_data()

# ==========================================
# SIDEBAR: THE ULTIMATE CONTROL PANEL
# ==========================================
st.sidebar.subheader("🔻 Filters")

# 1. Country Filter
country_list = ['All'] + sorted(df['Country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", country_list, key="country_select")

# 2. Dynamic Region Filter
if selected_country != 'All':
    region_options = ['All'] + sorted(df[df['Country'] == selected_country]['Admin 1 Name'].dropna().unique().tolist())
else:
    region_options = ['All'] + sorted(df['Admin 1 Name'].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", region_options, key="region_select")

# 3. Poverty Category Multiselect
category = st.sidebar.multiselect(
    "Poverty Risk Level",
    ["Extreme", "High", "Moderate"],
    default=["Extreme", "High", "Moderate"],
    help="Filter by the severity classification of the MPI.",
    key="risk_category"
)

# --- Analysis Settings ---
st.sidebar.subheader("📊 Analysis Settings")

# 4. Core Metric Selector
selected_metric = st.sidebar.selectbox(
    "Select Key Metric",
    ["MPI", "Headcount Ratio", "Intensity of Deprivation", "Vulnerable to Poverty", "In Severe Poverty"],
    key="core_metric"
)

# 5. Top N Selector
top_n = st.sidebar.slider("Top N Regions to Display", 5, 50, 10, 5, key="top_n_slider")

# --- Advanced Thresholds ---
st.sidebar.subheader("⚙️ Advanced")

# 6. Minimum MPI Threshold
min_mpi = float(df['MPI'].min())
max_mpi = float(df['MPI'].max())
mpi_threshold = st.sidebar.slider("Minimum MPI Threshold", min_value=min_mpi, max_value=max_mpi, value=min_mpi, key="mpi_slider")

# 7. Intensity Threshold
min_intensity = float(df['Intensity of Deprivation'].min())
max_intensity = float(df['Intensity of Deprivation'].max())
selected_intensity = st.sidebar.slider("Minimum Intensity (%)", min_value=min_intensity, max_value=max_intensity, value=min_intensity, key="intensity_slider")

# --- Reset Button ---
def reset_filters():
    st.session_state["country_select"] = "All"
    st.session_state["region_select"] = "All"
    st.session_state["risk_category"] = ["Extreme", "High", "Moderate"]
    st.session_state["core_metric"] = "MPI"
    st.session_state["top_n_slider"] = 10
    st.session_state["mpi_slider"] = float(df['MPI'].min())
    st.session_state["intensity_slider"] = float(df['Intensity of Deprivation'].min())

st.sidebar.button("🔄 Reset All Filters", on_click=reset_filters, use_container_width=True, type="primary")
st.sidebar.divider()
st.sidebar.info("Developed for the 5DATA004C Data Science Project Lifecycle coursework.")

# ==========================================
# APPLY ALL SIDEBAR FILTERS LOGIC
# ==========================================
filtered_df = df.copy()

if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Admin 1 Name'] == selected_region]

filtered_df = filtered_df[filtered_df['Poverty Risk Level'].isin(category)]
filtered_df = filtered_df[filtered_df['MPI'] >= mpi_threshold]
filtered_df = filtered_df[filtered_df['Intensity of Deprivation'] >= selected_intensity]


# ==========================================
# MAIN DASHBOARD RENDER
# ==========================================

# --- SECTION 1: Overview (Top KPIs) ---
st.subheader("High-Level Overview")
col1, col2, col3, col4 = st.columns(4)

total_regions = len(filtered_df)
avg_metric = filtered_df[selected_metric].mean() if not filtered_df.empty else 0
avg_severe = filtered_df['In Severe Poverty'].mean() if not filtered_df.empty else 0
avg_vuln = filtered_df['Vulnerable to Poverty'].mean() if not filtered_df.empty else 0

col1.metric("Total Regions Selected", f"{total_regions}")
col2.metric(f"Avg {selected_metric}", f"{avg_metric:.4f}") # Dynamically reacts to sidebar!
col3.metric("Avg Severe Poverty", f"{avg_severe:.1f}%")
col4.metric("Avg Vulnerability", f"{avg_vuln:.1f}%")

st.divider()

# --- SECTION 2: Dynamic Insights Panel ---
st.subheader("💡 Policymaker Insights") # Clean UI spacing
if not filtered_df.empty:
    
    # 1. Comparative Intelligence
    global_avg = df[selected_metric].mean()
    if avg_metric > global_avg:
        st.warning(f"⚠️ **Global Comparison:** The selected regions are **above** the global average for {selected_metric} ({avg_metric:.4f} vs {global_avg:.4f}).")
    else:
        st.success(f"**Global Comparison:** The selected regions are **below** the global average for {selected_metric} ({avg_metric:.4f} vs {global_avg:.4f}).")
    
    # 2. Extreme Case Explanations
    worst_region = filtered_df.loc[filtered_df[selected_metric].idxmax()]
    best_region = filtered_df.loc[filtered_df[selected_metric].idxmin()]
    
    st.error(f"**Critical High-Risk Region Identified:** **{worst_region['Admin 1 Name']}** ({worst_region['Country']}) has the highest **{selected_metric}** in this selection at **{worst_region[selected_metric]:.4f}**.\n\n"
             f"*Causal Driver Analysis: This is likely driven by an Intensity of Deprivation of {worst_region['Intensity of Deprivation']:.1f}% and {worst_region['In Severe Poverty']:.1f}% of its population in severe poverty.*")
    
    st.success(f"**Lowest Risk:** **{best_region['Admin 1 Name']}** ({best_region['Country']}) reports the lowest **{selected_metric}** at **{best_region[selected_metric]:.4f}**.")
else:
    st.warning("Adjust your filters to generate insights.")

st.divider()

# --- SECTION 3: Visualizations & Analysis ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Regional Breakdown", 
    "Global Heatmap", 
    "Poverty Drivers", 
    "Poverty Segmentation", 
    "Driver Correlation", 
    "Compare Nations",
    "Data Explorer"
])

with tab1:
    st.subheader(f"Top {top_n} Regions by {selected_metric}")
    if not filtered_df.empty:
        top_regions = filtered_df.nlargest(top_n, selected_metric)
        fig_bar = px.bar(
            top_regions, 
            x='Admin 1 Name', 
            y=selected_metric, 
            color='Country',
            title=f'Highest {selected_metric} Regions (Top {top_n})',
            labels={'Admin 1 Name': 'Region'}
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")
        
        st.divider()
        st.subheader(f"Regional Leaderboards: {selected_metric}")
        col_worst, col_best = st.columns(2)
        
        with col_worst:
            st.error("**Top 10 Highest Risk (Worst)**")
            ranked_worst = filtered_df.sort_values(by=selected_metric, ascending=False)
            st.dataframe(ranked_worst[['Country', 'Admin 1 Name', selected_metric]].head(10), use_container_width=True, hide_index=True)
            
        with col_best:
            st.success("**Top 10 Lowest Risk (Best)**")
            ranked_best = filtered_df.sort_values(by=selected_metric, ascending=True)
            st.dataframe(ranked_best[['Country', 'Admin 1 Name', selected_metric]].head(10), use_container_width=True, hide_index=True)
    else:
        st.warning("No data available.")

with tab2:
    st.subheader(f"Geospatial Distribution: {selected_metric}")
    if not filtered_df.empty:
        # Upgraded map with extra hover data
        map_data = filtered_df.groupby(['Country ISO3', 'Country'], as_index=False)[['MPI', 'Headcount Ratio', 'Intensity of Deprivation', 'Vulnerable to Poverty', 'In Severe Poverty']].mean()
        fig_map = px.choropleth(
            map_data,
            locations="Country ISO3",
            color=selected_metric,
            hover_name="Country",
            hover_data=['MPI', 'Headcount Ratio', 'Intensity of Deprivation'],
            color_continuous_scale=px.colors.sequential.Reds, 
            title=f"Average {selected_metric} by Country"
        )
        fig_map.update_geos(projection_type="natural earth", showcoastlines=True)
        fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True, key="map_chart")
    else:
        st.warning("No data available.")

with tab3:
    st.subheader("Poverty Drivers Breakdown")
    st.markdown("Analyze whether poverty is driven more by the *number of people* affected (Headcount) or the *severity* of their poverty (Intensity).")
    
    if not filtered_df.empty and len(filtered_df) > 2:
        fig_hc = px.scatter(
            filtered_df, x='Headcount Ratio', y='MPI', color='Country', hover_name='Admin 1 Name',
            trendline='ols', title='MPI vs. Headcount Ratio', labels={'Headcount Ratio': 'Headcount Ratio (%)', 'MPI': 'MPI Value'}
        )
        st.plotly_chart(fig_hc, use_container_width=True, key="scatter_hc")


        st.info("**Insight:** Higher MPI is strongly driven by high deprivation intensity rather than just the population affected. The slope of the trendline helps identify how severe poverty compounding affects the overall index.")

        fig_int = px.scatter(
            filtered_df, x='Intensity of Deprivation', y='MPI', color='Country', hover_name='Admin 1 Name',
            trendline='ols', title='MPI vs. Intensity of Deprivation', labels={'Intensity of Deprivation': 'Intensity of Deprivation (%)', 'MPI': 'MPI Value'}
        )
        st.plotly_chart(fig_int, use_container_width=True, key="scatter_int")
    else:
        st.warning("Not enough data to calculate trendlines. Please select 'All' countries or loosen your filter parameters.")

with tab4:
    st.subheader("Poverty Risk Segmentation")
    st.markdown("Categorizing regions into risk levels based on their MPI score to quickly identify the proportion of areas needing critical intervention.")
    if not filtered_df.empty:
        col_pie, col_insight = st.columns([2, 1])
        with col_pie:
            color_map = {'Extreme': '#d62728', 'High': '#ff7f0e', 'Moderate': '#2ca02c'}
            fig_pie = px.pie(filtered_df, names='Poverty Risk Level', title='Proportion of Regions by Poverty Risk', color='Poverty Risk Level', color_discrete_map=color_map, hole=0.4)
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")
            
        with col_insight:
            st.markdown("<br><br>", unsafe_allow_html=True)
            extreme_count = len(filtered_df[filtered_df['Poverty Risk Level'] == 'Extreme'])
            total_count = len(filtered_df)
            extreme_pct = (extreme_count / total_count * 100) if total_count > 0 else 0
            
            if extreme_pct > 0:
                st.error(f"🚨 **Critical Insight:**\n\n**{extreme_pct:.1f}%** of the selected regions fall into **Extreme Poverty** (MPI > 0.4). These {extreme_count} regions require immediate, targeted humanitarian intervention.")
            else:
                st.success(f"✅ **Positive Insight:**\n\n**0%** of the selected regions fall into Extreme Poverty. Continued scaffolding is required for High and Moderate risk areas.")
    else:
        st.warning("No data available.")

with tab5:
    st.subheader("Poverty Driver Correlation")
    if len(filtered_df) > 1:
        numeric_cols = ['MPI', 'Headcount Ratio', 'Intensity of Deprivation', 'Vulnerable to Poverty', 'In Severe Poverty']
        corr_matrix = filtered_df[numeric_cols].corr()
        fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', title="Statistical Correlation of Poverty Metrics")
        st.plotly_chart(fig_corr, use_container_width=True, key="heatmap")
    else:
        st.warning("Not enough data to calculate correlations. Please select 'All' countries or adjust sliders.")

with tab6:
    # ---Head-to-Head Comparison ---
    st.subheader("Head-to-Head Country Comparison")
    st.markdown(f"Select two countries to compare their national averages directly across **{selected_metric}**.")
    
    col_c1, col_c2 = st.columns(2)
    all_countries = sorted(df['Country'].dropna().unique().tolist())
    
    country1 = col_c1.selectbox("Select First Country", all_countries, index=all_countries.index("Afghanistan") if "Afghanistan" in all_countries else 0)
    country2 = col_c2.selectbox("Select Second Country", all_countries, index=all_countries.index("Zambia") if "Zambia" in all_countries else 1)
    
    df_c1 = df[df['Country'] == country1]
    df_c2 = df[df['Country'] == country2]
    
    if not df_c1.empty and not df_c2.empty:
        c1_mean = df_c1[selected_metric].mean()
        c2_mean = df_c2[selected_metric].mean()
        
        # Display the metrics with a dynamic delta arrow
        col_c1.metric(f"{country1} {selected_metric}", f"{c1_mean:.4f}", delta=f"{c1_mean - c2_mean:.4f} vs {country2}", delta_color="inverse")
        col_c2.metric(f"{country2} {selected_metric}", f"{c2_mean:.4f}", delta=f"{c2_mean - c1_mean:.4f} vs {country1}", delta_color="inverse")
        
        # Small visual comparison chart
        comp_df = pd.DataFrame([
            {'Country': country1, 'Value': c1_mean},
            {'Country': country2, 'Value': c2_mean}
        ])
        fig_comp = px.bar(comp_df, x='Country', y='Value', color='Country', title=f"Direct Comparison: {selected_metric}")
        st.plotly_chart(fig_comp, use_container_width=True)

with tab7:
    st.subheader("Sortable Database")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    st.markdown("### Export Tools")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Data for Excel", data=csv, file_name='policymaker_mpi_data.csv', mime='text/csv')