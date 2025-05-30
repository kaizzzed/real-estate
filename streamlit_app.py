## Step 00 - Import of the packages

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

from ydata_profiling import ProfileReport 
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(
    page_title="California Housing Dashboard",
    layout="centered",
    page_icon="🏠"
)

## Step 01 - Setup
st.sidebar.title("California - Real Estate Agency 🏡")
page = st.sidebar.selectbox("Select Page", ["Introduction", "Visualization", "Automated Report"])

# st.write("Explore the portfolio of our real estate agency in a nice way >>")

#st.video("video.mp4")

st.image("house2.jpg")

st.write("   ")
st.write("   ")
st.write("   ")

df = pd.read_csv("housing.csv")

## Step 02 - Load dataset
if page == "Introduction":
    st.subheader("01 Data Exploration")

    st.markdown("##### Data Preview")
    rows = st.slider("Select a number of rows to display", 5, 20, 5)
    st.dataframe(df.head(rows))

    st.markdown("##### Missing values")
    missing = df.isnull().sum()
    st.write(missing)

    if missing.sum() == 0:
        st.success("No missing values found")
    else:
        st.warning("Missing values found")

    st.markdown("##### Statistic about the dataset")
    if st.button("Show Describe Table"):
        st.dataframe(df.describe())

## Step 03 - Data Viz
elif page == "Visualization":
    st.subheader("02 Data Viz")

    col_x = st.selectbox("Select x-axis variable", df.columns, index=0)
    col_y = st.selectbox("Select y-axis variable", df.columns, index=1)

    tab1, tab2, tab3 = st.tabs(["Bar Chart", "Line Chart", "Correlation Heatmap"])
    
    with tab1:
        st.subheader("Bar Chart")
        st.bar_chart(df[[col_x, col_y]].sort_values(by=col_x),use_container_width=True)
    
    with tab2:
        st.subheader("Line Chart")
        st.line_chart(df[[col_x, col_y]].sort_values(by=col_x),use_container_width=True)
    
    with tab3:
        st.subheader("Correlation Matrix")
        df_numeric = df.select_dtypes(include=np.number)
        ## start with creating the empty frame that receives the plot
        fig_corr, ax_corr = plt.subplots(figsize=(18,14))
        ## create the plot, in this case with seaborn 
        sns.heatmap(df_numeric.corr(),annot=True,fmt=".2f",cmap='coolwarm')
        ## render the plot in streamlit 
        st.pyplot(fig_corr)

elif page == "Automated Report":
    st.subheader("Automated Report")
    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            profile = ProfileReport(df, title="California Housing Report", explorative=True, minimal=True)
    
    export = profile.to_html()
    st.download_button(label="Download full report", data=export, file_name="california_housing_report.html")
