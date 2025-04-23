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
st.caption("Use the filters in the sidebar to explore how victims of crime varies by year, region, and demographics.")
st.markdown("---")
# Sidebar:
st.sidebar.title("Filter Options")
st.sidebar.markdown("---")
# Filter widgets:
# Wa, W. (2020) Build your first interactive dashboard with cross-filtering in Streamlit. Medium. Available at: https://medium.com/@weijiawa/build-your-first-interactive-dashboard-with-cross-filtering-in-streamlit-e7ae673001d3 (Accessed: 22 April 2025).
year_filter = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=["2013/14","2014/15","2015/16","2016/17","2017/18","2018/19","2019/20"])
region_filter = st.sidebar.multiselect("Region", df["Region"].unique())
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

if region_filter:
    filtered_data = filtered_data[filtered_data["Region"].isin(region_filter)]

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