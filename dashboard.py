import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Excel
df = pd.read_excel("sales_daep.xlsx")

st.title("Excel Dashboard with Streamlit")
st.write("Here’s a preview of your data:")
st.dataframe(df)

st.set_page_config(page_title="Excel Dashboard", layout="wide")





####################### Try the upper part first #######
################ Comment below lines ###############
# Load Excel file
@st.cache_data

def load_data():
    return pd.read_excel("sales_daep.xlsx")


df = load_data()

# Sidebar filters
st.write(df.columns)
st.sidebar.header("Filters")
segment = st.sidebar.selectbox("Segment", df["Segment"].unique())
period = st.sidebar.selectbox("period", df["Year"].unique())

# Filter data
filtered_df = df[(df["Segment"] == segment) & (df["Year"] == period)]

# KPIs
total_spend = filtered_df["Sales"].sum()
avg_spend = filtered_df["Sales"].mean()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_spend:,.0f}")
col2.metric("Average Sales", f"${avg_spend:,.0f}")

# Data table
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Bar chart
st.subheader("Sales by Category of Goods")
st.bar_chart(filtered_df.groupby("Category of Goods")["Sales"].sum())

####################### Additional Visualizations #######################

# 1. Sales by Category of Goods
st.subheader("Sales by Category of Goods")
category_sales = filtered_df.groupby("Category of Goods")["Sales"].sum().reset_index()
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(data=category_sales, x="Category of Goods", y="Sales", palette="Blues_d", ax=ax)
ax.set_ylabel("Sales ($)")
ax.set_xlabel("Category of Goods")
ax.set_title("Sales by Category of Goods")
st.pyplot(fig)

# 2. Sales by Sub-Category
st.subheader("Sales by Sub-Category")
subcat_sales = filtered_df.groupby("Sub-Category")["Sales"].sum().reset_index()
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=subcat_sales, x="Sub-Category", y="Sales", palette="Greens_d", ax=ax)
ax.set_ylabel("Sales ($)")
ax.set_xlabel("Sub-Category")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
ax.set_title("Sales by Sub-Category")
st.pyplot(fig)

# 3. Sales by Region
st.subheader("Sales by Region")
region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
fig, ax = plt.subplots(figsize=(6,4))
sns.barplot(data=region_sales, x="Region", y="Sales", palette="Oranges_d", ax=ax)
ax.set_ylabel("Sales ($)")
ax.set_xlabel("Region")
ax.set_title("Sales by Region")
st.pyplot(fig)

# 4. Top 10 Products by Sales
st.subheader("Top 10 Products by Sales")
top_products = filtered_df.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(data=top_products, y="Product Name", x="Sales", palette="Purples_d", ax=ax)
ax.set_xlabel("Sales ($)")
ax.set_ylabel("Product Name")
ax.set_title("Top 10 Products by Sales")
st.pyplot(fig)

# 5. Pie Chart: Sales Share by Category of Goods
st.subheader("Sales Share by Category of Goods")
sales_category = filtered_df.groupby("Category of Goods")["Sales"].sum()
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(sales_category, labels=sales_category.index, autopct="%1.1f%%", startangle=140, colors=sns.color_palette("pastel"))
ax.set_title("Sales Share by Category of Goods")
st.pyplot(fig)

# 6. Heatmap: Region vs Category of Goods
st.subheader("Sales Heatmap: Region vs Category of Goods")
sales_heatmap = filtered_df.pivot_table(
    values="Sales",
    index="Region",
    columns="Category of Goods",
    aggfunc="sum",
    fill_value=0
)
fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(sales_heatmap, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set_title("Sales Heatmap by Region and Category")
st.pyplot(fig)