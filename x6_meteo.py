import json
import requests
import pandas as pd

#@title Open meteo api
def open_meteo_v1(latitude, longitude, start_date, end_date):
  vars1 = "hourly=temperature_2m,relativehumidity_2m"
  vars2 = "hourly=temperature_2m,relativehumidity_2m,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,terrestrial_radiation_instant"
  vars3 = "hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,rain,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,windspeed_10m,windspeed_100m,winddirection_10m,winddirection_100m,windgusts_10m,soil_temperature_0_to_7cm,soil_temperature_7_to_28cm"
  vars4 = "hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,rain,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,windspeed_10m,winddirection_10m,windgusts_10m"

  timezone = "Asia/Bangkok"
  url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&{vars4}"
  # url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&timezone={timezone}&{vars1}"
  # url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&timezone={timezone}&{vars}&models=best_match"
  # url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&timezone={timezone}&{vars3}&models=best_match"

  payload, headers={}, {}
  response = requests.request("GET", url, headers=headers, data=payload)
  print('response', response)
  data = json.loads(response.text)
  print('data', data)
  lat, lon = data['latitude'], data['longitude']
  elevation = data['elevation']
  time_list = data['hourly']['time']
  temp_2m_list = data['hourly']['temperature_2m']
  rh_2m_list= data['hourly']['relativehumidity_2m']
  
  dewp_2m= data['hourly']['dewpoint_2m']
  apparent_temp= data['hourly']['apparent_temperature']
  rain= data['hourly']['rain']
  cloudcover= data['hourly']['cloudcover']
  cloudcover_low= data['hourly']['cloudcover_low']
  cloudcover_mid= data['hourly']['cloudcover_mid']
  cloudcover_high= data['hourly']['cloudcover_high']
  shortwave_rad= data['hourly']['shortwave_radiation']
  direct_rad= data['hourly']['direct_radiation']
  diffuse_rad= data['hourly']['diffuse_radiation']
  direct_normal_irr= data['hourly']['direct_normal_irradiance']
  wspeed_10m= data['hourly']['windspeed_10m']
#   wspeed_100m= data['hourly']['windspeed_100m']
  wdirection_10m= data['hourly']['winddirection_10m']
#   wdirection_100m= data['hourly']['winddirection_100m']
  wgusts_10m= data['hourly']['windgusts_10m']
#   soil_temp_0_to_7cm= data['hourly']['soil_temperature_0_to_7cm']
#   soil_temp_7_to_28cm= data['hourly']['soil_temperature_7_to_28cm']

  info_df = pd.DataFrame({'lat':[lat], 'lon':[lon], 'elevation':[elevation], })
  df = pd.DataFrame({'time':time_list, 'temp_2m':temp_2m_list, 'rh_2m':rh_2m_list,
                     'dewpoint_2m':dewp_2m, 'apparent_temp':apparent_temp, 'rain':rain,
                     'cloudcover':cloudcover, 
                     'cloudcover_low':cloudcover_low, 'cloudcover_mid':cloudcover_mid,'cloudcover_high':cloudcover_high,
                     'shortwave_rad':shortwave_rad, 'direct_rad':direct_rad, 'diffuse_rad':diffuse_rad, 'direct_normal_irr':direct_normal_irr,
                     'wspeed_10m':wspeed_10m,
#                      'wspeed_100m':wspeed_100m,
                     'wdirection_10m':wdirection_10m,
#                      'wdirection_100m':wdirection_100m,
                     'wgusts_10m':wgusts_10m,
#                      'soil_temp_0_to_7cm':soil_temp_0_to_7cm, 'soil_temp_7_to_28cm':soil_temp_7_to_28cm,
                     })
  df['lat'], df['lon'], df['elevation']  = latitude, longitude, elevation
  df['lat_res'], df['lon_res']  = lat, lon
  df['datetime1'] = df['time'].apply(lambda x: pd.to_datetime(x[:10]+" "+x[11:]))
  df['indexs'] =  df['datetime1'].astype(str)+df['lat'].astype(str)+df['lon'].astype(str)
  df.index = df['indexs']
  return df

# timezone = "Asia/Bangkok"
# latitude, longitude = "13.7364157", "100.524722"
# start_date, end_date = "2021-12-01", "2022-01-03"
# df1 = open_meteo_v1(latitude, longitude, start_date, end_date, timezone)
# print(display(df1.head(2)))
