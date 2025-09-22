import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime, os

expense_file = "expenses.csv"

st.title("💰 Expense Tracker App")

# ---- Add New Expense ----
st.header("➕ Add Expense")
name = st.text_input("Expense Name")
amount = st.number_input("Amount (₹)", min_value=0.0)
category = st.selectbox("Category", ["Food", "Home", "Work", "Fun", "Misc"])
date = st.date_input("Date", datetime.date.today())

if st.button("Save Expense"):
    file_exists = os.path.exists(expense_file)
    with open(expense_file, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("Name,Amount,Category,Date\n")
        f.write(f"{name},{amount},{category},{date}\n")
    st.success("Expense Saved!")

# ---- Show Data ----
if os.path.exists(expense_file):
    df = pd.read_csv(expense_file)
    st.header("📊 Expense Summary")
    st.dataframe(df)

    total_spent = df["Amount"].sum()
    st.write(f"### Total Spent: ₹{total_spent:.2f}")

    # Category Pie Chart
    st.subheader("By Category")
    fig1, ax1 = plt.subplots()
    df.groupby("Category")["Amount"].sum().plot.pie(autopct="%1.1f%%", ax=ax1)
    st.pyplot(fig1)

    # Monthly Trend
    st.subheader("Monthly Trend")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    fig2, ax2 = plt.subplots()
    df.groupby("Month")["Amount"].sum().plot.bar(ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
