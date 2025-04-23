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