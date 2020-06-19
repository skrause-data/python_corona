# -*- coding: utf-8 -*-
def get_api(land, letzter_tag):
    '''
    Funktion importiert Corona Daten von covid19api.com. 

    Parameters
    ----------
    land : STRING
           Übergebene Werte: germany, italy, switzerland, france, spain, austria, netherlands 
           -> für mehr Länder siehe slugs: https://api.covid19api.com/countries
    letzter_tag : STRING
                  'bergibt den letzten Tag aus der Datenbank.
                  format: YYYY-MM-ddT00:00:00Z

    Returns
    -------
    data : LIST aus Dicts
           Gibt eine verschachtelte Liste (der Zeitraum) aller Werte (dict) zur�ck.
    code : INT 
           Gibt HTML Code aus (z.B. 200)
    
    '''
    
    import requests
    import json
    from datetime import date, timedelta
    
    gestern = date.today() - timedelta(days=1)
    gestern = str(gestern) + "T00:00:00Z"    # Fehlerquelle, dieser zusätzliche String?

    '''
    URLSCHEMA:
    GET By Country   
    https://api.covid19api.com/country/{country}/status/confirmed/live?from={date_from}&to={date_to}
    '''
    
    url = "https://api.covid19api.com/country/" + land + "/status/confirmed/live?from=" + letzter_tag + "&to=" + gestern

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)


    data = response.json()
    code= response.status_code
    
    return data, code
    
    
    




