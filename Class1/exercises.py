import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('weatherData.csv')

# Data format
'''
#   Column                                 Non-Null Count  Dtype  
---  ------                                 --------------  -----  
 0   lastUpdated                            3487 non-null   object 
 1   weatherStation.name                    3487 non-null   object 
 2   weatherStation.province                3487 non-null   object 
 3   weatherStation.location.coordinates.0  3487 non-null   float64
 4   weatherStation.location.coordinates.1  3487 non-null   float64
 5   avgAirTemperature                      3458 non-null   float64
 6   precipitation                          3480 non-null   float64
 7   minAirTemperature                      3468 non-null   float64
 8   maxAirTemperature                      3458 non-null   float64
'''

# Data cleaning
data.rename(columns={'weatherStation.name': 'station'}, inplace=True)
data.rename(columns={'weatherStation.province': 'province'}, inplace=True)
data.rename(columns={'weatherStation.location.coordinates.0': 'latitude'}, inplace=True)
data.rename(columns={'weatherStation.location.coordinates.1': 'longitude'}, inplace=True)

# Fill the data with the mean of the column when NaN
meanAirTmp = data["avgAirTemperature"].mean()
meanPrecipitation = data["precipitation"].mean()
meanMinAirTemperature = data["minAirTemperature"].mean()
meanMaxAirTemperature = data["maxAirTemperature"].mean()

data["avgAirTemperature"] = data["avgAirTemperature"].fillna(meanAirTmp)
data["precipitation"] = data["precipitation"].fillna(meanPrecipitation)
data["minAirTemperature"] = data["minAirTemperature"].fillna(meanMinAirTemperature)
data["maxAirTemperature"] = data["maxAirTemperature"].fillna(meanMaxAirTemperature)

# Set the date as datetime
data['lastUpdated'] = pd.to_datetime(data['lastUpdated'], errors="coerce")

# Set all string data to uppercase
data['station'] = data['station'].str.upper()
data['province'] = data['province'].str.upper()

# New Data Format
'''
 #   Column             Non-Null Count  Dtype  
---  ------             --------------  -----  
 0   lastUpdated        3487 non-null   object 
 1   station            3487 non-null   object 
 2   province           3487 non-null   object 
 3   latitude           3487 non-null   float64
 4   longitude          3487 non-null   float64
 5   avgAirTemperature  3458 non-null   float64
 6   precipitation      3480 non-null   float64
 7   minAirTemperature  3468 non-null   float64
 8   maxAirTemperature  3458 non-null   float64
'''
print('------------------------------------------------------------------------------------------------------')
print('Exercise 1')
# 1 Calcular la temperatura media del aire para cada estación meteorológica.

# for station in data['station'].unique():
#     print(f"Average air temperature for {station}: {data[data['station'] == station]['avgAirTemperature'].mean()}")

# Fastest way
print(data.groupby('station')['avgAirTemperature'].mean())


print('------------------------------------------------------------------------------------------------------')
print('Exercise 2')
# 2 Encontrar la temperatura máxima registrada en todo el dataset y la fecha en la que ocurrió.
# Print the id of the row with the maximum temperature
# rowmax = data['maxAirTemperature'].idxmax()
# #print(rowmax)
# # Print the date and the temperature
# maxAirTemperature = data.loc[rowmax, 'maxAirTemperature']
# date = data.loc[rowmax, 'lastUpdated']
# print(f"The maximum temperature registered was {maxAirTemperature} on {date}")

# Fastest way
print(data.loc[data['maxAirTemperature'].idxmax(), ['lastUpdated', 'maxAirTemperature']])

print('------------------------------------------------------------------------------------------------------')
print('Exercise 3')
# 3 Filtrar el dataset para mostrar solo los registros de una provincia específica.
filtered_data_by_province = data[data['province'] == 'BARCELONA']
print(filtered_data_by_province.info())

print('------------------------------------------------------------------------------------------------------')
print('Exercise 4')
# 4 Calcular la cantidad total de precipitación registrada en cada provincia
print(data.groupby('province')['precipitation'].sum())

print('------------------------------------------------------------------------------------------------------')
print('Exercise 5')
# 5 Calcular el promedio de temperatura del aire por mes en todo el dataset.
data_per_month = data.groupby(data['lastUpdated'].dt.month)['avgAirTemperature'].mean()
print(data_per_month)

print('------------------------------------------------------------------------------------------------------')
print('Exercise 6')
# 6 Filtrar el dataset para mostrar solo los registros de una estación meteorológica específica.
filtered_data_by_station = data[data['station'] == 'BARCELONA AEROPUERTO']
print(filtered_data_by_station.info())

print('------------------------------------------------------------------------------------------------------')
print('Exercise 7')
# 7 Encontrar el día con la precipitación más alta registrada en todo el dataset y la estación meteorológica donde ocurrió.
print(data.loc[data['precipitation'].idxmax(), [ 'station', 'precipitation']])

print('------------------------------------------------------------------------------------------------------')
print('Exercise 8')
# 8 Crear una visualización gráfica que muestre la relación entre la temperatura del aire y 
# la precipitación para un rango de fechas específico
starting_date = '2023-12-01'
ending_date = '2023-12-31'
filtered_data_by_date = data[(data['lastUpdated'] >= starting_date) & (data['lastUpdated'] <= ending_date)]
print(filtered_data_by_date.info())
plt.scatter(filtered_data_by_date['avgAirTemperature'], filtered_data_by_date['precipitation'])
plt.xlabel('Average Air Temperature')
plt.ylabel('Precipitation')
plt.title(f'Average Air Temperature vs Precipitation from {starting_date} to {ending_date}')
plt.show()

print('------------------------------------------------------------------------------------------------------')
print('Exercise 9')
# 9 Encontrar las coordenadas (latitud y longitud) de la estación meteorológica más cercana a un punto de interés dado.
