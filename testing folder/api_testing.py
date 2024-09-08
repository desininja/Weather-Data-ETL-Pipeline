import requests
import json
import pandas as pd

def get_weather_data():
    
 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
 

    url = 'api.openweathermap.org/data/2.5/forecast?'
    url1 = "https://api.openweathermap.org/data/2.5/forecast"
    api_params = {
        "q": "Toronto,Canada",
        "appid": Variable.get("api_key")
    }
    response = requests.get(url1, params=api_params)
    data = response.json()
    print(data)
    with open('weather_data.json','w') as f:
        json.dump(data,f)
    
    data_list = data['list']
    df = pd.json_normalize(data_list)
    print(df.head())
    df.to_csv('weather_data.csv', index=False)

if __name__ == '__main__':
    get_weather_data()