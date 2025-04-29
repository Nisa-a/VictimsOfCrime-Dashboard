# import necessary libraries:
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# Loading dataset into a data frame.
df = pd.read_csv("cleaned_data_crime.csv")

# Titles:
st.title("Crime Victimisation")
st.markdown("#####  An interactive dashboard")
st.caption("Use the filters in the sidebar to explore how victims of crime varies by year, gender, and demographics.")
st.markdown("---")

# Sidebar:
st.sidebar.title("Filter Options")
# Filter widgets:
# Wa, W. (2020) Build your first interactive dashboard with cross-filtering in Streamlit. Medium. Available at: https://medium.com/@weijiawa/build-your-first-interactive-dashboard-with-cross-filtering-in-streamlit-e7ae673001d3 (Accessed: 22 April 2025).
year_filter = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=["2013/14","2014/15","2015/16","2016/17","2017/18","2018/19","2019/20"])
ethnicity_filter = st.sidebar.multiselect("Ethnicity", sorted(df["Ethnicity"].unique()))
age_filter = st.sidebar.multiselect("Age", df["Age"].unique())
socio_eco_class_filter = st.sidebar.multiselect("Socio-economic classification", df["Socio-economic classification"].unique())
house_income_filter = st.sidebar.multiselect("Household income", df["Household income"].unique())
st.sidebar.markdown("---")

# Apply filters only if a value is selected:
# Wa, W. (2020) Build your first interactive dashboard with cross-filtering in Streamlit. Medium. Available at: https://medium.com/@weijiawa/build-your-first-interactive-dashboard-with-cross-filtering-in-streamlit-e7ae673001d3 (Accessed: 22 April 2025).
filtered_data = df.copy()
if year_filter:
    filtered_data = filtered_data[filtered_data["Year"].isin(year_filter)]

if ethnicity_filter:
    filtered_data = filtered_data[filtered_data["Ethnicity"].isin(ethnicity_filter)]

if age_filter:
    filtered_data = filtered_data[filtered_data["Age"].isin(age_filter)]

if socio_eco_class_filter:
    filtered_data = filtered_data[filtered_data["Socio-economic classification"].isin(socio_eco_class_filter)]

if house_income_filter:
    filtered_data = filtered_data[filtered_data["Household income"].isin(house_income_filter)]

if filtered_data.empty:
    st.warning("No data available for the selected filters. Try adjusting the filters.")
    st.stop() 

# Create download button for filtered data.
st.sidebar.download_button("Export as CSV", filtered_data.to_csv(index=False), "filtered_data.csv")

# Layout for the summary metrics:

st.subheader("Key Summary Metrics") 
# Tech with Tim (2021) How to Build an Interactive Dashboard with Streamlit. YouTube. Available at: https://www.youtube.com/watch?v=hQnMV_bF84I (Accessed: 22 April 2025).
# Streamlit (n.d.) st.metric – Streamlit Docs. Available at: https://docs.streamlit.io/develop/api-reference/data/st.metric (Accessed: 22 April 2025).
# Streamlit (n.d.) st.columns – Streamlit Docs. Available at: https://docs.streamlit.io/develop/api-reference/layout/st.columns (Accessed: 22 April 2025).
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    highest_year = df.groupby("Year")["Sample size"].sum().idxmax()
    col1.metric("Peak Victim Year", highest_year)

with col2:
    region_count = df["Region"].nunique()
    col2.metric("Covered Regions", region_count)

with col3:
    average_rate = round(df["Value"].mean(), 2)
    col3.metric("Avg. Victimisation Rate", f"{average_rate:.2f}%", help="Average across all years and regions" )
st.markdown("---")

st.subheader("Trends") 
col4, col5 = st.columns([4,2])
# Trend line chart:
victim_trend_chart = filtered_data.groupby("Year")["Sample size"].sum().reset_index()
fig = px.line(victim_trend_chart, x="Year", y="Sample size", labels={"Sample size": "Victim Count"}, title="Victims Over Time:")
col4.plotly_chart(fig)

# Pie Chart for gender
gender_stats = df[df["Gender"].isin(["Female","Male"])].groupby("Gender")["Sample size"].sum().reset_index()
# Plotly.com. (2025). Pie Charts. [online] Available at https://plotly.com/python/pie-charts/
fig = px.pie(gender_stats,height = 600,width = 900, names= "Gender", values= "Sample size", title="Gender Breakdown:", color = "Gender", labels={"Sample size": "Total Victims"} )
fig.update(layout_showlegend=False)
fig.update_traces(textposition='inside', textinfo='percent+label')
col5.plotly_chart(fig)
st.markdown("---")

# Create tabs for the different visualisations:
st.subheader(" Victimisation by Demographic")
# Streamlit (n.d.) st.tabs – Streamlit Docs. Available at: https://docs.streamlit.io/develop/api-reference/layout/st.tabs (Accessed: 22 April 2025).
tab1, tab2, tab3, tab4 = st.tabs(["By Ethnicity", "By Age Group", "By Household income", "By Socio-economic classification"])

# Bar chart for ethnicity:
ethnicity_stats = filtered_data.groupby("Ethnicity")["Sample size"].mean().reset_index()
# Plotly (n.d.). Bar Charts. [online] plotly.com. Available at: https://plotly.com/python/bar-charts/.
fig = px.bar(ethnicity_stats, height = 600,width = 900, x="Ethnicity", y="Sample size", title= "Ethnicity of Victims", color = "Ethnicity", labels= {"Sample size": "Avg. Number of Victims"}, )
# plotly.com. (n.d.). Layout.xaxis. [online] Available at: https://plotly.com/python/reference/layout/xaxis/.
fig.update_xaxes(showticklabels=False) # Hide x-axis label.
tab1.plotly_chart(fig)

# Bar chart for age group:
age_stats = filtered_data.groupby("Age")["Sample size"].mean().reset_index()
fig = px.bar(age_stats, x="Age", y="Sample size", title="Age Group of Victims", color = "Age", labels = {"Sample size": "Avg. Number of Victims"})
# Plotly.com. (2025). Layout. [online] Available at: https://plotly.com/python/reference/layout/#layout-showlegend [Accessed 22 Apr. 2025].
fig.update_layout(showlegend=False)  # Hide legend.
tab2.plotly_chart(fig)

# Bar chart for household income:
household_stats = filtered_data.groupby("Household income")["Sample size"].mean().reset_index()
fig = px.bar(household_stats, height = 600,width = 900, x="Household income", y="Sample size", title="Household Income of Victims", color = "Household income", labels = {"Sample size": "Avg. Number of Victims"})
fig.update_xaxes(showticklabels=False) # Hide x-axis label.
tab3.plotly_chart(fig)

# Bar chart for Socio-economic classification:
Socio_stats = filtered_data.groupby("Socio-economic classification")["Sample size"].mean().reset_index()
fig = px.bar(Socio_stats, height = 600,width = 900, x="Socio-economic classification", y="Sample size", title="Socio-economic classification of Victims", color = "Socio-economic classification", labels = {"Sample size": "Avg. Number of Victims"})
fig.update_xaxes(showticklabels=False) # Hide x-axis label.
tab4.plotly_chart(fig)

# Display the tabular format of the filtered data:
if st.checkbox("View Raw Data"):
    st.dataframe(filtered_data)
    