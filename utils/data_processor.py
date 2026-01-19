from datetime import datetime

# --- PART 1: PARSING & FILTERING (Previous Task) ---

def parse_transactions(raw_lines):
    """Parses raw lines into dictionaries."""
    parsed_data = []
    for line in raw_lines:
        try:
            parts = line.split('|')
            if len(parts) != 8: continue
            
            record = {
                'TransactionID': parts[0].strip(),
                'Date': parts[1].strip(),
                'ProductID': parts[2].strip(),
                'ProductName': parts[3].strip().replace(',', ''),
                'Quantity': int(parts[4].strip().replace(',', '')),
                'UnitPrice': float(parts[5].strip().replace(',', '')),
                'CustomerID': parts[6].strip(),
                'Region': parts[7].strip()
            }
            parsed_data.append(record)
        except (ValueError, IndexError):
            continue
    return parsed_data

def validate_and_filter_data(transactions, region=None, min_amount=None, max_amount=None):
    """Validates and filters data."""
    valid_txns = []
    invalid_count = 0
    
    # Track stats for summary
    total_input = len(transactions)
    filtered_region = 0
    filtered_amount = 0

    for txn in transactions:
        # Validation
        if txn['Quantity'] <= 0 or txn['UnitPrice'] <= 0:
            invalid_count += 1
            continue
        if not txn['Region'] or not txn['CustomerID']:
            invalid_count += 1
            continue
        if not txn['TransactionID'].startswith('T'):
            invalid_count += 1
            continue
            
        # Filter Region
        if region and txn['Region'].lower() != region.lower():
            filtered_region += 1
            continue
            
        # Filter Amount
        total = txn['Quantity'] * txn['UnitPrice']
        if min_amount is not None and total < min_amount:
            filtered_amount += 1
            continue
        if max_amount is not None and total > max_amount:
            filtered_amount += 1
            continue
            
        valid_txns.append(txn)
        
    summary = {
        'total_input': total_input,
        'invalid_records': invalid_count,
        'filtered_by_region': filtered_region,
        'filtered_by_amount': filtered_amount,
        'final_count': len(valid_txns)
    }
    return valid_txns, invalid_count, summary

# --- PART 2: DATA ANALYSIS FUNCTIONS (New Task) ---

def calculate_total_revenue(transactions):
    """Calculates total revenue from all transactions."""
    total_revenue = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    return total_revenue

