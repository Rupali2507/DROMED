from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Medical supply categories and items
MEDICAL_SUPPLIES = {
    "Medications": [
        "Amoxicillin 500mg", "Ibuprofen 400mg", "Paracetamol 500mg", 
        "Aspirin 325mg", "Omeprazole 20mg", "Metformin 850mg",
        "Amlodipine 5mg", "Cetirizine 10mg", "Azithromycin 250mg",
        "Insulin Regular 100ml"
    ],
    "First Aid": [
        "Adhesive Bandages", "Gauze Rolls", "Medical Tape",
        "Elastic Bandages", "Wound Dressing", "Cotton Swabs",
        "Antiseptic Wipes", "Burn Dressing", "Compression Bandages",
        "Surgical Gloves"
    ],
    "Emergency Supplies": [
        "Emergency Saline 500ml", "Blood Collection Tubes",
        "IV Start Kits", "Syringes 5ml", "Oxygen Masks",
        "Emergency Blankets", "Cold Packs", "Hot Packs",
        "Splints", "cervical collars"
    ],
    "Medical Devices": [
        "Blood Glucose Meters", "Digital Thermometers",
        "Pulse Oximeters", "Blood Pressure Cuffs",
        "Nebulizer Sets", "Stethoscopes", "First Aid Kits",
        "Pregnancy Test Kits", "Hand Sanitizers"
    ]
}

# Supplier companies specializing in medical supplies
MEDICAL_SUPPLIERS = [
    "MedLine Industries", "Cardinal Health", "McKesson Medical",
    "Henry Schein Medical", "Owens & Minor", "BD Medical",
    "Baxter Healthcare", "Abbott Medical", "Johnson & Johnson Medical",
    "Boston Scientific"
]

def generate_mock_inventory_data(num_records):
    data = []
    current_date = datetime.now()
    
    # Generate a balanced number of items from each category
    items_per_category = num_records // len(MEDICAL_SUPPLIES)
    
    for category, items in MEDICAL_SUPPLIES.items():
        for _ in range(items_per_category):
            product = random.choice(items)
            
            # Realistic stock levels based on item type
            if "mg" in product or "ml" in product:  # Medications
                current_stock = random.randint(100, 1000)
                avg_daily_usage = random.randint(5, 50)
            elif category == "Medical Devices":
                current_stock = random.randint(10, 100)
                avg_daily_usage = random.randint(1, 5)
            else:  # First Aid and Emergency Supplies
                current_stock = random.randint(50, 500)
                avg_daily_usage = random.randint(3, 20)
            
            # Generate realistic restock date
            days_ago = random.randint(1, 30)
            last_restock_date = current_date - timedelta(days=days_ago)
            
            # Calculate reorder point (2 weeks supply)
            reorder_point = avg_daily_usage * 14
            
            # Generate unit price based on category
            if category == "Medical Devices":
                unit_price = round(random.uniform(50.0, 500.0), 2)
            elif category == "Medications":
                unit_price = round(random.uniform(5.0, 100.0), 2)
            else:
                unit_price = round(random.uniform(2.0, 50.0), 2)
            
            data.append({
                "Product": product,
                "Category": category,
                "Current_Stock": current_stock,
                "Avg_Daily_Usage": avg_daily_usage,
                "Reorder_Point": reorder_point,
                "Unit_Price": unit_price,
                "Last_Restock_Date": last_restock_date.strftime("%Y-%m-%d"),
                "Supplier": random.choice(MEDICAL_SUPPLIERS),
                "Storage_Location": f"Zone-{random.choice('ABCD')}{random.randint(1,20)}"
            })
    
    return data

# Generate dataset
num_records = 100  # Increased for better variety
mock_data = generate_mock_inventory_data(num_records)

# Convert to DataFrame and save to CSV
df = pd.DataFrame(mock_data)
df.to_csv("dromed_inventory_data.csv", index=False)
print("Mock medical inventory data saved to dromed_inventory_data.csv")

# Display first few records and basic statistics
print("\nSample of generated data:")
print(df.head())
print("\nDataset Statistics:")
print(df.groupby('Category').size())