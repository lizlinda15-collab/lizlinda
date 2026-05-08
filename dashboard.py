import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Nova University Dashboard", layout="wide")

# Dashboard title
st.title("🏛️ Nova University Dashboard")
st.markdown("#### Institutional Analytics | 2023 – 2025")
st.markdown("---")

# Load data - Simplified
@st.cache_data
def load_data():
    np.random.seed(42)
    
    # Departments (15 total - bigger than Clinton)
    departments = [
        "Business", "Engineering", "Computing", "Law", "Medicine",
        "Nursing", "Education", "Humanities", "Social Sciences", 
        "Pharmacy", "Architecture", "Journalism", "Agriculture",
        "Dentistry", "Veterinary Medicine"
    ]
    
    years = [2023, 2024, 2025]
    
    data = []
    
    for year in years:
        growth = 1 + (year - 2023) * 0.12
        
        for dept in departments:
            # Students
            if dept in ["Business", "Computing"]:
                students = int(2000 * growth * np.random.uniform(0.9, 1.1))
            elif dept in ["Medicine", "Nursing"]:
                students = int(1200 * growth * np.random.uniform(0.9, 1.1))
            else:
                students = int(700 * growth * np.random.uniform(0.9, 1.1))
            
            # Completion rate
            if dept in ["Medicine", "Nursing"]:
                completion = np.random.uniform(85, 95) + (year - 2023) * 1.5
            elif dept in ["Business", "Computing"]:
                completion = np.random.uniform(80, 90) + (year - 2023) * 2
            else:
                completion = np.random.uniform(75, 88) + (year - 2023) * 2
            
            completion = min(completion, 98)
            
            # Graduates
            graduating = int(students * np.random.uniform(0.22, 0.28))
            
            # Learning mode
            if year == 2023:
                mode = np.random.choice(["Physical", "Virtual", "Blended"], p=[0.7, 0.15, 0.15])
            elif year == 2024:
                mode = np.random.choice(["Physical", "Virtual", "Blended"], p=[0.55, 0.25, 0.20])
            else:
                mode = np.random.choice(["Physical", "Virtual", "Blended"], p=[0.4, 0.35, 0.25])
            
            data.append({
                "Year": year,
                "Department": dept,
                "Total_Students": students,
                "Graduating_Students": graduating,
                "Completion_Rate": round(completion, 1),
                "Learning_Mode": mode,
                "Student_Satisfaction": round(np.random.uniform(3.2, 4.8), 1)
            })
    
    return pd.DataFrame(data)

# Financial data - Simplified
@st.cache_data
def load_financial_data():
    years = [2023, 2024, 2025]
    
    financial_data = []
    
    for year in years:
        growth = 1 + (year - 2023) * 0.12
        
        tuition = 800 * growth * np.random.uniform(0.95, 1.05)
        research = 150 * growth * np.random.uniform(0.9, 1.1)
        donations = 50 * growth * np.random.uniform(0.8, 1.2)
        other = 200 * growth * np.random.uniform(0.9, 1.1)
        
        total_revenue = tuition + research + donations + other
        
        salaries = 450 * growth * np.random.uniform(0.95, 1.05)
        infrastructure = 150 * growth * np.random.uniform(0.9, 1.1)
        operations = 200 * growth * np.random.uniform(0.95, 1.05)
        
        total_expenses = salaries + infrastructure + operations
        profit = total_revenue - total_expenses
        
        financial_data.append({
            "Year": year,
            "Tuition_Revenue": round(tuition, 1),
            "Research_Grants": round(research, 1),
            "Donations": round(donations, 1),
            "Other_Income": round(other, 1),
            "Total_Revenue": round(total_revenue, 1),
            "Salaries": round(salaries, 1),
            "Infrastructure": round(infrastructure, 1),
            "Operations": round(operations, 1),
            "Total_Expenses": round(total_expenses, 1),
            "Net_Profit": round(profit, 1)
        })
    
    return pd.DataFrame(financial_data)

# Load data
df = load_data()
df_finance = load_financial_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Dashboard")

