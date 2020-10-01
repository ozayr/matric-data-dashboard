import requests
import json
from api.utils.data import Process


processor = Process('2016_Matric_Schools_Report.csv')
processor.run_processing_pipeline()

for row in processor.raw_data.iterrows():
    response = requests.post('http://localhost:9000/create_record/',data = row[1].to_json(),headers={"Content-Type":"application/json","accept": "application/json"})
print("LOADING DONE")