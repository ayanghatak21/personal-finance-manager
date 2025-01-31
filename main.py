import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager
from utils.charts import create_category_summary_chart, create_income_vs_expenses_chart
from assets.category_icons import CATEGORY_ICONS, CATEGORY_COLORS

st.set_page_config(page_title="Personal Finance Manager", layout="wide")

# Initialize data manager
data_manager = DataManager()

# Main title
st.title("💰 Personal Finance Manager")

# Sidebar
st.sidebar.header("Add Transaction")

# Transaction Form
with st.sidebar.form("transaction_form"):
    date = st.date_input("Date", datetime.now())
    amount = st.number_input("Amount ($)", min_value=0.0, format="%f")

    # Category selection with icons using radio buttons
    categories = list(CATEGORY_ICONS.keys())
    selected_category = st.radio(
        "Category",
        categories,
        format_func=lambda x: f"{x} {CATEGORY_ICONS[x]}"
    )

    transaction_type = st.selectbox("Type", ["income", "expense"])

    submit_button = st.form_submit_button("Add Transaction")
    if submit_button and amount > 0:
        data_manager.add_transaction(date, amount, selected_category, transaction_type)
        st.success("Transaction added successfully!")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Transaction History")
    transactions = data_manager.get_transactions()
    if not transactions.empty:
        st.dataframe(
            transactions.sort_values('date', ascending=False),
            use_container_width=True
        )
    else:
        st.info("No transactions yet. Add some using the form!")

with col2:
    st.subheader("Analytics")
    period = st.selectbox("View by", ["week", "month", "year"])

    expenses, income = data_manager.get_summary(period)

    if not expenses.empty:
        expenses_chart = create_category_summary_chart(expenses, period)
        st.plotly_chart(expenses_chart, use_container_width=True)

        total_expenses = expenses.groupby('period')['amount'].sum()
        total_income = income.groupby('period')['amount'].sum()

        income_vs_expenses = create_income_vs_expenses_chart(
            total_income,
            total_expenses,
            period
        )
        st.plotly_chart(income_vs_expenses, use_container_width=True)
    else:
        st.info("Add some transactions to see analytics!")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit | "
    "Track your finances with ease!"
)