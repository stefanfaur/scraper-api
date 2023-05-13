from fastapi import FastAPI
import requests
import json
import concurrent.futures

app = FastAPI()

def fetch_carrier_data(session, url, headers, carrier_id):
    data = {
        "Guid": "15a9e559-3103-4bcf-8555-4c3502d3bcec",
        "CarrierIds": [carrier_id]
    }
    
    response = session.post(url, headers=headers, json=data)
    
    modified_payloads = []
    
    if response.status_code == 200:
        response_json = response.json()
        
        if "Payload" in response_json and response_json["Payload"]:
            for item in response_json["Payload"]:
                keys_to_keep = ["CarrierId", "Latitude", "Longitude"]
                modified_item = {key: item[key] for key in keys_to_keep if key in item}
                modified_payloads.append(modified_item)
                
    else:
        print(f"Request for CarrierId {carrier_id} failed with status code {response.status_code}")
    
    return carrier_id, modified_payloads

@app.get("/fetch_carrier_data")
async def fetch_data():
    url = 'https://fleet.trackgps.ro/api/PublicMap/get-vehicles-address'
    headers = {'Content-Type': 'application/json'}
    responses = {}

    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_carrier_data, session, url, headers, carrier_id) for carrier_id in range(14132, 14230)]
            for future in concurrent.futures.as_completed(futures):
                carrier_id, modified_payloads = future.result()
                responses[carrier_id] = modified_payloads

    return responses
