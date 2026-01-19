# Sales Analytics System

## Overview
This is a Python-based data analytics system designed to process sales records, enrich them with real-time product data from an external API, and generate comprehensive business reports.

## Features
- **Data Cleaning**: Parses pipe-delimited files, removes invalid records, and handles data anomalies.
- **Analysis**: Calculates Total Revenue, Region-wise performance, and identifies top-selling products.
- **API Integration**: Fetches product categories and brands from DummyJSON API to enrich local sales data.
- **Reporting**: Generates a detailed text-based sales report (`output/sales_report.txt`).

## Project Structure
sales-analytics-system/ │ ├── data/ │ ├── sales_data.txt # Raw input data │ └── enriched_sales_data.txt # Output data with API details │ ├── output/ │ └── sales_report.txt # Final business report │ ├── utils/ │ ├── file_handler.py # Handles file reading/encoding │ ├── data_processor.py # core logic for parsing & analysis │ ├── api_handler.py # Fetches data from DummyJSON API │ └── report_generator.py # Creates formatted text reports │ ├── main.py # Main entry point of the application └── README.md # Project documentation

## Requirements
- Python 3.x
- `requests` library

## Installation & Usage
1. Install dependencies:
   ```bash
   pip install requests