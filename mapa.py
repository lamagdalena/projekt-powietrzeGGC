import json
import requests

def get_measuring_stations():
    URL = 'http://api.gios.gov.pl/pjp-api/rest/station/findAll'
    a = requests.get(URL)
    dane = json.loads(a.text)
    return dane
    
def get_sensors(station_id):
    URL = 'http://api.gios.gov.pl/pjp-api/rest/station/sensors/{}'.format(station_id)
    s = requests.get(URL)
    def json_validator(s):
        try:
            json.loads(s.text)
            return True
        except ValueError as error:
            return False
    if json_validator(s) is True:
        tresc = json.loads(s.text)
        return tresc
        
def stan_zanieczyszczen_dla_stacji(station_id):
    stanowiska = get_sensors(station_id)
    dane = []
    if type(stanowiska) == list:
        for ident in stanowiska:
            URL = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/{}'.format(ident['id'])
            b = requests.get(URL)
            wynik = json.loads(b.text)
            dane.append(wynik)
        return dane

def poziom_zagrozenia_dla_stacji(station_id):
    wyniki = stan_zanieczyszczen_dla_stacji(station_id)
    if type(wyniki) == list:
        for slow in wyniki:
            if slow['key'] == 'PM10':
                if type(slow['values'][0]['value']) == float:
                    if slow['values'][0]['value'] <= 50.00:
                        return 'Poziom dopuszalny'
                    elif slow['values'][0]['value'] <= 200.00:
                        return 'Poziom informowania'
                    elif slow['values'][0]['value'] >= 300.00:
                        return 'Poziom alarmowy'
                else:
                    return 'Brak aktualnych danych dla PM10.'
    else:
        return 'Brak danych'
   
   
import folium

def mapa_zanieczyszczen():
    m = folium.Map(location = [52.22977, 21.01178], zoom_start = 6)

    inf = get_measuring_stations()
    
    for slownik in inf:
        folium.Marker([float(slownik['gegrLat']), float(slownik['gegrLon'])], popup = (slownik['stationName'] + ' ' + poziom_zagrożenia_dla_stacji({}).format(slownik['id'])) ).add_to(m)

    return m
