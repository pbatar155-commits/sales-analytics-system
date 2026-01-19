import os

def read_sales_data(filename):
    """
    Reads the sales data file handling potential encoding issues.
    Tries multiple encodings (utf-8, latin-1, cp1252) to ensure file is read correctly.
    
    Args:
        filename (str): Path to the file.
        
    Returns:
        list: List of raw string lines from the file (excluding header).
    """
    # List of encodings to try as per requirements
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return []

    for encoding in encodings_to_try:
        try:
            print(f"Attempting to read file with encoding: {encoding}")
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                
                # Check if file is empty
                if not lines:
                    return []
                
                # Skip header and remove empty lines immediately
                # lines[1:] skips the first row (Header)
                cleaned_lines = [line.strip() for line in lines[1:] if line.strip()]
                
                print(f"Successfully read {len(cleaned_lines)} lines using {encoding}.")
                return cleaned_lines
                
        except UnicodeDecodeError:
            # If this encoding fails, the loop continues to the next one
            continue
        except Exception as e:
            print(f"Unexpected error with encoding {encoding}: {e}")
            return []

    print("Error: Failed to read file with all attempted encodings.")
    return []