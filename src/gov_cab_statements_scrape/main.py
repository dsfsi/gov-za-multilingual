#!/usr/bin/env python3
import helper_functions
import logging
import sys
import datetime
import os

def main():
    """Main function to execute the cabinet statement scraping process"""
    # Configure logging
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"scraper_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info("Starting cabinet statement scraping process")
    
    try:
        # Read existing data
        data = helper_functions.read_JSON_file()
        logging.info(f"Read {len(data)} existing statements")
        
        # Determine the latest date we have
        if data:
            # Sort data by datetime if available, otherwise by date
            sorted_data = sorted(
                data, 
                key=lambda x: x.get('datetime', x.get('date', '2000-01-01')),
                reverse=True
            )
            
            latest_item = sorted_data[0]
            latest_date = latest_item.get('date', "14 Mar 2013")
            logging.info(f"Latest statement date is: {latest_date}")
        else:
            latest_date = "14 Mar 2013"  # Default start date
            logging.info("No existing data found, starting from default date")
        
        # Get new cabinet statements
        cabinet_statements = helper_functions.get_cabinent_statements_urls(latest_date)
        logging.info(f"Found {len(cabinet_statements)} new cabinet statements to process")
        
        if not cabinet_statements:
            logging.info("No new statements to process, exiting")
            return
        
        # Process each statement in reverse order (oldest first)
        new_data = []
        success_count = 0
        
        for idx, statement in enumerate(reversed(cabinet_statements)):
            logging.info(f"Processing statement {idx+1}/{len(cabinet_statements)}: {statement.get('title', 'Unknown')}")
            logging.info('-' * 50)
            
            # Extract translations
            extracted = helper_functions.extract_translations(statement['url'])
            
            if extracted:
                new_data.append(extracted)
                success_count += 1
                logging.info(f"Successfully processed statement {idx+1}/{len(cabinet_statements)}")
            else:
                logging.warning(f"Failed to extract translations for statement {idx+1}/{len(cabinet_statements)}")
        
        logging.info(f"Successfully processed {success_count}/{len(cabinet_statements)} statements")
        
        if new_data:
            # Update CSV files (optional)
            try:
                helper_functions.update_all_csv(new_data)
                logging.info("Successfully updated CSV files")
            except Exception as e:
                logging.error(f"Error updating CSV files: {str(e)}")
            
            # Update JSON file
            combined_data = data + new_data
            if helper_functions.write_JSON_file(combined_data):
                logging.info(f"Successfully updated JSON file with {len(combined_data)} total statements")
            else:
                logging.error("Failed to update JSON file")
        else:
            logging.info("No new data to add")
        
    except Exception as e:
        logging.error(f"Unexpected error in main process: {str(e)}", exc_info=True)
        sys.exit(1)
    
    logging.info("Cabinet statement scraping process complete")

if __name__ == "__main__":
    main()