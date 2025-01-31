import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager
from utils.charts import create_category_summary_chart, create_income_vs_expenses_chart
from utils.custom_categories import CustomCategoryManager
from assets.category_icons import CATEGORY_ICONS, CATEGORY_COLORS

st.set_page_config(page_title="Personal Finance Manager", layout="wide")

# Initialize managers
data_manager = DataManager()
custom_category_manager = CustomCategoryManager()

# Main title
st.title("💰 Personal Finance Manager")

# Initialize session states
if 'show_transaction_modal' not in st.session_state:
    st.session_state.show_transaction_modal = False
if 'show_custom_category_modal' not in st.session_state:
    st.session_state.show_custom_category_modal = False
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# Button to open modal
if st.button("➕ Add Transaction", type="primary"):
    st.session_state.show_transaction_modal = True

# Custom Category Modal
if st.session_state.show_custom_category_modal:
    st.subheader("Create Custom Category")
    with st.form("custom_category_form", clear_on_submit=True):
        category_name = st.text_input("Category Name")
        # Simplified color picker
        color = st.color_picker("Category Color", "#FF0000")
        # Use a default icon for custom categories
        default_icon = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/></svg>'''

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Create", type="primary", use_container_width=True):
                if category_name:
                    custom_category_manager.add_custom_category(
                        category_name, default_icon, color
                    )
                    st.success(f"Category '{category_name}' created!")
                    st.session_state.show_custom_category_modal = False
                    st.rerun()
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.show_custom_category_modal = False
                st.rerun()

# Transaction Modal
if st.session_state.show_transaction_modal:
    st.subheader("Add New Transaction")

    # Style for category icons
    st.markdown("""
    <style>
        button[kind="secondary"] {
            background: none;
            border: 2px solid #f0f2f6;
            border-radius: 10px;
            padding: 20px 10px;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }
        button[kind="secondary"]:hover {
            border-color: #0066cc;
            transform: translateY(-2px);
        }
        .category-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #262730;
        }
        .category-label {
            font-size: 0.9em;
            margin-top: 5px;
            color: #262730;
        }
    </style>
    """, unsafe_allow_html=True)

    # Category selection grid
    st.write("#### Select Category")

    # Combine built-in and custom categories
    custom_categories = custom_category_manager.get_custom_categories()
    all_categories = {**CATEGORY_ICONS, **{name: data['icon'] for name, data in custom_categories.items()}}

    categories = list(all_categories.keys())
    cols = st.columns(3)

    # Add custom category button first
    with cols[0]:
        if st.button(
            "➕ Create Category",
            key="create_category",
            help="Create a new custom category",
            type="secondary",
            use_container_width=True
        ):
            st.session_state.show_custom_category_modal = True
            st.rerun()

    # Display all categories
    for idx, category in enumerate(categories, start=1):
        with cols[idx % 3]:
            if st.button(
                category,
                key=f"cat_{category}",
                help=f"Select {category}",
                type="secondary",
                use_container_width=True
            ):
                st.session_state.selected_category = category

            # Display icon
            icon = all_categories[category]
            st.markdown(f"""
                <div style="text-align: center; margin-top: -60px; pointer-events: none;">
                    {icon}
                </div>
            """, unsafe_allow_html=True)

    if st.session_state.selected_category:
        st.markdown(f"""
        <div style='text-align: center; margin: 10px 0;'>
            Selected: <b>{st.session_state.selected_category}</b>
        </div>
        """, unsafe_allow_html=True)

    # Transaction form
    with st.form("transaction_form", clear_on_submit=True):
        date = st.date_input("Date", datetime.now())
        amount = st.number_input("Amount ($)", min_value=0.0, format="%f")
        transaction_type = st.selectbox("Type", ["income", "expense"])

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Add", type="primary", use_container_width=True):
                if amount > 0 and st.session_state.selected_category:
                    data_manager.add_transaction(
                        date, amount, st.session_state.selected_category, transaction_type
                    )
                    st.success("Transaction added successfully!")
                    st.session_state.show_transaction_modal = False
                    st.session_state.selected_category = None
                    st.rerun()
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.show_transaction_modal = False
                st.session_state.selected_category = None
                st.rerun()

# Rest of the main content 
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

        # Calculate totals by period
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