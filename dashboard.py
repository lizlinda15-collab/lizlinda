import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="Liz Supermarket Sales Dashboard", layout="wide")

# Dashboard title
st.title("🛒 Liz Supermarket Sales Analysis Dashboard")
st.markdown("#### Comprehensive Sales Analytics | 2023 – 2025")
st.markdown("---")

# Load data
@st.cache_data
def load_sales_data():
    np.random.seed(42)
    
    # Date range: 3 years of daily data
    dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="D")
    
    # Branches
    branches = ["Downtown", "Westlands", "Eastlands", "South B", "Karen", "Thika Road"]
    
    # Product categories
    categories = {
        "Fresh Produce": ["Tomatoes", "Onions", "Potatoes", "Cabbages", "Kales", "Carrots", "Spinach"],
        "Dairy & Eggs": ["Milk", "Yogurt", "Cheese", "Butter", "Eggs", "Cream"],
        "Meat & Seafood": ["Beef", "Chicken", "Pork", "Fish", "Sausages", "Bacon"],
        "Beverages": ["Soda", "Juice", "Water", "Tea", "Coffee", "Energy Drinks"],
        "Snacks": ["Chips", "Biscuits", "Candy", "Chocolate", "Popcorn", "Nuts"],
        "Household": ["Detergent", "Soap", "Tissue", "Cleaning", "Batteries", "Light Bulbs"],
        "Personal Care": ["Shampoo", "Soap Bar", "Toothpaste", "Deodorant", "Lotion", "Razor"],
        "Grains & Cereals": ["Rice", "Maize Flour", "Wheat Flour", "Bread", "Pasta", "Beans"],
        "Frozen Foods": ["Frozen Veg", "Ice Cream", "Frozen Meat", "Fries", "Pizza"],
        "Health & Baby": ["Diapers", "Baby Food", "Vitamins", "First Aid", "Sanitary Pads"]
    }
    
    # Payment methods
    payment_methods = ["Cash", "M-Pesa", "Card", "Bank Transfer"]
    
    data = []
    
    for date in dates:
        year = date.year
        month = date.month
        day_of_week = date.dayofweek
        is_weekend = day_of_week >= 5
        
        # Seasonal factors
        if month == 12:  # December peak
            season_factor = 1.5
        elif month == 1:  # January low
            season_factor = 0.7
        elif month == 8:  # August moderate
            season_factor = 0.9
        else:
            season_factor = 1.0
        
        # Yearly growth
        year_factor = 1 + (year - 2023) * 0.12  # 12% annual growth
        
        for branch in branches:
            # Branch popularity factor
            if branch in ["Downtown", "Westlands"]:
                branch_factor = 1.3
            elif branch in ["Karen", "Thika Road"]:
                branch_factor = 1.1
            else:
                branch_factor = 0.9
            
            for category, products in categories.items():
                for product in products[:3]:  # Limit to 3 products per category for performance
                    # Base price per product
                    if product in ["Milk", "Beef", "Rice"]:
                        price = np.random.uniform(100, 300)
                    elif product in ["Tomatoes", "Onions", "Potatoes"]:
                        price = np.random.uniform(50, 150)
                    else:
                        price = np.random.uniform(30, 200)
                    
                    # Volume sold
                    if category == "Fresh Produce":
                        base_volume = np.random.uniform(20, 100)
                    elif category in ["Dairy & Eggs", "Beverages"]:
                        base_volume = np.random.uniform(15, 80)
                    else:
                        base_volume = np.random.uniform(5, 50)
                    
                    # Apply factors
                    volume = base_volume * season_factor * year_factor * branch_factor
                    if is_weekend:
                        volume *= 1.3  # Weekend boost
                    
                    volume = int(volume)
                    sales_amount = volume * price
                    
                    # Payment method distribution (cash decreasing over years)
                    if year <= 2023:
                        payment = np.random.choice(payment_methods, p=[0.5, 0.3, 0.15, 0.05])
                    elif year == 2024:
                        payment = np.random.choice(payment_methods, p=[0.4, 0.35, 0.2, 0.05])
                    else:
                        payment = np.random.choice(payment_methods, p=[0.3, 0.4, 0.25, 0.05])
                    
                    data.append({
                        "Date": date,
                        "Year": year,
                        "Month": date.strftime("%b"),
                        "Weekday": date.strftime("%A"),
                        "Is_Weekend": is_weekend,
                        "Branch": branch,
                        "Category": category,
                        "Product": product,
                        "Quantity": volume,
                        "Unit_Price": round(price, 2),
                        "Sales_Amount": round(sales_amount, 2),
                        "Payment_Method": payment,
                        "Payment_Type": "Cash" if payment == "Cash" else "Digital"
                    })
    
    return pd.DataFrame(data)

