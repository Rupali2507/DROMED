import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path

class DroneInventoryManager:
    def __init__(self, data_file="Server/datasets/dromed_inventory_data.csv"):
        """Initialize the inventory manager with data file path."""
        self.data_file = data_file
        self.load_data()
        
    def load_data(self):
        """Load inventory data from CSV file."""
        try:
            self.data = pd.read_csv(self.data_file)
            self.data['Last_Restock_Date'] = pd.to_datetime(self.data['Last_Restock_Date'])
            print(f"Successfully loaded {len(self.data)} inventory items.")
        except FileNotFoundError:
            print(f"Error: {self.data_file} not found. Please generate inventory data first.")
            self.data = None

    def analyze_stock_levels(self, critical_days=7, warning_days=14):
        """Analyze current stock levels and identify items needing attention."""
        if self.data is None:
            return None
            
        # Calculate remaining days of stock
        self.data['Remaining_Days'] = (
            self.data['Current_Stock'] / self.data['Avg_Daily_Usage']
        ).round(1)
        
        # Categorize items by urgency
        self.data['Status'] = 'OK'
        self.data.loc[self.data['Remaining_Days'] <= warning_days, 'Status'] = 'Warning'
        self.data.loc[self.data['Remaining_Days'] <= critical_days, 'Status'] = 'Critical'
        
        return {
            'critical': self.data[self.data['Status'] == 'Critical'],
            'warning': self.data[self.data['Status'] == 'Warning'],
            'ok': self.data[self.data['Status'] == 'OK']
        }

    def generate_restock_report(self):
        """Generate a report of items needing restock."""
        if self.data is None:
            return None
            
        restock_needed = self.data[self.data['Current_Stock'] <= self.data['Reorder_Point']]
        
        restock_report = restock_needed.assign(
            Quantity_To_Order=lambda x: (
                (x['Reorder_Point'] * 2) - x['Current_Stock']
            ).astype(int),
            Estimated_Cost=lambda x: x['Quantity_To_Order'] * x['Unit_Price']
        )
        
        return restock_report[['Product', 'Category', 'Current_Stock', 
                             'Reorder_Point', 'Quantity_To_Order', 
                             'Unit_Price', 'Estimated_Cost', 'Supplier']]

    def get_category_summary(self):
        """Generate summary statistics by category."""
        if self.data is None:
            return None
            
        return self.data.groupby('Category').agg({
            'Current_Stock': 'sum',
            'Unit_Price': 'mean',
            'Product': 'count'
        }).round(2)

    def save_reports(self, output_dir="reports"):
        """Save all reports to CSV files."""
        if self.data is None:
            return
            
        # Create reports directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate timestamp for file names
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        # Save various reports
        stock_levels = self.analyze_stock_levels()
        restock_report = self.generate_restock_report()
        category_summary = self.get_category_summary()
        
        # Save full inventory status
        self.data.to_csv(f"{output_dir}/full_inventory_{timestamp}.csv", index=False)
        
        # Save critical items
        if not stock_levels['critical'].empty:
            stock_levels['critical'].to_csv(
                f"{output_dir}/critical_items_{timestamp}.csv", index=False)
        
        # Save restock report
        if not restock_report.empty:
            restock_report.to_csv(
                f"{output_dir}/restock_order_{timestamp}.csv", index=False)
        
        # Save category summary
        category_summary.to_csv(f"{output_dir}/category_summary_{timestamp}.csv")
        
        print(f"Reports saved in {output_dir} directory")

def main():
    """Main function to run the inventory management system."""
    # Initialize the inventory manager
    manager = DroneInventoryManager()
    
    # Analyze stock levels
    stock_status = manager.analyze_stock_levels()
    if stock_status:
        print("\nInventory Status Summary:")
        print(f"Critical Items: {len(stock_status['critical'])}")
        print(f"Warning Items: {len(stock_status['warning'])}")
        print(f"OK Items: {len(stock_status['ok'])}")
        
        # Display critical items
        if not stock_status['critical'].empty:
            print("\nCritical Items (Need Immediate Attention):")
            print(stock_status['critical'][['Product', 'Current_Stock', 
                                          'Remaining_Days', 'Supplier']])
    
    # Generate and display restock report
    restock_report = manager.generate_restock_report()
    if restock_report is not None and not restock_report.empty:
        print("\nRestock Order Recommendations:")
        print(restock_report)
        
        total_cost = restock_report['Estimated_Cost'].sum()
        print(f"\nTotal Estimated Restock Cost: ${total_cost:,.2f}")
    
    # Save all reports
    manager.save_reports()

if __name__ == "__main__":
    main()