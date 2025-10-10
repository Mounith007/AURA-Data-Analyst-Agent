#!/usr/bin/env python3
"""
Test script to verify Parquet support in AURA file upload system
"""

import pandas as pd
import numpy as np
from pathlib import Path

def create_test_parquet_file():
    """Create a sample Parquet file for testing"""
    
    # Create sample data
    np.random.seed(42)
    data = {
        'id': range(1, 1001),
        'name': [f'Customer_{i}' for i in range(1, 1001)],
        'age': np.random.randint(18, 80, 1000),
        'salary': np.random.normal(50000, 15000, 1000).round(2),
        'department': np.random.choice(['Sales', 'Marketing', 'Engineering', 'HR', 'Finance'], 1000),
        'join_date': pd.date_range('2020-01-01', '2024-12-31', periods=1000),
        'is_active': np.random.choice([True, False], 1000, p=[0.8, 0.2]),
        'performance_score': np.random.uniform(1.0, 5.0, 1000).round(2)
    }
    
    df = pd.DataFrame(data)
    
    # Create test files directory
    test_dir = Path(__file__).parent.parent / "data" / "test_files"
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as Parquet with compression
    parquet_path = test_dir / "sample_employees.parquet"
    df.to_parquet(parquet_path, compression='snappy', index=False)
    
    print(f"✅ Created test Parquet file: {parquet_path}")
    print(f"📊 Data shape: {df.shape}")
    print(f"💾 File size: {parquet_path.stat().st_size / 1024:.2f} KB")
    
    # Show data types and first few rows
    print("\n📋 Data Info:")
    print(df.dtypes)
    print("\n🔍 Sample Data:")
    print(df.head())
    
    return parquet_path

def create_test_files():
    """Create multiple test files in different formats for comparison"""
    
    # Same data in different formats
    np.random.seed(42)
    data = {
        'product_id': range(1, 101),
        'product_name': [f'Product_{i}' for i in range(1, 101)],
        'category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], 100),
        'price': np.random.uniform(10.0, 500.0, 100).round(2),
        'stock': np.random.randint(0, 1000, 100),
        'rating': np.random.uniform(1.0, 5.0, 100).round(1)
    }
    
    df = pd.DataFrame(data)
    
    test_dir = Path(__file__).parent.parent / "data" / "test_files"
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Save in different formats
    files_created = {}
    
    # Parquet (compressed)
    parquet_path = test_dir / "products.parquet"
    df.to_parquet(parquet_path, compression='snappy', index=False)
    files_created['parquet'] = parquet_path.stat().st_size
    
    # CSV
    csv_path = test_dir / "products.csv"
    df.to_csv(csv_path, index=False)
    files_created['csv'] = csv_path.stat().st_size
    
    # JSON
    json_path = test_dir / "products.json"
    df.to_json(json_path, orient='records', indent=2)
    files_created['json'] = json_path.stat().st_size
    
    # Excel
    excel_path = test_dir / "products.xlsx"
    df.to_excel(excel_path, index=False)
    files_created['xlsx'] = excel_path.stat().st_size
    
    print("\n📂 File Size Comparison:")
    for format_name, size in files_created.items():
        print(f"{format_name.upper()}: {size / 1024:.2f} KB")
    
    # Calculate compression ratio
    parquet_size = files_created['parquet']
    csv_size = files_created['csv']
    
    if parquet_size < csv_size:
        compression_ratio = (csv_size - parquet_size) / csv_size * 100
        print(f"\n🗜️ Parquet vs CSV: {compression_ratio:.1f}% smaller")
    else:
        size_increase = (parquet_size - csv_size) / csv_size * 100
        print(f"\n📊 Parquet vs CSV: {size_increase:.1f}% larger (expected for small datasets due to metadata overhead)")
        print("   💡 Parquet becomes more efficient with larger datasets (>10k rows)")
    
    return test_dir

if __name__ == "__main__":
    print("🧪 Creating test files for AURA Parquet support...")
    
    # Create individual test files
    parquet_file = create_test_parquet_file()
    
    # Create comparison files
    test_dir = create_test_files()
    
    print(f"\n✅ Test files created in: {test_dir}")
    print("\n📝 Next steps:")
    print("1. Start the AURA API Gateway: python api_gateway/main.py")
    print("2. Start the frontend: npm run dev")
    print("3. Upload the test Parquet files through the UI")
    print("4. Verify Parquet files are processed correctly")
    
    print("\n🔗 API Endpoints to test:")
    print("GET  http://localhost:8000/files/supported-formats")
    print("POST http://localhost:8000/files/upload")
    print("GET  http://localhost:8000/files")