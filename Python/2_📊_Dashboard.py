import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Load the CSV file
df = pd.read_csv(r'C:\Users\abhin\Desktop\excelr\data analyst files by sir\DATA ANALYST PROJECT\Dairy project\dairy_dataset.csv')

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Extract Year and Month for filtering and visualization
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.strftime('%B')

# Set the title and description of the dashboard
st.set_page_config(page_title="Dairy Farm Dashboard", layout="wide")

# Layout for header with image and title
header = st.container()
with header:
    t1, t2 = st.columns([1, 3])
    with t1:
        st.image(r'C:\Users\abhin\Desktop\excelr\data science material by mam\DATA SCIENCE PROJECT\dairy_project\nddb.png', width=180)
    with t2:
        st.title('NDDB DAIRY FARM DASHBOARD')
        st.markdown("This dashboard provides key insights into the operations of a dairy farm, including sales, stock levels, and revenue.")

# Sidebar - Filters
st.sidebar.header('Filters')

# Filter by Year
year_filter = st.sidebar.selectbox('Select a Year', ['All'] + sorted(df['Year'].unique().tolist()))

# Filter by Product Name
product_name_filter = st.sidebar.selectbox('Select a Product Name', ['All'] + list(df['Product Name'].unique()))

# Filter by Sales Channel
sales_channel_filter = st.sidebar.selectbox('Select a Sales Channel', ['All'] + list(df['Sales Channel'].unique()))

# Apply filters
filtered_df = df.copy()

if year_filter != 'All':
    filtered_df = filtered_df[filtered_df['Year'] == int(year_filter)]

if product_name_filter != 'All':
    filtered_df = filtered_df[filtered_df['Product Name'] == product_name_filter]

if sales_channel_filter != 'All':
    filtered_df = filtered_df[filtered_df['Sales Channel'] == sales_channel_filter]

# Layout - Split into 3 columns for the KPIs
kpi1, kpi2, kpi3 = st.columns(3)

# Total Quantity Sold
total_quantity_sold = filtered_df['Quantity Sold (liters/kg)'].sum()
kpi1.metric("Total Quantity Sold (liters/kg)", f"{total_quantity_sold:,.2f}")

# Total Revenue
total_revenue = filtered_df['Approx. Total Revenue(INR)'].sum()
kpi2.metric("Total Revenue (INR)", f"{total_revenue:,.2f}")

# Average Price per Unit Sold
if not filtered_df['Price per Unit (sold)'].empty:
    average_price_per_unit_sold = filtered_df['Price per Unit (sold)'].mean()
    kpi3.metric("Average Price per Unit Sold (INR)", f"{average_price_per_unit_sold:,.2f}")
else:
    kpi3.metric("Average Price per Unit Sold (INR)", "No Data")

# Remaining Stock
remaining_stock = filtered_df['Quantity in Stock (liters/kg)'].sum()
st.metric("Remaining Stock (liters/kg)", f"{remaining_stock:,.2f}")

# Products Below Minimum Stock Threshold
products_below_threshold = filtered_df[filtered_df['Quantity in Stock (liters/kg)'] < filtered_df['Minimum Stock Threshold (liters/kg)']]
num_products_below_threshold = products_below_threshold.shape[0]
st.metric("Products Below Minimum Stock Threshold", num_products_below_threshold)

# Layout - Charts Side by Side
chart1, chart2 = st.columns(2)

# Visualization - Total Revenue by Product Name (Bar Chart)
with chart1:
    st.subheader(f'Total Revenue for {product_name_filter} Products via {sales_channel_filter} Sales Channel')
    total_revenue_by_product = filtered_df.groupby('Product Name')['Approx. Total Revenue(INR)'].sum().sort_values(ascending=False)
    fig_revenue = px.bar(total_revenue_by_product, 
                         x=total_revenue_by_product.index, 
                         y=total_revenue_by_product.values, 
                         labels={'x':'Product Name', 'y':'Total Revenue (INR)'},
                         title="Revenue Distribution by Product",
                         color=total_revenue_by_product.values,
                         color_continuous_scale=px.colors.sequential.Teal)
    st.plotly_chart(fig_revenue)

# Visualization - Quantity Sold by Customer Location (Bar Chart)
with chart2:
    st.subheader(f'Quantity Sold for {product_name_filter} via {sales_channel_filter}')
    quantity_sold_by_location = filtered_df.groupby('Customer Location')['Quantity Sold (liters/kg)'].sum().sort_values(ascending=False)
    fig_quantity = px.bar(quantity_sold_by_location, 
                          x=quantity_sold_by_location.index, 
                          y=quantity_sold_by_location.values, 
                          labels={'x':'Customer Location', 'y':'Quantity Sold (liters/kg)'},
                          title="Quantity Sold by Customer Location",
                          color=quantity_sold_by_location.values,
                          color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig_quantity)

# Layout - Charts Side by Side
chart3, chart4 = st.columns(2)

# Visualization - Revenue Distribution by Customer Location (Pie/Doughnut Chart)
with chart3:
    st.subheader('Revenue Distribution by Customer Location')
    revenue_by_location = filtered_df.groupby('Customer Location')['Approx. Total Revenue(INR)'].sum().reset_index()
    fig_pie_revenue = px.pie(revenue_by_location, 
                             names='Customer Location', 
                             values='Approx. Total Revenue(INR)', 
                             title='Revenue Share by Customer Location', 
                             hole=0.3)  # Use hole=0.3 for a doughnut chart effect
    st.plotly_chart(fig_pie_revenue)

# Visualization - Quantity Sold by Product Name (Pie/Doughnut Chart)
with chart4:
    st.subheader('Quantity Sold by Product Name')
    quantity_by_product = filtered_df.groupby('Product Name')['Quantity Sold (liters/kg)'].sum().reset_index()
    fig_pie_quantity = px.pie(quantity_by_product, 
                              names='Product Name', 
                              values='Quantity Sold (liters/kg)', 
                              title='Quantity Sold Share by Product Name', 
                              hole=0.3)  # Use hole=0.3 for a doughnut chart effect
    st.plotly_chart(fig_pie_quantity)

# Monthly Revenue Line Chart
st.subheader(f'Monthly Revenue Trend for {year_filter}')
monthly_revenue = filtered_df.groupby(['Year', 'Month'])['Approx. Total Revenue(INR)'].sum().reset_index()
monthly_revenue['Month'] = pd.Categorical(monthly_revenue['Month'], categories=[
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)
monthly_revenue = monthly_revenue.sort_values('Month')

fig_line = px.line(monthly_revenue, 
                   x='Month', 
                   y='Approx. Total Revenue(INR)', 
                   title='Monthly Revenue Trend', 
                   labels={'Month':'Month', 'Approx. Total Revenue(INR)':'Revenue (INR)'},
                   markers=True)
st.plotly_chart(fig_line)

# Filtered Data View by Customer Location
st.subheader('Filtered Data')
location_filter = st.selectbox('Select a Customer Location', filtered_df['Customer Location'].unique())
filtered_data_by_location = filtered_df[filtered_df['Customer Location'] == location_filter]
st.write(filtered_data_by_location)