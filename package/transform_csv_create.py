import csv
from .load_raw_data import fetch_nse_gainer_data, fetch_nse_looser_data
from .upload_cloud import upload_to_cloud
from datetime import date
gdata = fetch_nse_gainer_data()
ldata = fetch_nse_looser_data()
def process_data(data):
    logging.info(f"Processing raw data: {data}")
    data = data.split("\n")
    start = data[0].find("'") +1
    end = data[0].find('"')
    data[0] = data[0][:start] + data[0][end:]
    data1 = []
    for i in range(21):
        data1.append(list(eval(data[i])))
    return data1

def create_csv():
    gdata = fetch_nse_gainer_data()
    ldata = fetch_nse_looser_data()

    with open("Data/gdata.csv","w",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(process_data(gdata))
    upload_to_cloud(name="gainer",file_id="1MmNtM4hGlZYzI9yQAnAosHLctkPOHU8I")
    
        
    with open("Data/ldata.csv","w",newline="") as f:
        writer = csv.writer(f)
        writer.writerows(process_data(ldata))
    upload_to_cloud(name="looser",file_id="1MmNtM4hGlZYzI9yQAnAosHLctkPOHU8I")
    