import streamlit as st
import pandas as pd
import os

expense_file = "expenses.csv"

st.title("💰 Expense Tracker App")

# ---- Add New Expense ----
st.header("➕ Add Expense")
name = st.text_input("Expense Name")
amount = st.number_input("Amount (₹)", min_value=0.0)
category = st.selectbox("Category", ["Food", "Home", "Work", "Fun", "Misc"])
# Use pandas to get today's date
date = st.date_input("Date", pd.Timestamp("today"))

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

    # Expenses by category (text only)
    st.subheader("By Category")
    category_totals = df.groupby("Category")["Amount"].sum()
    for cat, amt in category_totals.items():
        st.write(f"{cat}: ₹{amt:.2f}")

    # Monthly Trend (text only)
    st.subheader("Monthly Trend")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    monthly_totals = df.groupby("Month")["Amount"].sum()
    for month, amt in monthly_totals.items():
        st.write(f"{month}: ₹{amt:.2f}")