years = st.sidebar.multiselect("Select Year(s)", df["Year"].unique(), default=[2023, 2024, 2025])
df_filtered = df[df["Year"].isin(years)]

depts = st.sidebar.multiselect("Select Department(s)", df["Department"].unique(), default=df["Department"].unique()[:6])
df_filtered = df_filtered[df_filtered["Department"].isin(depts)]

modes = st.sidebar.multiselect("Select Learning Mode", df["Learning_Mode"].unique(), default=df["Learning_Mode"].unique())
df_filtered = df_filtered[df_filtered["Learning_Mode"].isin(modes)]

# Key Metrics
st.header("📊 University Overview")

col1, col2, col3, col4, col5 = st.columns(5)

total_students = df_filtered["Total_Students"].sum()
total_graduates = df_filtered["Graduating_Students"].sum()
avg_completion = df_filtered["Completion_Rate"].mean()
avg_satisfaction = df_filtered["Student_Satisfaction"].mean()
total_revenue = df_finance[df_finance["Year"].isin(years)]["Total_Revenue"].sum()

with col1:
    st.metric("👨‍🎓 Total Students", f"{total_students:,}")
with col2:
    st.metric("🎓 Graduates", f"{total_graduates:,}")
with col3:
    st.metric("📈 Completion Rate", f"{avg_completion:.1f}%")
with col4:
    st.metric("⭐ Satisfaction", f"{avg_satisfaction:.1f}/5.0")
with col5:
    st.metric("💰 Revenue", f"KES {total_revenue:.0f}M")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📚 Academics", "🎓 Students", "💰 Finance", "📊 Insights"])

