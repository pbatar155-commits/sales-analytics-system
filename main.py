import os
import sys

# Import all modules
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter_data,
    calculate_total_revenue,
    find_peak_sales_day
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from utils.report_generator import generate_sales_report

def main():
    print("========================================")
    print("      SALES DATA ANALYTICS SYSTEM       ")
    print("========================================")

    try:
        # --- STEP 1: READ DATA ---
        print("\n[1/10] Reading sales data...")
        file_path = os.path.join('data', 'sales_data.txt')
        
        if not os.path.exists(file_path):
            print(f"Error: Data file not found at {file_path}")
            return

        raw_lines = read_sales_data(file_path)
        if not raw_lines:
            print("Error: File is empty or could not be read.")
            return
        print(f"   ✓ Successfully read {len(raw_lines)} raw lines")

        # --- STEP 2: PARSE DATA ---
        print("\n[2/10] Parsing and cleaning transactions...")
        all_transactions = parse_transactions(raw_lines)
        print(f"   ✓ Parsed {len(all_transactions)} records")

        # --- STEP 3 & 4: USER INTERACTION (FILTERS) ---
        print("\n[3/10] Preparing Filter Options...")
        
        # Calculate available options for display
        regions = sorted(list(set(t['Region'] for t in all_transactions if t['Region'])))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in all_transactions]
        min_amt, max_amt = (min(amounts), max(amounts)) if amounts else (0, 0)
        
        print(f"   Available Regions: {', '.join(regions)}")
        print(f"   Amount Range: ${min_amt:,.2f} - ${max_amt:,.2f}")

        # User Input
        user_choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        
        selected_region = None
        min_val = None
        max_val = None

        if user_choice == 'y':
            print("   --- Enter Filter Criteria (Press Enter to skip) ---")
            
            # Region Input
            reg_input = input(f"   Region ({', '.join(regions)}): ").strip()
            if reg_input:
                selected_region = reg_input
            
            # Min Amount Input
            min_input = input("   Min Transaction Amount: ").strip()
            if min_input:
                try:
                    min_val = float(min_input)
                except ValueError:
                    print("   ! Invalid number, ignoring min amount.")

            # Max Amount Input
            max_input = input("   Max Transaction Amount: ").strip()
            if max_input:
                try:
                    max_val = float(max_input)
                except ValueError:
                    print("   ! Invalid number, ignoring max amount.")

        # --- STEP 5: VALIDATE & FILTER ---
        print("\n[4/10] Validating and Filtering transactions...")
        valid_data, invalid_count, summary = validate_and_filter_data(
            all_transactions, 
            region=selected_region, 
            min_amount=min_val, 
            max_amount=max_val
        )
        print(f"   ✓ Valid: {len(valid_data)} | Invalid/Filtered Removed: {invalid_count + summary['filtered_by_region'] + summary['filtered_by_amount']}")

        if not valid_data:
            print("\nError: No valid data left after filtering! Exiting.")
            return

        # --- STEP 6: ANALYSIS ---
        print("\n[5/10] Analyzing sales data...")
        # (Calling functions just to show progress, actual report uses report_generator)
        total_rev = calculate_total_revenue(valid_data)
        peak_day = find_peak_sales_day(valid_data)
        print("   ✓ Analysis complete (Revenue, Peak Days, Top Products calculated)")

        # --- STEP 7: API FETCH ---
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        if api_products:
            print(f"   ✓ Fetched {len(api_products)} products")
        else:
            print("   ! Warning: API fetch failed. Proceeding without enrichment.")

        # --- STEP 8: ENRICHMENT ---
        print("\n[7/10] Enriching sales data...")
        enriched_data = []
        if api_products:
            product_map = create_product_mapping(api_products)
            enriched_data = enrich_sales_data(valid_data, product_map)
            
            # Calculate success rate
            matches = sum(1 for t in enriched_data if t.get('API_Match'))
            print(f"   ✓ Enriched {matches}/{len(valid_data)} transactions")
        else:
            enriched_data = valid_data # Fallback
            print("   ! Skipping enrichment due to API error")

        # --- STEP 9: SAVE ENRICHED FILE ---
        print("\n[8/10] Saving enriched data...")
        enriched_file_path = os.path.join('data', 'enriched_sales_data.txt')
        save_enriched_data(enriched_data, enriched_file_path)
        print(f"   ✓ Saved to: {enriched_file_path}")

        # --- STEP 10: GENERATE REPORT ---
        print("\n[9/10] Generating comprehensive report...")
        report_path = os.path.join('output', 'sales_report.txt')
        generate_sales_report(valid_data, enriched_data, report_path)
        print(f"   ✓ Report saved to: {report_path}")

        print("\n[10/10] Process Complete!")
        print("========================================")
        print(f"SUCCESS: System executed successfully.")
        print(f"Outputs available in 'data/' and 'output/' folders.")
        print("========================================")

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nCRITICAL ERROR: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()