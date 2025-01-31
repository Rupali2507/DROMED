from flask import Flask, jsonify, request
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Load inventory data from CSV file
def load_inventory_data():
    try:
        data = []
        with open('datasets/dromed_inventory_data.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Convert numerical values for consistency
                row['Current_Stock'] = int(row['Current_Stock'])
                row['Avg_Daily_Usage'] = float(row['Avg_Daily_Usage'])
                row['Reorder_Point'] = int(row['Reorder_Point'])
                row['Unit_Price'] = float(row['Unit_Price'])
                data.append(row)
        return data
    except FileNotFoundError:
        print("Error: CSV file not found!")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

inventory_data = load_inventory_data()

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the DroMed Inventory API!"}), 200

# Get all inventory data
@app.route('/api/inventory', methods=['GET'])
def get_all_inventory():
    return jsonify(inventory_data), 200

# Search inventory by product name
@app.route('/api/inventory/search', methods=['GET'])
def search_inventory():
    search_term = request.args.get('item', '').lower()

    if not search_term:
        return jsonify({"error": "No search term provided"}), 400

    # Search for products containing the search term
    results = [item for item in inventory_data if search_term in item['Product'].lower()]

    if results:
        return jsonify(results), 200
    else:
        return jsonify({"message": "No items found matching the search term."}), 404

# Filter inventory by category, supplier, or storage location
@app.route('/api/inventory/filter', methods=['GET'])
def filter_inventory():
    category = request.args.get('category', '').lower()
    supplier = request.args.get('supplier', '').lower()
    location = request.args.get('location', '').lower()

    # Filter based on the query parameters
    results = [
        item for item in inventory_data
        if (category in item['Category'].lower() if category else True) and
           (supplier in item['Supplier'].lower() if supplier else True) and
           (location in item['Storage_Location'].lower() if location else True)
    ]

    if results:
        return jsonify(results), 200
    else:
        return jsonify({"message": "No items found matching the filter criteria."}), 404

# Get paginated inventory data
@app.route('/api/inventory/paginated', methods=['GET'])
def get_paginated_inventory():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        if page < 1 or per_page < 1:
            return jsonify({"error": "Page and per_page must be positive integers"}), 400
    except ValueError:
        return jsonify({"error": "Invalid input for page or per_page"}), 400

    # Calculate start and end indices
    start = (page - 1) * per_page
    end = start + per_page

    # Paginate inventory data
    paginated_data = inventory_data[start:end]

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total_items": len(inventory_data),
        "data": paginated_data
    }), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