# TAB 1: Academics
with tab1:
    st.subheader("Completion Rate by Department")
    
    completion_data = df_filtered.groupby(["Year", "Department"])["Completion_Rate"].mean().reset_index()
    
    fig1 = px.bar(
        completion_data,
        x="Department",
        y="Completion_Rate",
        color="Year",
        title="Completion Rate by Department (%)",
        barmode="group"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("Learning Mode Distribution")
    mode_data = df_filtered.groupby(["Year", "Learning_Mode"])["Total_Students"].sum().reset_index()
    
    fig2 = px.bar(
        mode_data,
        x="Year",
        y="Total_Students",
        color="Learning_Mode",
        title="Physical vs Virtual vs Blended Learning",
        barmode="stack"
    )
    st.plotly_chart(fig2, use_container_width=True)

# TAB 2: Students
with tab2:
    st.subheader("Student Population by Department")
    
    student_data = df_filtered.groupby(["Year", "Department"])["Total_Students"].sum().reset_index()
    
    fig3 = px.bar(
        student_data,
        x="Department",
        y="Total_Students",
        color="Year",
        title="Student Enrollment by Department",
        barmode="group"
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    st.subheader("Top 10 Courses by Graduates (2025)")
    grad_data = df_filtered[df_filtered["Year"] == 2025].groupby("Department")["Graduating_Students"].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig4 = px.bar(
        grad_data,
        x="Department",
        y="Graduating_Students",
        title="Departments with Highest Graduates (2025)",
        color="Graduating_Students"
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    st.subheader("Fastest Growing Departments")
    growth_data = df_filtered.groupby(["Year", "Department"])["Total_Students"].sum().reset_index()
    growth_2023 = growth_data[growth_data["Year"] == 2023].set_index("Department")["Total_Students"]
    growth_2025 = growth_data[growth_data["Year"] == 2025].set_index("Department")["Total_Students"]
    
    growth_rate = ((growth_2025 - growth_2023) / growth_2023 * 100).sort_values(ascending=False).head(8).reset_index()
    growth_rate.columns = ["Department", "Growth_Percent"]
    
    fig5 = px.bar(
        growth_rate,
        x="Department",
        y="Growth_Percent",
        title="Department Growth Rate (2023-2025)",
        color="Growth_Percent"
    )
    st.plotly_chart(fig5, use_container_width=True)

# TAB 3: Finance
with tab3:
    st.subheader("Revenue and Expenses Trend")
    
    finance_year = df_finance[df_finance["Year"].isin(years)]
    finance_melt = finance_year.melt(id_vars=["Year"], value_vars=["Total_Revenue", "Total_Expenses", "Net_Profit"], var_name="Category", value_name="Amount")
    
    fig6 = px.line(
        finance_melt,
        x="Year",
        y="Amount",
        color="Category",
        title="Revenue, Expenses & Profit (KES Millions)",
        markers=True
    )
    st.plotly_chart(fig6, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue breakdown (latest year)
        rev_2025 = finance_year[finance_year["Year"] == 2025].iloc[0]
        revenue_data = pd.DataFrame({
            "Source": ["Tuition", "Research", "Donations", "Other"],
            "Amount": [rev_2025["Tuition_Revenue"], rev_2025["Research_Grants"], rev_2025["Donations"], rev_2025["Other_Income"]]
        })
        
        fig7 = px.pie(
            revenue_data,
            values="Amount",
            names="Source",
            title=f"Revenue Breakdown (2025)",
            hole=0.3
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    with col2:
        # Expense breakdown
        expense_data = pd.DataFrame({
            "Expense": ["Salaries", "Infrastructure", "Operations"],
            "Amount": [rev_2025["Salaries"], rev_2025["Infrastructure"], rev_2025["Operations"]]
        })
        
        fig8 = px.pie(
            expense_data,
            values="Amount",
            names="Expense",
            title=f"Expense Breakdown (2025)",
            hole=0.3
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    # Financial metrics
    st.subheader("Financial Health")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        profit_margin = (rev_2025["Net_Profit"] / rev_2025["Total_Revenue"]) * 100
        st.metric("Profit Margin", f"{profit_margin:.1f}%")
    
    with col2:
        rev_growth = ((finance_year[finance_year["Year"] == 2025]["Total_Revenue"].values[0] - 
                       finance_year[finance_year["Year"] == 2023]["Total_Revenue"].values[0]) / 
                      finance_year[finance_year["Year"] == 2023]["Total_Revenue"].values[0]) * 100
        st.metric("Revenue Growth (3yr)", f"{rev_growth:.1f}%")
    
    with col3:
        expense_ratio = (rev_2025["Total_Expenses"] / rev_2025["Total_Revenue"]) * 100
        st.metric("Expense Ratio", f"{expense_ratio:.1f}%")

# TAB 4: Insights
with tab4:
    st.subheader("Key Institutional Insights")
    
    # Department ranking
    st.markdown("### 🏆 Department Performance Ranking (2025)")
    dept_2025 = df_filtered[df_filtered["Year"] == 2025].groupby("Department").agg({
        "Completion_Rate": "mean",
        "Student_Satisfaction": "mean"
    }).reset_index()
    dept_2025 = dept_2025.sort_values("Completion_Rate", ascending=False)
    
    st.dataframe(dept_2025, use_container_width=True)
    
    # Top performing departments
    st.markdown("### 🎯 Strategic Recommendations")
    
    recommendations = [
        "**Digital Transformation** - Expand online learning programs to reach 40% of students by 2026",
               "**Research Investment** - Increase research funding by 25% to boost publications and patents",
        "**International Partnerships** - Double international student exchange programs",
        "**Student Support** - Enhance support services for virtual learners to improve completion rates",
        "**Faculty Development** - Invest in faculty training for blended learning methodologies"
    ]
    
    for rec in recommendations:
        st.info(rec)
    
    # Satisfaction vs Completion scatter
    st.markdown("### 📊 Student Satisfaction vs Completion Rate")
    scatter_data = df_filtered.groupby("Department")[["Completion_Rate", "Student_Satisfaction"]].mean().reset_index()
    
    fig9 = px.scatter(
        scatter_data,
        x="Completion_Rate",
        y="Student_Satisfaction",
        text="Department",
        title="Department Performance: Satisfaction vs Completion",
        size="Completion_Rate"
    )
    st.plotly_chart(fig9, use_container_width=True)

# Data Download
st.markdown("---")
st.subheader("📎 Download Data")

csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download Data as CSV", csv, "nova_university_data.csv", "text/csv")

with st.expander("View Raw Data"):
    st.dataframe(df_filtered, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📌 Nova University Dashboard | 2023-2025")
