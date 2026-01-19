import requests
import json

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    Handles pagination/limits (fetches 100 products as per requirement).
    
    Returns:
        list: List of product dictionaries from API.
    """
    url = 'https://dummyjson.com/products?limit=100'
    print(f"Fetching data from API: {url}...")
    
    try:
        response = requests.get(url, timeout=10) # 10s timeout to prevent hanging
        
        # Check if request was successful (Status Code 200)
        response.raise_for_status()
        
        data = response.json()
        products = data.get('products', [])
        
        print(f"Successfully fetched {len(products)} products from API.")
        return products
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: Failed to fetch products. Reason: {e}")
        return []
    except json.JSONDecodeError:
        print("API Error: Invalid JSON response.")
        return []

def create_product_mapping(api_products):
    """
    Creates a lookup dictionary (mapping) for fast access.
    Key: Product ID (int), Value: Product Details (dict).
    """
    mapping = {}
    for prod in api_products:
        p_id = prod.get('id')
        if p_id:
            mapping[p_id] = {
                'title': prod.get('title'),
                'category': prod.get('category'),
                'brand': prod.get('brand'),
                'rating': prod.get('rating')
            }
    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data by merging with API product info.
    """
    enriched_data = []
    
    print("Enriching sales data with API details...")
    
    for txn in transactions:
        # Create a copy to avoid modifying original list
        new_txn = txn.copy()
        
        # Extract ID: "P109" -> "109" -> 109
        prod_id_str = txn['ProductID']
        
        api_match = False
        # Default values
        new_txn['API_Category'] = 'None'
        new_txn['API_Brand'] = 'None'
        new_txn['API_Rating'] = 0.0
        
        try:
            # Remove 'P' or other non-digit chars
            clean_id_str = ''.join(filter(str.isdigit, prod_id_str))
            
            if clean_id_str:
                prod_id = int(clean_id_str)
                
                # Check mapping
                if prod_id in product_mapping:
                    info = product_mapping[prod_id]
                    new_txn['API_Category'] = info['category']
                    new_txn['API_Brand'] = info['brand']
                    new_txn['API_Rating'] = info['rating']
                    api_match = True
                    
        except ValueError:
            pass 
            
        new_txn['API_Match'] = api_match
        enriched_data.append(new_txn)
        
    return enriched_data

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves the enriched dataset to a new pipe-delimited file.
    """
    if not enriched_transactions:
        print("No data to save.")
        return

    print(f"Saving enriched data to {filename}...")
    
    # Define Header
    header = [
        "TransactionID", "Date", "ProductID", "ProductName", 
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write Header
            f.write('|'.join(header) + '\n')
            
            # Write Rows
            for txn in enriched_transactions:
                row = [
                    str(txn.get('TransactionID', '')),
                    str(txn.get('Date', '')),
                    str(txn.get('ProductID', '')),
                    str(txn.get('ProductName', '')),
                    str(txn.get('Quantity', '')),
                    str(txn.get('UnitPrice', '')),
                    str(txn.get('CustomerID', '')),
                    str(txn.get('Region', '')),
                    # New Fields
                    str(txn.get('API_Category', 'None')),
                    str(txn.get('API_Brand', 'None')),
                    str(txn.get('API_Rating', 0.0)),
                    str(txn.get('API_Match', False))
                ]
                f.write('|'.join(row) + '\n')
                
        print("File saved successfully.")
        
    except IOError as e:
        print(f"Error saving file: {e}")