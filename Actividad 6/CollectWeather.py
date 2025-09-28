import requests #Librería para hacer peticiones HTTP 
import pandas as pd  #Manejo de los dataframes
import numpy as np  #Manejar valores númericos y NaN
from keys import * #Importa la API key guardada del archivo de keys.py

city = "Florence" #Nombre de la ciudad
country = "IT" #Código del país

#Llamada a la API de OpenWeather
response = requests.get(
    f'https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={OWM_key}&units=metric&lang=en'
)

#Verfica que la respuesta sea exitosa (200 = OK)
if response.status_code != 200:
    print("Error en la API:", response.status_code, response.text) #Muestra el error si falla
else:
    data = response.json() #Convierte la respuesta JSON en un diccionario de Python

    forecast_list = data.get('list', []) #Obtiene la lista de predicciones, o una lista vacía si no existe

#Lista para guardar los datos que se van a extraer
    times, temperatures, humidities = [], [], []
    weather_statuses, wind_speeds = [], []
    rain_volumes, snow_volumes = [], []

#Registro del pronóstico 
    for entry in forecast_list:
        times.append(entry.get('dt_txt', np.nan)) #Fecha y hora
        temperatures.append(entry.get('main', {}).get('temp', np.nan))  #Temperatura en °C
        humidities.append(entry.get('main', {}).get('humidity', np.nan))  #Humedad en %
        weather_statuses.append(entry.get('weather', [{}])[0].get('main', np.nan))  #Estado del clima (Clear, Clouds, Rain...)
        wind_speeds.append(entry.get('wind', {}).get('speed', np.nan))  #Velocidad del viento
        rain_volumes.append(entry.get('rain', {}).get('3h', np.nan))   #Lluvia acumulada en 3 horas
        snow_volumes.append(entry.get('snow', {}).get('3h', np.nan))   #Nieve acumulada en 3 horas

#Dataframe de los datos recolectados
    df = pd.DataFrame({
        'time': times,
        'temperature': temperatures,
        'humidity': humidities,
        'weather_status': weather_statuses,
        'wind_speed': wind_speeds,
        'rain_volume_3h': rain_volumes,
        'snow_volume_3h': snow_volumes
    })

    print(df.head())   #Muestra las primeras 5 filas del Dataframe
