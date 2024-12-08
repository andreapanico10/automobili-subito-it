import requests
import json 
import numpy as np
import pandas as pd

url = "https://hades.subito.it/v1/search/items"

querystring = {"q":"alfa giulia","c":"2","t":"s","qso":"false","shp":"false","urg":"false","sort":"datedesc","lim":"100","start":"0"}

payload = ""
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://www.subito.it",
    "priority": "u=1, i",
    "referer": "https://www.subito.it/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "x-subito-channel": "web",
    "x-subito-environment-id": "c79e6360-ea6b-431f-9b65-3be9d52c7b84"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
try:
    json_response = response.json()  # Parse response text as JSON
    # Print the keys of the JSON response
    ads = json_response['ads']
    data_rows = []

    for ad in ads:
        """
        print(ad['subject'])
        print(ad['body'])
        features = ad['features']

        for feat in features:
            if feat['uri'] == '/doors':
                print('Porte: ',feat['values'][0]['value'])
            
            if feat['uri'] == '/fuel':
                print('Carburante: ',feat['values'][0]['value'])
            
            if feat['uri'] == '/vehicle_status':
                print('Tipo di veicolo: ',feat['values'][0]['value'])

            if feat['uri'] == '/vat_deductible':
                print('Iva deducibile: ',feat['values'][0]['value'])

            if feat['uri'] == '/gearbox':
                print('Cambio: ',feat['values'][0]['value'])
            
            if feat['uri'] == '/price':
                print('Prezzo: ',feat['values'][0]['value'])

            if feat['uri'] == '/car':
                for value in feat['values']:
                    print(f'{value["label"]}: ',value['value'])

            if feat['uri'] == '/car_type': 
                print('Tipo di macchina: ',feat['values'][0]['value'])
            
            if feat['uri'] == '/seats': 
                print('Posti: ',feat['values'][0]['value'])
            
            if feat['uri'] == '/mileage': 
                print('Km range: ',feat['values'][0]['value'])

            if feat['uri'] == '/mileage_scalar': 
                print('km precisi: ',feat['values'][0]['value'])

            if feat['uri'] == '/year': 
                print('Anno di immatricolazione: ',feat['values'][0]['value'])

            if feat['uri'] == '/register_date': 
                print('Data di immatricolazione: ',feat['values'][0]['value'])

        print('Advertiser: ', ad['advertiser']['name'])
        print('Company: ', ad['advertiser']['company'])
        print('Città: ', ad['geo']['city']['value'])
        print('Provincia: ', ad['geo']['city']['short_name'])

        """
        # Initialize a row with the necessary fields
        row = [
            ad.get('subject', ''),
            ad.get('body', ''),
            ad['advertiser'].get('name', ''),
            ad['advertiser'].get('company', ''),
            ad['geo']['city'].get('value', ''),
            ad['geo']['city'].get('short_name', ''),
        ]
        
        features = ad.get('features', [])
        
        # Extract specific features
        feature_values = {
            'Doors': None,
            'Fuel': None,
            'Vehicle_status': None,
            'Vat_deductible': None,
            'Gearbox': None,
            'Price': None,
            'Car_type': None,
            'Seats': None,
            'Mileage': None,
            'Mileage_scalar': None,
            'Year': None,
            'Register_date': None,
        }
        
        for feat in features:
            if feat['uri'] in ['/doors', '/fuel', '/vehicle_status', '/vat_deductible', '/gearbox', 
                            '/price', '/car_type', '/seats', '/mileage', '/mileage_scalar', 
                            '/year', '/register_date']:
                label = feat['uri'].replace('/', '').capitalize()
                feature_values[label] = feat['values'][0]['value']
            
            if feat['uri'] == '/car':
                for value in feat['values']:
                    feature_values[value["label"]] = value['value']
        
        # Extend the row with feature values
        row.extend(feature_values.values())
        if len(row) < 21:
            row.append(None)

        # Append the row to the list
        data_rows.append(row)
    # Convert list of rows to NumPy array
    np_array = np.array(data_rows, dtype=object)
    #print(np_array)

    columns = [
    'Subject', 'Body', 'Advertiser Name', 'Company', 
    'City', 'Province', 
    'Porte', 'Carburante', 'Tipo di veicolo', 'Iva deducibile', 
    'Cambio', 'Prezzo', 'Tipo di macchina', 'Posti', 
    'Km range', 'Km precisi', 'Anno di immatricolazione', 
    'Data di immatricolazione', '1', '2', '3'
    ]
    df = pd.DataFrame(np_array, columns=columns)
    print(df)
    
except json.JSONDecodeError:
    print("Failed to parse JSON response")