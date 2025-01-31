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

# Initialize session state for modal
if 'show_transaction_modal' not in st.session_state:
    st.session_state.show_transaction_modal = False

# Button to open modal
if st.button("➕ Add Transaction", type="primary"):
    st.session_state.show_transaction_modal = True

# Transaction Modal
if st.session_state.show_transaction_modal:
    with st.form("transaction_form", clear_on_submit=True):
        st.subheader("Add New Transaction")

        date = st.date_input("Date", datetime.now())
        amount = st.number_input("Amount ($)", min_value=0.0, format="%f")

        # Category selection with larger icons in a grid
        st.write("#### Select Category")
        categories = list(CATEGORY_ICONS.keys())
        cols = st.columns(3)  # Create 3 columns for the grid

        # Style for category icons
        icon_style = '''
        <style>
            .category-icon { font-size: 2em; margin-bottom: 5px; }
            .category-label { font-size: 1em; }
        </style>
        '''
        st.markdown(icon_style, unsafe_allow_html=True)

        # Display categories in a grid
        selected_category = st.radio(
            "Category",
            categories,
            format_func=lambda x: f'''
            <div style="text-align: center">
                <div class="category-icon">{CATEGORY_ICONS[x]}</div>
                <div class="category-label">{x}</div>
            </div>
            ''',
            horizontal=True,
            label_visibility="collapsed"
        )

        transaction_type = st.selectbox("Type", ["income", "expense"])

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Add", type="primary", use_container_width=True):
                if amount > 0:
                    data_manager.add_transaction(date, amount, selected_category, transaction_type)
                    st.success("Transaction added successfully!")
                    st.session_state.show_transaction_modal = False
                    st.experimental_rerun()
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.show_transaction_modal = False
                st.experimental_rerun()

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
        st.info("No transactions yet. Add some using the '➕ Add Transaction' button!")

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