from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

app = Flask(__name__)
API_KEY = os.getenv('OPENWEATHER_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city = ''
    unit = 'metric'
    unit_symbol = '°C'

    if request.method == 'POST':
        city = request.form.get('city', '')
        unit = request.form.get('unit', 'metric')
        unit_symbol = '°C' if unit == 'metric' else '°F'

        if city:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'unit': unit_symbol
                }
            else:
                weather_data = {'error': 'City not found'}

    return render_template('index.html', weather=weather_data, city=city, unit=unit)


if __name__ == '__main__':
    app.run(debug=True)