# Load data
df = load_sales_data()

# Calculate summary metrics
total_sales = df["Sales_Amount"].sum()
total_quantity = df["Quantity"].sum()
avg_transaction = df.groupby("Date")["Sales_Amount"].sum().mean()
total_customers = df.groupby("Date").size().sum()

# Sidebar Filters
st.sidebar.header("🔍 Filter Dashboard")

# Date range filter
min_date = df["Date"].min()
max_date = df["Date"].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
else:
    filtered_df = df.copy()

# Year filter
years = st.sidebar.multiselect("Select Year(s)", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
filtered_df = filtered_df[filtered_df["Year"].isin(years)]

# Branch filter
branches = st.sidebar.multiselect("Select Branch(es)", df["Branch"].unique(), default=df["Branch"].unique())
filtered_df = filtered_df[filtered_df["Branch"].isin(branches)]

# Category filter
categories = st.sidebar.multiselect("Select Category(ies)", df["Category"].unique(), default=df["Category"].unique())
filtered_df = filtered_df[filtered_df["Category"].isin(categories)]

# Top bar metrics
st.header("📊 Sales Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("💰 Total Sales", f"KES {total_sales:,.0f}")
with col2:
    st.metric("📦 Total Quantity Sold", f"{total_quantity:,.0f} units")
with col3:
    st.metric("💳 Avg Daily Sales", f"KES {avg_transaction:,.0f}")
with col4:
    st.metric("👥 Est. Customers", f"{total_customers:,.0f}")
with col5:
    best_branch = filtered_df.groupby("Branch")["Sales_Amount"].sum().idxmax()
    st.metric("🏆 Best Branch", best_branch)

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Sales Trends",
    "🏪 Branch Performance",
    "📦 Product Analysis",
    "💳 Payment Analytics",
    "📊 Category Insights",
    "📋 Data & Export"
])

