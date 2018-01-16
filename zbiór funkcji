import json
import requests

def get_measuring_stations():
    URL = 'http://api.gios.gov.pl/pjp-api/rest/station/findAll'
    a = requests.get(URL)
    dane = json.loads(a.text)
    return dane

def get_measuring_stations_for_city(city):
    data = get_measuring_stations()
    stacje_w_miescie = []
    for slownik in data:
        if slownik['city'] != None:
            if slownik['city']['name'] == city:
                stacje_w_miescie.append(slownik)
        else:
            if slownik['stationName'] == city:
                stacje_w_miescie.append(slownik)
    if len(stacje_w_miescie) == 0:
        return 'Brak danych'
    else:
        return stacje_w_miescie
    
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

def get_sensors_for_city(city):
    stacja = get_measuring_stations_for_city(city)
    if stacja == 'Brak danych':
        return 'Brak danych'
    else:
        for slown in stacja:
            return get_sensors(slown['id'])
        
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

def poziom_zagrożenia_dla_stacji(station_id):
    wyniki = stan_zanieczyszczen_dla_stacji(station_id)
    if type(wyniki) == list:
        for slow in wyniki:
            if slow['key'] == 'PM10':
                if type(slow['values'][0]['value']) == float:
                    if slow['values'][0]['value'] <= 50.00:
                        print('Poziom dopuszalny')
                    elif slow['values'][0]['value'] <= 200.00:
                        print('Poziom informowania')
                    elif slow['values'][0]['value'] >= 300.00:
                        print('Poziom alarmowy')
                else:
                    print('Brak aktualnych danych dla PM10.')
    else:
        return 'Brak danych'
        


def current_state_for_city(city):
    stan_pomiar = get_sensors_for_city(city)
    stan_miasto = []
    aktualny_stan_miasto_CO = []
    aktualny_stan_miasto_PM10 = []
    aktualny_stan_miasto_C6H6 = []
    aktualny_stan_miasto_NO2 = []
    aktualny_stan_miasto_PM25 = []
    aktualny_stan_miasto_O3 = []
    aktualny_stan_miasto_SO2 = []
    
    if stan_pomiar == 'Brak danych':
        return 'Brak danych'
    else:
        for lista in stan_pomiar:
            for slo in lista:
                URL = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/{}'.format(slo['id'])
                f = requests.get(URL)
                wynik1 = json.loads(f.text)
                stan_miasto.append(wynik1)
    
    for y in stan_miasto:
        if y['key'] == 'CO' and y['values'][0]['value'] != None:
            aktualny_stan_miasto_CO.append(y['values'][0]['value'])
        elif y['key'] == 'PM10' and y['values'][0]['value'] != None:
            aktualny_stan_miasto_PM10.append(y['values'][0]['value'])
        elif y['key'] == 'C6H6' and y['values'][0]['value'] != None:
            aktualny_stan_miasto_C6H6.append(y['values'][0]['value'])
        elif y['key'] == 'NO2' and y['values'][0]['value'] != None:
            aktualny_stan_miasto_NO2.append(y['values'][0]['value'])
        elif y['key'] == 'PM2.5' and y['values'][0]['value'] != None:
            aktualny_stan_miasto_PM25.append(y['values'][0]['value'])
        elif y['key'] == 'O3' and y['values'][0]['value'] != None:
            aktualny_stan_miasto_O3.append(y['values'][0]['value'])
        elif y['key'] == 'SO2' and y['values'][0]['value'] != None:
            aktualny_stan_miasto_SO2.append(y['values'][0]['value'])
    
    srednie_wskazania = []   
    if len(aktualny_stan_miasto_CO) > 0:
        midCO = sum(aktualny_stan_miasto_CO) / len(aktualny_stan_miasto_CO)
        srednie_wskazania.append({'CO' : midCO})
        
    if len(aktualny_stan_miasto_PM10) > 0:
        midPM10 = sum(aktualny_stan_miasto_PM10) / len(aktualny_stan_miasto_PM10)
        srednie_wskazania.append({'PM10' : midPM10})
        
    if len(aktualny_stan_miasto_C6H6) > 0:
        midC6H6 = sum(aktualny_stan_miasto_C6H6) / len(aktualny_stan_miasto_C6H6)
        srednie_wskazania.append({'C6H6' : midC6H6})
    
    if len(aktualny_stan_miasto_NO2) > 0:
        midNO2 = sum(aktualny_stan_miasto_NO2) / len(aktualny_stan_miasto_NO2)
        srednie_wskazania.append({'NO2' : midNO2})
    
    if len(aktualny_stan_miasto_PM25) > 0:
        midPM25 = sum(aktualny_stan_miasto_PM25) / len(aktualny_stan_miasto_PM25)
        srednie_wskazania.append({'PM2.5' : midPM25})
    
    if len(aktualny_stan_miasto_O3) > 0:
        midO3 = sum(aktualny_stan_miasto_O3) / len(aktualny_stan_miasto_O3)
        srednie_wskazania.append({'O3' : midO3})
    
    if len(aktualny_stan_miasto_SO2) > 0:
        midSO2 = sum(aktualny_stan_miasto_SO2) / len(aktualny_stan_miasto_SO2)
        srednie_wskazania.append({'SO2' : midSO2})
        
       
    if len(srednie_wskazania) == 0:
        return 'Brak aktualnych danych'
    else:
        return srednie_wskazania
    
