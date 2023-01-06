import json
import requests
import pandas as pd
from datetime import datetime, timedelta, date, tzinfo

save_x3_filename = "x3_data"
apikey = "2601b3bc3f684d2681b3bc3f687d26f8"

def IMB_weather(lat, lon, start, end, apikey):
  df_temp = pd.DataFrame([])
  df_temp['lat'], df_temp['lon'] = pd.Series(lat), pd.Series(lon)
  url1 = "https://api.weather.com/v3/wx/hod/r1/direct?geocode="
  url2 = str(lat)+","+str(lon)+"&startDateTime="+start+"T00Z&endDateTime="+end+"T00Z"
  # url2 = str(lat)+","+str(lon)+"&startDateTime="+start+"T12Z&endDateTime="+end+"T12Z"
  # url2 = str(lat)+","+str(lon)+"&startDateTime="+start+"T06Z&endDateTime="+end+"T06Z"
  url3 = "&format=json&units=m&apiKey="+apikey
  url = url1+url2+url3
  payload, headers={},{}
  response = requests.request("GET", url, headers=headers, data=payload)
  # print(response)
  data = json.loads(response.text)
  df = pd.DataFrame(data)
  df['datetime_ns'] = pd.to_datetime(df['validTimeUtc'])
  df['datetime_ns_thai'] = df['datetime_ns'].map(lambda x: x.tz_convert('Asia/Bangkok'))
  df['datetime_thai'] = df['datetime_ns_thai'].map(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
  df['datetime_utc'] = df['datetime_ns'].map(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
  df.drop(['validTimeUtc', 'datetime_ns', 'datetime_ns_thai'], axis=1, inplace=True)
  df['lat'] = df['requestedLatitude'].map(lambda x: df_temp['lat'][0])
  df['lon'] = df['requestedLongitude'].map(lambda x: df_temp['lon'][0])
  return df

def x3_api(q1, start, end, apikey):
    x3 = IMB_weather(q1[0], q1[1], start, end, apikey)
    x3.drop(['gridpointId', 'drivingDifficultyIndex', 'iconCode', 'iconCodeExtended',
                'snow1Hour', 'snow6Hour', 'snow24Hour','snow2Day', 'snow3Day', 'snow7Day', 'snowMtd',
                'snowSeason', 'snowYtd','windGust', 'precip2Day', 'precip3Day', 'precip7Day', 'precipMtd',
                'precipYtd'], axis=1, inplace=True)

    change_list = ['requestedLatitude', 'requestedLongitude', 'latitude', 'longitude', 'precip1Hour',
                  'precip6Hour', 'precip24Hour', 'pressureChange', 'pressureMeanSeaLevel', 'relativeHumidity',
                  'temperature', 'temperatureChange24Hour', 'temperatureMax24Hour', 'temperatureMin24Hour',
                  'temperatureDewPoint', 'temperatureFeelsLike', 'uvIndex', 'visibility', 'windDirection', 'windSpeed',
                  'windSpeed', 'lat', 'lon']

    for col_name in change_list: x3[col_name] =x3[col_name].astype('float32')
    x3['datetime_thai2'] = x3['datetime_thai'].apply(lambda x: pd.to_datetime(x[:14]+"00:00"))
    x3.index = x3['datetime_thai2']
    x3.drop(['datetime_thai', 'datetime_utc', 'datetime_thai2'], axis=1, inplace=True)
    x3.rename(columns={'temperature':'temp_x3'}, inplace=True)
    # x3.to_csv(save_x3_filename+'.csv' ,encoding='utf-8-sig')
    # print(x3.shape); display(x3.head(1)); display(x3.tail(1));
    x3.index = x3.index+timedelta(hours=2)
    print('x3', end = ' '); print(x3.index[0], end = ' '); print(x3.index[-1]);
    return x3