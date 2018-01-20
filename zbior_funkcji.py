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
        lista_stanowisk_pomiarowych = json.loads(s.text)
        return lista_stanowisk_pomiarowych

def get_sensors_for_city(city):
    stacje = get_measuring_stations_for_city(city)
    stanowiska_w_miescie = []
    if stacje == 'Brak danych':
        return 'Brak danych'
    else:
        for slown in stacje:
            stanowiska_w_miescie.append(get_sensors(slown['id']))
        return stanowiska_w_miescie
        
def stan_zanieczyszczen_dla_stacji(station_id):
    stanowiska = get_sensors(station_id)
    wskazania_dla_stacji = []
    if type(stanowiska) == list:
        for ident in stanowiska:
            URL = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/{}'.format(ident['id'])
            b = requests.get(URL)
            wynik = json.loads(b.text)
            wskazania_dla_stacji.append(wynik)
        return wskazania_dla_stacji

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
        


def current_state_for_city(city):
    stan_pomiar = get_sensors_for_city(city)
    stan_miasto = []
    
    if stan_pomiar == 'Brak danych':
        return 'Brak danych'
    else:
        for lista in stan_pomiar:
            for slo in lista:
                URL = 'http://api.gios.gov.pl/pjp-api/rest/data/getData/{}'.format(slo['id'])
                f = requests.get(URL)
                wynik1 = json.loads(f.text)
                stan_miasto.append(wynik1)
    
    aktualne_pomiary = []
    
    for y in stan_miasto:
        if y['values'][0]['value'] != None:
            aktualne_pomiary.append({y['key'] : y['values'][0]['value']})
                      
    merged_measures = defaultdict(list)
    for slowniki in aktualne_pomiary:
        for key, value in chain(slowniki.items()):
            merged_measures[key].append(value)
    
    totally_merged_measures = []
    for k, v in merged_measures.items():
        totally_merged_measures.append({k : ((sum(v) / len(v)))})
        
    return totally_merged_measures
    
