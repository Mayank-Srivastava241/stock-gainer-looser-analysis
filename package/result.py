import csv
import logging
from datetime import date
import pandas as pd
import numpy as np
from .upload_cloud import upload_to_cloud
logging.basicConfig(filename=f"loggs/{date.today().strftime("%d-%m-%Y")}_log.log",filemode='a',level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s')

def file_copy():
    DATA = []
    with open("Data/gdata.csv","r") as f:
        reader = csv.reader(f)
        for read in reader:
            DATA.append(read)
    with open("Data/gdata_prev.csv","w",newline='') as f:
        writer = csv.writer(f)
        writer.writerows(DATA)    
    DATA = []
    with open("Data/ldata.csv","r") as f:
        reader = csv.reader(f)
        for read in reader:
            DATA.append(read)
    with open("Data/ldata_prev.csv","w",newline='') as f:
        writer = csv.writer(f)
        writer.writerows(DATA)
    logging.info("Previous File Updated Successfully.")

def comparison():
    gdata_df = pd.DataFrame(pd.read_csv("Data/gdata.csv"))
    gdata_prev_df = pd.DataFrame(pd.read_csv("Data/gdata_prev.csv"))
    ldata_df = pd.DataFrame(pd.read_csv("Data/ldata.csv"))
    ldata_prev_df = pd.DataFrame(pd.read_csv("Data/ldata_prev.csv"))

    gdf = gdata_df['Symbol']
    ldf = ldata_df['Symbol']
    gprevdf = gdata_prev_df['Symbol']
    lprevdf = ldata_prev_df['Symbol']

    common_gg = set(gdf).intersection(set(gprevdf))
    common_ll = set(ldf).intersection(set(lprevdf))
    common_gl = set(gdf).intersection(set(lprevdf))
    common_lg = set(ldf).intersection(set(gprevdf))

    cols = {
    "Common Gainers": list(common_gg),
    "Common Losers": list(common_ll),
    "Gainers converted to Losers": list(common_gl),
    "Losers converted to Gainers": list(common_lg)
    }

    max_len = max(len(v) for v in cols.values())

    for k in cols:
        cols[k].extend([np.nan] * (max_len - len(cols[k])))

    new_df = pd.DataFrame(cols).fillna('')

    new_df.to_csv("Data/comparison_result.csv", index=False)
    logging.info(f"Comparison Result CSV created successfully.\nData:{new_df}")
    upload_to_cloud(name="result",file_id="11QyZQtJetb2XXE4zk9orde-3dAw0qJea")
    logging.info("Comparison Result File uploaded successfully.")
    print("Comparison Result File uploaded successfully.")
    file_copy()


