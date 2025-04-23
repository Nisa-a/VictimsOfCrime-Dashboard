# import necessary libraries:
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# Loading dataset into a data frame.
df = pd.read_csv("cleaned_data_crime.csv")

# Titles:
st.title("Crime Victimisation")
st.markdown("An interactive dashboard")
st.caption("Use the filters in the sidebar to explore how victims of crime varies by year, gender, and demographics.")
st.markdown("---")

# Sidebar:
st.sidebar.title("Filter Options")
st.sidebar.markdown("---")

# Filter widgets:
# Wa, W. (2020) Build your first interactive dashboard with cross-filtering in Streamlit. Medium. Available at: https://medium.com/@weijiawa/build-your-first-interactive-dashboard-with-cross-filtering-in-streamlit-e7ae673001d3 (Accessed: 22 April 2025).
year_filter = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=["2013/14","2014/15","2015/16","2016/17","2017/18","2018/19","2019/20"])
ethnicity_filter = st.sidebar.multiselect("Ethnicity", sorted(df["Ethnicity"].unique()))
gender_filter = st.sidebar.selectbox("Gender", sorted(df["Gender"].unique()), index = 0)
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

if gender_filter:
    filtered_data = filtered_data[filtered_data["Gender"] == gender_filter]

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
st.sidebar.download_button("Download Filtered Data as CSV", filtered_data.to_csv(index=False), "filtered_data.csv")

# Layout for the summary metrics:
# Tech with Tim (2021) How to Build an Interactive Dashboard with Streamlit. YouTube. Available at: https://www.youtube.com/watch?v=hQnMV_bF84I (Accessed: 22 April 2025).
# Streamlit (n.d.) st.metric – Streamlit Docs. Available at: https://docs.streamlit.io/develop/api-reference/data/st.metric (Accessed: 22 April 2025).
# Streamlit (n.d.) st.columns – Streamlit Docs. Available at: https://docs.streamlit.io/develop/api-reference/layout/st.columns (Accessed: 22 April 2025).
col1, col2, col3 = st.columns(3)

with col1:
    highest_year = df.groupby("Year")["Sample size"].sum().idxmax()
    col1.metric("Year with Most Reported Victims", highest_year)

with col2:
    region_count = df["Region"].nunique()
    col2.metric("Covered Regions", region_count)

with col3:
    average_rate = round(df["Value"].mean(), 2)
    col3.metric("Overall Victimisation Rate", f"{average_rate:.2f}%")

# Trend line chart: 
victim_trend_chart = filtered_data.groupby("Year")["Sample size"].sum().reset_index()
fig = px.line(victim_trend_chart, x="Year", y="Sample size", labels={"Sample size": "Victim Count"}, title="Number of Victims Over Time")
st.plotly_chart(fig)

# display the tabular format of the filtered data:
if st.checkbox("Show Raw Filtered Data"):
    st.dataframe(filtered_data)

# Create tabs for the different visualisations:
# Streamlit (n.d.) st.tabs – Streamlit Docs. Available at: https://docs.streamlit.io/develop/api-reference/layout/st.tabs (Accessed: 22 April 2025).
tab1, tab2, tab3 = st.tabs(["By Ethnicity", "By Gender", "By Age Group"])

# Bar chart for ethnicity:
ethnicity_stats = filtered_data.groupby("Ethnicity")["Sample size"].mean().reset_index()
# Plotly (n.d.). Bar Charts. [online] plotly.com. Available at: https://plotly.com/python/bar-charts/.
fig = px.bar(ethnicity_stats, height = 600,width = 900, x="Ethnicity", y="Sample size", title="Victimisation by Ethnicity", color = "Ethnicity", labels= {"Sample size": "Avg. Number of Victims"}, )
# plotly.com. (n.d.). Layout.xaxis. [online] Available at: https://plotly.com/python/reference/layout/xaxis/.
fig.update_xaxes(showticklabels=False) # Hide x-axis label.
tab1.plotly_chart(fig)


