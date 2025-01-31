import plotly.express as px
import plotly.graph_objects as go
from assets.category_icons import CATEGORY_COLORS

def create_category_summary_chart(expenses, period_type='month'):
    period_labels = {
        'week': 'Week',
        'month': 'Month',
        'year': 'Year'
    }

    fig = px.bar(
        expenses,
        x='period',
        y='amount',
        color='category',
        title=f'Expenses by Category per {period_labels[period_type]}',
        color_discrete_map=CATEGORY_COLORS,
        barmode='group'
    )

    fig.update_layout(
        xaxis_title=period_labels[period_type],
        yaxis_title="Amount ($)",
        showlegend=True,
        plot_bgcolor='white'
    )

    return fig

def create_income_vs_expenses_chart(income, expenses, period_type='month'):
    fig = go.Figure()

    # Add income line
    fig.add_trace(go.Scatter(
        x=income.index,
        y=income.values,
        name='Income',
        line=dict(color='#28a745', width=2)
    ))

    # Add expenses line
    fig.add_trace(go.Scatter(
        x=expenses.index,
        y=expenses.values,
        name='Expenses',
        line=dict(color='#dc3545', width=2)
    ))

    fig.update_layout(
        title=f'Income vs Expenses per {period_type.capitalize()}',
        xaxis_title=period_type.capitalize(),
        yaxis_title="Amount ($)",
        plot_bgcolor='white',
        hovermode='x'
    )

    return fig