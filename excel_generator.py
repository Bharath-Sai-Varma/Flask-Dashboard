import pandas as pd
import numpy as np
import random

# Generate a richer dataset
regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Furniture", "Clothing", "Groceries"]
subcategories = {
    "Electronics": ["Mobiles", "Laptops", "TVs"],
    "Furniture": ["Chairs", "Tables", "Sofas"],
    "Clothing": ["Shirts", "Pants", "Shoes"],
    "Groceries": ["Fruits", "Snacks", "Drinks"]
}

data = []
for _ in range(200):
    cat = random.choice(categories)
    data.append({
        "Date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=random.randint(0, 300)),
        "Region": random.choice(regions),
        "Category": cat,
        "Sub-Category": random.choice(subcategories[cat]),
        "Sales": random.randint(500, 8000),
        "Profit": random.randint(-500, 2000),
        "Quantity": random.randint(1, 20)
    })

df = pd.DataFrame(data)
excel_path = "sales_data.xlsx"
df.to_excel(excel_path, index=False)
excel_path
