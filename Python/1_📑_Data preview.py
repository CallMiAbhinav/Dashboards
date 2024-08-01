import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Set the title of the app
st.title("🐄 Nddb Dairy Data Preview")

# Description
st.markdown("""
Welcome to the Data Preview Page Where you can Preview the data and Get EDA of the dataset in use, Feel free to Explore the dataset and its features.
""")

# importing the dataset from local directory.
data = pd.read_csv(r'C:\Users\abhin\Desktop\excelr\data analyst files by sir\DATA ANALYST PROJECT\Dairy project\dairy_dataset.csv')
    
# Display the dataframe
st.header("Data Preview")
st.write(data)

# Display some statistics
st.header("Data Statistics")
st.write(data.describe())

# Data Visualizations
st.header("Data Visualizations")
    
# Histogram
st.subheader("Histogram")
column = st.selectbox("Select a column for histogram", data.columns)

if column:
    fig, ax = plt.subplots(figsize=(20,10))
    sns.histplot(data[column], kde=True, ax=ax)
    st.pyplot(fig)
    
    
# Boxplot
    st.subheader("Boxplot")
    column = st.selectbox("Select a column for boxplot", data.columns, key="boxplot")
    if column:
        fig, ax = plt.subplots(figsize=(10,6))
        sns.boxplot(y=data[column], ax=ax)
        st.pyplot(fig)
    
# Correlation Heatmap
    # Correlation Heatmap
    st.header("Correlation Heatmap")
    
    # Select correlation coefficient range
    min_corr = st.slider("Minimum correlation coefficient", -1.0, 1.0, -1.0)
    max_corr = st.slider("Maximum correlation coefficient", -1.0, 1.0, 1.0)
    
    if min_corr < max_corr:
        numeric_data = data.select_dtypes(include='number')
        corr = numeric_data.corr()
        
        # Filter the correlation matrix
        mask = (corr >= min_corr) & (corr <= max_corr)
        filtered_corr = corr.where(mask)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(filtered_corr, annot=True, cmap='coolwarm', ax=ax, vmin=-1, vmax=1, center=0)
        ax.set_title(f"Correlation Heatmap (Correlation Coefficients between {min_corr} and {max_corr})")
        st.pyplot(fig)
    else:
        st.warning("The minimum correlation coefficient should be less than the maximum correlation coefficient.")

    

# Scatter Plot
    st.header("Regression Scatter Plot")
    numeric_data = data.select_dtypes(include="number")
    columns = numeric_data.columns.tolist()
    x_column = st.selectbox("Select the X-axis column", columns)
    y_column = st.selectbox("Select the Y-axis column", columns)
    line_color = st.color_picker("Pick a color for the regression line", "#FF0000")
    
    if x_column and y_column:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.regplot(x=numeric_data[x_column], y=numeric_data[y_column], ax=ax, line_kws={'color': line_color})
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"Regression Scatter Plot of {x_column} vs {y_column}")
        st.pyplot(fig)

else:
    st.info("Please upload a CSV file to preview the data.")