# ==============================
# TAB 1: Sales Trends
# ==============================
with tab1:
    st.subheader("Sales Trends Over Time")
    
    # Monthly sales trend
    monthly_sales = filtered_df.groupby(["Year", "Month"])["Sales_Amount"].sum().reset_index()
    monthly_sales["Date"] = pd.to_datetime(monthly_sales["Year"].astype(str) + "-" + monthly_sales["Month"], format="%Y-%b")
    monthly_sales = monthly_sales.sort_values("Date")
    
    fig1 = px.line(
        monthly_sales,
        x="Date",
        y="Sales_Amount",
        title="Monthly Sales Trend (KES)",
        markers=True,
        line_shape="spline"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Yearly comparison
        yearly_sales = filtered_df.groupby("Year")["Sales_Amount"].sum().reset_index()
        fig2 = px.bar(
            yearly_sales,
            x="Year",
            y="Sales_Amount",
            title="Yearly Total Sales",
            text_auto=True,
            color="Sales_Amount",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Weekday vs Weekend
        filtered_df["Week_Type"] = filtered_df["Is_Weekend"].map({True: "Weekend", False: "Weekday"})
        weekday_sales = filtered_df.groupby("Week_Type")["Sales_Amount"].sum().reset_index()
        fig3 = px.pie(
            weekday_sales,
            values="Sales_Amount",
            names="Week_Type",
            title="Weekday vs Weekend Sales",
            hole=0.3,
            color_discrete_map={"Weekday": "#3498db", "Weekend": "#e74c3c"}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # Seasonal heatmap
    st.subheader("Seasonal Sales Pattern")
    pivot_sales = filtered_df.pivot_table(
        values="Sales_Amount",
        index="Year",
        columns="Month",
        aggfunc="sum",
        fill_value=0
    )
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pivot_sales = pivot_sales[[m for m in month_order if m in pivot_sales.columns]]
    
    fig4 = px.imshow(
        pivot_sales / 1000,
        text_auto=True,
        aspect="auto",
        title="Sales Heatmap: Year vs Month (KES '000)",
        labels={"x": "Month", "y": "Year", "color": "Sales (KES K)"},
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ==============================
# TAB 2: Branch Performance
# ==============================
with tab2:
    st.subheader("Branch Performance Analysis")
    
    # Sales by branch
    branch_sales = filtered_df.groupby("Branch")["Sales_Amount"].sum().sort_values(ascending=False).reset_index()
    
    fig5 = px.bar(
        branch_sales,
        x="Branch",
        y="Sales_Amount",
        title="Total Sales by Branch (KES)",
        color="Sales_Amount",
        color_continuous_scale="Greens",
        text_auto=True
    )
    st.plotly_chart(fig5, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Branch monthly trend
        branch_trend = filtered_df.groupby(["Date", "Branch"])["Sales_Amount"].sum().reset_index()
        top_branches = branch_sales.head(4)["Branch"].tolist()
        branch_trend_top = branch_trend[branch_trend["Branch"].isin(top_branches)]
        
        fig6 = px.line(
            branch_trend_top,
            x="Date",
            y="Sales_Amount",
            color="Branch",
            title="Top Branches - Sales Trend",
            markers=True
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        # Branch market share
        fig7 = px.pie(
            branch_sales,
            values="Sales_Amount",
            names="Branch",
            title="Branch Market Share",
            hole=0.3
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    # Branch performance metrics
    st.subheader("Branch Performance Metrics (2025)")
    branch_metrics = filtered_df[filtered_df["Year"] == 2025].groupby("Branch").agg({
        "Sales_Amount": "sum",
        "Quantity": "sum",
        "Sales_Amount": "count"
    }).round(0)
    branch_metrics.columns = ["Total_Sales", "Total_Quantity", "Transaction_Count"]
    branch_metrics["Avg_Transaction"] = branch_metrics["Total_Sales"] / branch_metrics["Transaction_Count"]
    st.dataframe(branch_metrics, use_container_width=True)

# ==============================
# TAB 3: Product Analysis
# ==============================
with tab3:
    st.subheader("Product Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top products by sales
        top_products = filtered_df.groupby("Product")["Sales_Amount"].sum().sort_values(ascending=False).head(15).reset_index()
        
        fig8 = px.bar(
            top_products,
            x="Sales_Amount",
            y="Product",
            orientation="h",
            title="Top 15 Products by Sales (KES)",
            color="Sales_Amount",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        # Top products by quantity
        top_quantity = filtered_df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(15).reset_index()
        
        fig9 = px.bar(
            top_quantity,
            x="Quantity",
            y="Product",
            orientation="h",
            title="Top 15 Products by Quantity Sold",
            color="Quantity",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    # Product trend for top sellers
    st.subheader("Top 5 Products - Sales Trend")
    top_5_products = filtered_df.groupby("Product")["Sales_Amount"].sum().nlargest(5).index
    product_trend = filtered_df[filtered_df["Product"].isin(top_5_products)].groupby(["Date", "Product"])["Sales_Amount"].sum().reset_index()
    
    fig10 = px.line(
        product_trend,
        x="Date",
        y="Sales_Amount",
        color="Product",
        title="Top 5 Products Sales Trends",
        markers=True
    )
    st.plotly_chart(fig10, use_container_width=True)
    
    # Product performance table
    st.subheader("Product Performance Summary")
    product_summary = filtered_df.groupby("Product").agg({
        "Sales_Amount": "sum",
        "Quantity": "sum",
        "Unit_Price": "mean"
    }).round(2).sort_values("Sales_Amount", ascending=False)
    product_summary.columns = ["Total_Sales_KES", "Total_Quantity", "Avg_Price"]
    st.dataframe(product_summary.head(20), use_container_width=True)

# ==============================
# TAB 4: Payment Analytics
# ==============================
with tab4:
    st.subheader("Payment Method Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Payment distribution
        payment_dist = filtered_df.groupby("Payment_Method")["Sales_Amount"].sum().reset_index()
        
        fig11 = px.pie(
            payment_dist,
            values="Sales_Amount",
            names="Payment_Method",
            title="Sales by Payment Method",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig11, use_container_width=True)
    
    with col2:
        # Cash vs Digital trend
        payment_trend = filtered_df.groupby(["Year", "Payment_Type"])["Sales_Amount"].sum().reset_index()
        
        fig12 = px.bar(
            payment_trend,
            x="Year",
            y="Sales_Amount",
            color="Payment_Type",
            title="Cash vs Digital Payment Trend",
            barmode="group",
            color_discrete_map={"Cash": "#f39c12", "Digital": "#27ae60"}
        )
        st.plotly_chart(fig12, use_container_width=True)
    
    # Digital adoption over time
    st.subheader("Digital Payment Adoption Rate")
    digital_adoption = filtered_df.groupby("Year").apply(
        lambda x: (x[x["Payment_Type"] == "Digital"]["Sales_Amount"].sum() / x["Sales_Amount"].sum()) * 100
    ).reset_index(name="Digital_Adoption_Rate")
    
    fig13 = px.line(
        digital_adoption,
        x="Year",
        y="Digital_Adoption_Rate",
        title="Digital Payment Adoption Rate (%)",
        markers=True,
        line_shape="linear"
    )
    fig13.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="50% Target")
    st.plotly_chart(fig13, use_container_width=True)
    
    # Payment method by branch
    st.subheader("Payment Methods by Branch")
    branch_payment = filtered_df.groupby(["Branch", "Payment_Method"])["Sales_Amount"].sum().reset_index()
    
    fig14 = px.bar(
        branch_payment,
        x="Branch",
        y="Sales_Amount",
        color="Payment_Method",
        title="Payment Method Distribution by Branch",
        barmode="stack"
    )
    st.plotly_chart(fig14, use_container_width=True)

# ==============================
# TAB 5: Category Insights
# ==============================
with tab5:
    st.subheader("Category Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by category
        category_sales = filtered_df.groupby("Category")["Sales_Amount"].sum().sort_values(ascending=False).reset_index()
        
        fig15 = px.bar(
            category_sales,
            x="Category",
            y="Sales_Amount",
            title="Total Sales by Category (KES)",
            color="Sales_Amount",
            color_continuous_scale="Reds",
            text_auto=True
        )
        st.plotly_chart(fig15, use_container_width=True)
    
    with col2:
        # Category market share
        fig16 = px.pie(
            category_sales.head(8),
            values="Sales_Amount",
            names="Category",
            title="Top 8 Categories by Market Share",
            hole=0.3
        )
        st.plotly_chart(fig16, use_container_width=True)
    
    # Category performance over time
    st.subheader("Top Categories Performance Trend")
    top_categories = category_sales.head(6)["Category"].tolist()
    category_trend = filtered_df[filtered_df["Category"].isin(top_categories)].groupby(["Date", "Category"])["Sales_Amount"].sum().reset_index()
    
    fig17 = px.line(
        category_trend,
        x="Date",
        y="Sales_Amount",
        color="Category",
        title="Top Categories - Sales Trends",
        markers=True
    )
    st.plotly_chart(fig17, use_container_width=True)
    
    # Category by branch heatmap
    st.subheader("Category Performance by Branch")
    category_branch = filtered_df.groupby(["Branch", "Category"])["Sales_Amount"].sum().reset_index()
    category_branch_pivot = category_branch.pivot(index="Branch", columns="Category", values="Sales_Amount").fillna(0)
    
    fig18 = px.imshow(
        category_branch_pivot / 1000,
        text_auto=True,
        aspect="auto",
        title="Sales Heatmap: Branch vs Category (KES '000)",
        labels={"x": "Category", "y": "Branch", "color": "Sales (KES K)"},
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig18, use_container_width=True)

# ==============================
# TAB 6: Data & Export
# ==============================
with tab6:
    st.subheader("Sales Data Export")
    
    # Summary statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Daily Summary")
        daily_summary = filtered_df.groupby("Date").agg({
            "Sales_Amount": "sum",
            "Quantity": "sum",
            "Transaction_Count": "count"
        }).reset_index()
        daily_summary.columns = ["Date", "Daily_Sales", "Daily_Quantity", "Transactions"]
        st.dataframe(daily_summary.head(50), use_container_width=True)
    
    with col2:
        st.markdown("### Category Summary")
        category_summary = filtered_df.groupby("Category").agg({
            "Sales_Amount": "sum",
            "Quantity": "sum",
            "Product": "nunique"
        }).reset_index()
        category_summary.columns = ["Category", "Total_Sales", "Total_Quantity", "Unique_Products"]
        st.dataframe(category_summary, use_container_width=True)
    
    # Download buttons
    st.markdown("---")
    st.subheader("📎 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_full = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Full Data", csv_full, "liz_supermarket_full_data.csv", "text/csv")
    
    with col2:
        csv_daily = daily_summary.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Daily Summary", csv_daily, "liz_supermarket_daily_summary.csv", "text/csv")
    
    with col3:
        csv_category = category_summary.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Category Summary", csv_category, "liz_supermarket_category_summary.csv", "text/csv")
    
    # Raw data view
    with st.expander("View Raw Sales Data"):
        st.dataframe(filtered_df.head(500), use_container_width=True)

# Footer
st.markdown("---")
st.caption("📌 Liz Supermarket Sales Dashboard | Data 2023-2025 | For inquiries: analytics@lizsupermarket.co.ke")