def region_wise_sales(transactions):
    """
    Analyzes sales by region.
    Returns: Dict with sales, count, and percentage per region.
    """
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)
    
    # 1. Aggregate Data
    for t in transactions:
        r = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        
        if r not in region_stats:
            region_stats[r] = {'total_sales': 0.0, 'transaction_count': 0}
        
        region_stats[r]['total_sales'] += amount
        region_stats[r]['transaction_count'] += 1
        
    # 2. Calculate Percentage & Format
    final_stats = {}
    for r, stats in region_stats.items():
        percent = (stats['total_sales'] / total_revenue) * 100 if total_revenue > 0 else 0
        final_stats[r] = {
            'total_sales': round(stats['total_sales'], 2),
            'transaction_count': stats['transaction_count'],
            'percentage': round(percent, 2)
        }
        
    # 3. Sort by total_sales descending (convert to list of tuples for sorting or keep dict)
    # Returning dict as requested, but standard practice suggests ordered output.
    # Python 3.7+ dicts maintain insertion order.
    sorted_stats = dict(sorted(final_stats.items(), key=lambda item: item[1]['total_sales'], reverse=True))
    
    return sorted_stats

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    Returns: List of tuples (ProductName, TotalQuantity, TotalRevenue).
    """
    product_map = {}
    
    for t in transactions:
        p_name = t['ProductName']
        qty = t['Quantity']
        rev = qty * t['UnitPrice']
        
        if p_name not in product_map:
            product_map[p_name] = {'qty': 0, 'rev': 0.0}
        
        product_map[p_name]['qty'] += qty
        product_map[p_name]['rev'] += rev
        
    # Convert to list
    product_list = [
        (name, data['qty'], round(data['rev'], 2)) 
        for name, data in product_map.items()
    ]
    
    # Sort by Quantity Descending
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    return product_list[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    Returns: Dict of customer statistics.
    """
    cust_stats = {}
    
    for t in transactions:
        c_id = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        prod = t['ProductName']
        
        if c_id not in cust_stats:
            cust_stats[c_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set() # Using set for unique products
            }
            
        cust_stats[c_id]['total_spent'] += amount
        cust_stats[c_id]['purchase_count'] += 1
        cust_stats[c_id]['products_bought'].add(prod)
        
    # Format Output
    final_stats = {}
    for c_id, data in cust_stats.items():
        final_stats[c_id] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(data['total_spent'] / data['purchase_count'], 2),
            'products_bought': list(data['products_bought'])
        }
        
    # Sort by total_spent descending
    return dict(sorted(final_stats.items(), key=lambda item: item[1]['total_spent'], reverse=True))

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns: Dictionary sorted by date with revenue, count, and unique customers.
    """
    daily_stats = {}
    
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        cust = t['CustomerID']
        
        if date not in daily_stats:
            daily_stats[date] = {'revenue': 0.0, 'txns': 0, 'customers': set()}
            
        daily_stats[date]['revenue'] += amount
        daily_stats[date]['txns'] += 1
        daily_stats[date]['customers'].add(cust)
        
    # Format and Sort by Date
    formatted_stats = {}
    
    # Sort keys (dates)
    sorted_dates = sorted(daily_stats.keys())
    
    for date in sorted_dates:
        data = daily_stats[date]
        formatted_stats[date] = {
            'daily_revenue': round(data['revenue'], 2),
            'transaction_count': data['txns'],
            'unique_customers': len(data['customers'])
        }
        
    return formatted_stats

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.
    Returns: Tuple (date, revenue, transaction_count).
    """
    trends = daily_sales_trend(transactions)
    
    if not trends:
        return None
        
    # Find max revenue day
    peak_day = max(trends.items(), key=lambda x: x[1]['daily_revenue'])
    
    # peak_day is ('2024-12-15', {'daily_revenue': ...})
    date = peak_day[0]
    metrics = peak_day[1]
    
    return (date, metrics['daily_revenue'], metrics['transaction_count'])

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with total quantity sold < threshold.
    Returns: List of tuples sorted by quantity ascending.
    """
    # Reuse logic from top_selling but don't slice top N
    all_products = top_selling_products(transactions, n=1000)
    
    # Filter for low quantity
    low_performers = [p for p in all_products if p[1] < threshold]
    
    # Sort ascending (lowest first)
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers


# --- PART 3: API ENRICHMENT & SAVING ---

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.
    Matches 'P101' -> ID 101.
    """
    enriched_data = []
    
    for txn in transactions:
        # Create a copy to avoid modifying original list directly
        new_txn = txn.copy()
        
        # Extract numeric ID from 'P101', 'P109', etc.
        try:
            p_id_str = txn['ProductID']
            # Remove 'P' and convert to int (e.g., 'P101' -> 101)
            numeric_id = int(p_id_str.replace('P', ''))
        except ValueError:
            numeric_id = -1 # Invalid format
            
        # Check if this ID exists in our API data
        if numeric_id in product_mapping:
            api_info = product_mapping[numeric_id]
            
            # Add new fields
            new_txn['API_Match'] = True
            new_txn['API_Category'] = api_info['category']
            new_txn['API_Brand'] = api_info['brand']
            new_txn['API_Rating'] = api_info['rating']
        else:
            # Product not found in API
            new_txn['API_Match'] = False
            new_txn['API_Category'] = 'N/A'
            new_txn['API_Brand'] = 'N/A'
            new_txn['API_Rating'] = 0.0
            
        enriched_data.append(new_txn)
        
    return enriched_data

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves the enriched data to a pipe-delimited file.
    """
    if not enriched_transactions:
        print("No data to save.")
        return

    print(f"Saving enriched data to {filename}...")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 1. Write Header
            header = "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
            f.write(header)
            
            # 2. Write Rows
            for t in enriched_transactions:
                row = f"{t['TransactionID']}|{t['Date']}|{t['ProductID']}|{t['ProductName']}|" \
                      f"{t['Quantity']}|{t['UnitPrice']}|{t['CustomerID']}|{t['Region']}|" \
                      f"{t['API_Category']}|{t['API_Brand']}|{t['API_Rating']}|{t['API_Match']}\n"
                f.write(row)
                
        print("File saved successfully.")
        
    except Exception as e:
        print(f"Error saving file: {e}")