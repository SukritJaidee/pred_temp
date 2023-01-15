import json
import requests
import pandas as pd
save_tmd_filename = "tmd_data"

def tmd_weather(lat, lon, day, hour, duration):
    url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at"
    # querystring = {"lat":lat, "lon":lon, "fields":"tc,rh", "date":"2022-12-03", "hour":hour, "duration":"2"}
    querystring = {"lat":lat, "lon":lon, "fields":"tc,rh", "date":day, "hour":hour, "duration":duration}
    Bearer = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImRhNmJmMGU5ZTBiZGU5ZWI2NjUzMzRjNGIzMjI2MjdkMzhlMDk4ZTIzZmQ5YTZhYTg5N2VmNjRhMjA1MzYzNWU1NTAyMTMxOGM5N2I0OGVhIn0.eyJhdWQiOiIyIiwianRpIjoiZGE2YmYwZTllMGJkZTllYjY2NTMzNGM0YjMyMjYyN2QzOGUwOThlMjNmZDlhNmFhODk3ZWY2NGEyMDUzNjM1ZTU1MDIxMzE4Yzk3YjQ4ZWEiLCJpYXQiOjE2NDk0MDE0MDcsIm5iZiI6MTY0OTQwMTQwNywiZXhwIjoxNjgwOTM3NDA3LCJzdWIiOiIzODkiLCJzY29wZXMiOltdfQ.vjoiRxPJwC3k-6NvDibqOcfN6R1TDvyjdW3B79inIVGIeJnghhKLedSTA-NLctcVJ4mP0eEY4pWfHyT5Ldn5DbdrTRrU-ATHsqHwLPhxwRG9ucx2494Gq1n2WDuKeBH8RsTzGedMOKSMgGtKYCbBZuOUPO8uDKXJzihOyYL08Z1XHvDegFG-nB_Yq24rWrAOHsL-hY0hrwexBjL6dXIXTGz_EgVlLnf57W-YuI08bOY7Gh2nqqwdtr3C1uv-v_SMp0XLuVzPwrEcbPXFxGby15QEoeKLfxlnNPX5tc0FO9Wglyswny5zqU_almZz_upgJB_Kj2Xw5M2O3IK6MFA6znXR1tQxZOCnsrI95ittzucbK5CoWVoIaoxOA-KA8d_gnXI-lCS0E-Fi-JYWrZZMKKyIu8fGNdUvYVgzUvRT3T2argyUa7xmnoDomlgDrPrN20yak7HGyLnrvFw0iD4X78uiphfw2etlWnkQPrTtd22cvTVUzyoVReGCqO4g1abmxEWrS8_glZnT_H9VG6pa1vThak3rwDJPm150UhE5rBHt5x_K8B56TkdAePRToAAwrOfIHNlRvQ4LtfC-5Tn7Go913A8H94fGge5sThZ17ELc-6q7plkPqFe2pjmK-sHEPMkLMu2lhXfz2QHUFAob7Q5qLdVUw-ykTouoz7XVoAM"  
    headers = { 'accept': "application/json", 'authorization': Bearer, }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    # print(data)
    # temd_tmd = data['WeatherForecasts'][0]['forecasts'][0]['data']['tc']
    df = pd.DataFrame(data['WeatherForecasts'][0]['forecasts'])
    df['rh'] = df['data'].apply(lambda x: x['rh'])
    df['tc'] = df['data'].apply(lambda x: x['tc'])
    df['datatime'] = df['time'].apply(lambda x: x[:10]+' '+x[11:19])
    df.drop(['time', 'data'], axis=1, inplace=True)
    df.index = df['datatime'].astype('datetime64[ns]')
    # df.to_csv(save_tmd_filename+'.csv' ,encoding='utf-8-sig', index=False)
    return df