
res1 = res.drop(['tc', 'rh', 'datatime'], axis=1)
print(res1.shape)
res1.columns = ['lat', 'lon', 'latitude', 'longitude', 'elevation', 'distance', 'temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'year', 'month', 'day', 'hour', 'minute', 'temp.1', 'dwpt.1', 'rhum.1', 'wdir.1', 'wspd.1',
                  'pres', 'lat.1', 'lon.1', 'year.1', 'month.1', 'day.1', 'hour.1', 'minute.1', 'requestedLatitude', 'requestedLongitude', 'latitude.1', 'longitude.1', 'precip1Hour', 'precip6Hour', 'precip24Hour', 'pressureChange',
                  'pressureMeanSeaLevel', 'relativeHumidity', 'temperature', 'temperatureChange24Hour', 'temperatureMax24Hour', 'temperatureMin24Hour', 'temperatureDewPoint', 'temperatureFeelsLike', 'uvIndex',
                  'visibility', 'windDirection', 'windSpeed', 'lat.2', 'lon.2', 'lats', 'lons', 'temp_cs', 'wind_kphs', 'wind_degrees', 'wind_dirs', 'pressure_mbs', 'precip_mms', 'humiditys', 'clouds', 'feelslike_cs',
                  'windchill_cs', 'heatindex_cs', 'dewpoint_cs', 'will_it_rains', 'chance_of_rains', 'vis_kms', 'gust_kphs']
                  

path =  'drive/MyDrive/chula_weather/one_model/models/model_from_tam_LT/'
models = 'Final Blend Model 20112022_950_ibm'
saved_lr = load_model(path+models)
unseen_pred = predict_model(saved_lr, data=res1)
actual = res[['tc', 'datatime']]
res2 = pd.concat([unseen_pred, actual], axis=1,  join="inner")
print(display(res2))