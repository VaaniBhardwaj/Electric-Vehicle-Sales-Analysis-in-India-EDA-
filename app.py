import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="EV Sales Dashboard", layout="wide")

# Title
st.title("🚗 Electric Vehicle Sales Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("EV_Dataset.csv")

df = load_data()

# Sidebar
st.sidebar.header("Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

state_filter = st.sidebar.multiselect(
    "Select State",
    options=sorted(df['State'].unique()),
    default=sorted(df['State'].unique())
)

filtered_df = df[
    (df['Year'].isin(year_filter)) &
    (df['State'].isin(state_filter))
]

# Dataset preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(50))

# KPI Section
col1, col2, col3 = st.columns(3)

col1.metric("Total EV Sales", int(filtered_df['EV_Sales_Quantity'].sum()))
col2.metric("Total States", filtered_df['State'].nunique())
col3.metric("Years Covered", filtered_df['Year'].nunique())

# ---- Charts Section ----
st.markdown("---")
st.subheader("Visual Analysis")

# 1. Year-wise EV Sales
st.markdown("### 📈 Year-wise EV Sales Trend")
yearly_sales = filtered_df.groupby('Year')['EV_Sales_Quantity'].sum()

fig1, ax1 = plt.subplots()
ax1.plot(yearly_sales.index, yearly_sales.values)
ax1.set_xlabel("Year")
ax1.set_ylabel("EV Sales Quantity")
st.pyplot(fig1)

# 2. Bar chart – Vehicle Category
st.markdown("### 📊 EV Sales by Vehicle Category")
fig2, ax2 = plt.subplots()
sns.barplot(
    x='Vehicle_Category',
    y='EV_Sales_Quantity',
    data=filtered_df,
    ax=ax2
)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)

# 3. Donut Chart – Vehicle Type Share
st.markdown("### 🍩 Vehicle Type Share")
vehicle_type_sales = filtered_df.groupby('Vehicle_Type')['EV_Sales_Quantity'].sum()

fig3, ax3 = plt.subplots()
ax3.pie(
    vehicle_type_sales,
    labels=vehicle_type_sales.index,
    autopct='%1.1f%%',
    startangle=90
)
centre_circle = plt.Circle((0,0),0.70)
ax3.add_artist(centre_circle)
st.pyplot(fig3)

# 4. Heatmap – State vs Year
st.markdown("### 🔥 Heatmap: State vs Year EV Sales")
pivot_table = filtered_df.pivot_table(
    values='EV_Sales_Quantity',
    index='State',
    columns='Year',
    aggfunc='sum'
)

fig4, ax4 = plt.subplots(figsize=(10,6))
sns.heatmap(pivot_table, cmap="YlGnBu", ax=ax4)
st.pyplot(fig4)

# 5. Boxplot – Outlier View
st.markdown("### 📦 EV Sales Distribution (Outliers)")
fig5, ax5 = plt.subplots()
sns.boxplot(x=filtered_df['EV_Sales_Quantity'], ax=ax5)
st.pyplot(fig5)

# Footer
st.markdown("---")
st.caption("EV Sales Dashboard | Built with Streamlit")