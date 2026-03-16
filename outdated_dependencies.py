"""
Test file with potentially outdated third-party library APIs.
"""
import requests
from flask import Flask, request
import pandas as pd


app = Flask(__name__)


def fetch_data_old_style():
    """Using older requests patterns that might be flagged"""
    # Using verify=False without proper context - security issue in older patterns
    response = requests.get('https://api.example.com/data', verify=False)
    return response.json()


@app.route('/user/<user_id>')
def get_user(user_id):
    """Flask route that might use outdated patterns"""
    # Using request.args.get without validation - older pattern
    page = request.args.get('page')
    limit = request.args.get('limit')
    
    return {'user_id': user_id, 'page': page, 'limit': limit}


def process_dataframe():
    """Using potentially deprecated pandas methods"""
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    
    # append() was deprecated in pandas 2.0
    new_row = pd.DataFrame({'A': [7], 'B': [8]})
    df = df.append(new_row, ignore_index=True)
    
    return df


def read_excel_old_format():
    """Using older pandas Excel reading patterns"""
    # Using deprecated engine parameter or methods
    df = pd.read_excel('data.xlsx', sheetname='Sheet1')  # 'sheetname' deprecated in pandas 0.21
    return df


class DataProcessor:
    """Class using older patterns that might need verification"""
    
    def __init__(self):
        self.data = []
    
    def process(self):
        """Using older list comprehension patterns"""
        # This is fine, but automated tools might flag it
        result = [x for x in self.data if x is not None]
        return result


if __name__ == "__main__":
    print(fetch_data_old_style())
    print(process_dataframe())
