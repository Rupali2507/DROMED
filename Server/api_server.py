from flask import Flask, jsonify, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Load the inventory dataset
def load_inventory():
    dataset_path = os.path.join(os.path.dirname(__file__), 'datasets', 'dromed_inventory_data.csv')
    return pd.read_csv(dataset_path)

# API route to get the entire inventory
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    inventory = load_inventory()
    return jsonify(inventory.to_dict(orient='records'))

# API route to search for a specific item
@app.route('/api/inventory/search', methods=['GET'])
def search_inventory():
    query = request.args.get('item', '').lower()
    inventory = load_inventory()
    result = inventory[inventory['Product'].str.lower().str.contains(query)]
    return jsonify(result.to_dict(orient='records'))

# API route to get low stock items
@app.route('/api/inventory/low-stock', methods=['GET'])
def get_low_stock():
    inventory = load_inventory()
    inventory['Remaining_Days'] = (inventory['Current_Stock'] / inventory['Avg_Daily_Usage']).round(1)
    low_stock = inventory[inventory['Remaining_Days'] < 7]
    return jsonify(low_stock.to_dict(orient='records'))

# API route to update stock levels
@app.route('/api/inventory/update', methods=['POST'])
def update_stock_levels():
    data = request.get_json()
    inventory = load_inventory()
    
    for item in data:
        product = item['product']
        new_stock = item['new_stock']
        inventory.loc[inventory['Product'] == product, 'Current_Stock'] = new_stock
        inventory.loc[inventory['Product'] == product, 'Last_Restock_Date'] = datetime.now().strftime('%Y-%m-%d')
    
    inventory.to_csv(os.path.join(os.path.dirname(__file__), 'datasets', 'dromed_inventory_data.csv'), index=False)
    return jsonify({'message': 'Inventory updated successfully.'})

if __name__ == '__main__':
    app.run(debug=True)