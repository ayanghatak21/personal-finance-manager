import pandas as pd
from datetime import datetime
import os

class DataManager:
    def __init__(self):
        self.file_path = 'data/transactions.csv'
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['date', 'amount', 'category', 'type'])
            df.to_csv(self.file_path, index=False)

    def add_transaction(self, date, amount, category, type_):
        df = pd.read_csv(self.file_path)
        new_row = pd.DataFrame({
            'date': [date],
            'amount': [amount],
            'category': [category],
            'type': [type_]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.file_path, index=False)

    def get_transactions(self):
        df = pd.read_csv(self.file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_summary(self, period='month'):
        df = self.get_transactions()

        if period == 'week':
            df['period'] = df['date'].dt.isocalendar().week
        elif period == 'month':
            df['period'] = df['date'].dt.month
        else:  # year
            df['period'] = df['date'].dt.year

        # Return full DataFrames instead of series
        expenses = df[df['type'] == 'expense'].groupby(['period', 'category'])['amount'].sum().reset_index()
        income = df[df['type'] == 'income'].groupby(['period', 'category'])['amount'].sum().reset_index()

        return expenses, income