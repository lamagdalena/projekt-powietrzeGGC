import json
import requests

    
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

     

import matplotlib.pyplot as plt

def wykres_zanieczyszczenia_dla_stacji(station_id):
    dane1 = stan_zanieczyszczen_dla_stacji(station_id)
    PM10 = []
    NO2 = []
    PM25 = []
    O3 = []
    SO2 = []
    CO = []
    C6H6 = []
    czas = []
    
    if type(dane1) == list:
        for slownik in dane1:
            for slownik2 in slownik['values'][0:24]:
                czas.append(slownik2['date'])
                if slownik['key'] == 'PM10':
                    PM10.append(slownik2['value'])
                elif slownik['key'] == 'NO2':
                    NO2.append(slownik2['value'])
                elif slownik['key'] == 'PM2.5':
                    PM25.append(slownik2['value'])
                elif slownik['key'] == 'O3':
                    O3.append(slownik2['value'])
                elif slownik['key'] == 'SO2':
                    SO2.append(slownik2['value'])
                elif slownik['key'] == 'CO':
                    CO.append(slownik2['value'])
                elif slownik['key'] == 'C6H6':
                    C6H6.append(slownik2['value'])
    
    if len(PM10) < 1:
        for x in range(1, 25):
            PM10.append(None)  
            
    if len(NO2) < 1:
        for x in range(1, 25):
            NO2.append(None)
            
    if len(PM25) < 1:
        for x in range(1, 25):
            PM25.append(None)
            
    if len(O3) < 1:
        for x in range(1, 25):
            O3.append(None)
        
    if len(SO2) < 1:
        for x in range(1, 25):
            SO2.append(None)
            
    if len(CO) < 1:
        for x in range(1, 25):
            CO.append(None)
            
    if len(C6H6) < 1:
        for x in range(1, 25):
            C6H6.append(None)
          
        
    czas = czas[0:24]
    
    if len(czas) < 1:
        print('Brak danych pomiarowych dla podanego numeru stacji')
    else:
        plt.plot(czas, PM10, 'r-', czas, NO2, 'b-' , czas, PM25, 'g-', czas, O3, 'y-', czas, SO2, 'k-', czas, CO, 'r:' , czas, C6H6, 'b:')
        plt.legend(('PM10', 'NO2', 'PM2.5', 'O3', 'SO2', 'CO', 'benzen'))
        plt.xlabel('CZAS')
        plt.ylabel('POZIOM ZANIECZYSZCZENIA')
        plt.title('Wykres zanieczyszczenia od czasu')
        plt.grid(True)
        plt.show()
            
    
   
