from package.transform_csv_create import create_csv
from package.result import comparison
import logging
from datetime import date
logging.basicConfig(filename=f"loggs/{date.today().strftime('%d-%m-%Y')}_log.log",filemode='a',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
if __name__ == "__main__":
    create_csv()
    logging.info("Upload Process Completed.")
    comparison()
    logging.info("Result Generation Process Completed.")
    
