from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display_data():
    if request.method == 'POST':
        city_name = request.form.get('city_name')
        coordinates = get_coordinates(city_name)

        if coordinates is not None:
            api_key = '00886ee668fbe9baee451986175b3c5b'
            url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={coordinates[0]}&lon={coordinates[1]}&appid={api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                json_data = response.json()
                lon = json_data['coord']['lon']
                lat = json_data['coord']['lat']
                aqi = json_data['list'][0]['main']['aqi']
                if aqi == 1:
                    aqi_pos = "Good"
                if aqi == 2:
                    aqi_pos = "Fair"
                if aqi == 3:
                    aqi_pos = "Moderate"
                if aqi == 4:
                    aqi_pos = "Poor"
                if aqi == 5:
                    aqi_pos = "Very Poor"
                co = json_data['list'][0]['components']['co']
                return render_template('index.html', lon=lon, lat=lat, aqi=aqi, co=co, city_name=city_name, aqi_pos=aqi_pos)
            else:
                return f'Error: Unable to fetch air quality data. Status code {response.status_code}'

    return render_template('index.html', lon=None, lat=None, aqi=None, co=None, city_name=None)

def get_coordinates(city_name):
    api_key = 'aec9c35636834e57a0547909ef254cd9' 
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
