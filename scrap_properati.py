#!/usr/bin/python3

import os, sys
import time
from numpy.random import random

import re
import csv
import json
import requests
from bs4 import BeautifulSoup as bs

#####
#       UTILS
#####

def parse_url( url:str ):
    '''
    Dado un url devuelve objeto parseado de BeautifulSoup
    '''
    n_attempts=5
    for _ in range(n_attempts):    
        try:
            response = requests.get( url )
            
            if response.status_code != 200:
                print('***Error en request. Status code',response.status_code, url)
                continue
            
            return bs( response.content, features="lxml" )
            
        except:
            print('***Error en conexión a', url)
                    
    return None
    
    


def get_links(url_search:str) -> list:
    '''
    Devuelve lista con todos los links a publicaciones de alquileres, dada una
    url de búsqueda con el formato que especifica numero de página
    '''
    URL_PROPERATI='https://www.properati.com.ar'
    urls = []

    soup = parse_url( url_search )
    if not soup: 
        return []
    
    tags = soup.find_all( name='a', attrs={'target':'_blank'} )

    for t in tags:
        attr_href = t['href']
        url_pub = URL_PROPERATI + attr_href
        
        if attr_href.startswith('/detalle') and url_pub not in urls:
            urls.append( url_pub )


    return urls



def find_value(keys: str, dic: dict):
  '''
  Dado una secuencia de keys anidadas en el dict
  Si encuentra cada una de las keys devuelve el valor, buscando recursivamente
  '''
  list_keys = keys.split('.')
  if list_keys[0] in dic:

    if len(list_keys)==1:
      return dic[ list_keys[0] ]
    else:
      new_keys = '.'.join(list_keys[1:])
      return find_value( new_keys, dic[list_keys[0]] )
  
  else:
    return None



def get_data(urls: list) -> list:
    '''
    Dada una lista con urls de publicaciones de properati
    Arma una lista de diccionarios, donde cada uno tiene la misma estructura:
    keys = las keys de to_extract
    values = el valor que tenga el json de cada publicacion en la secuencia de keys definida en los values de to_extract.
    Si el json de una publicacion no contiene una secuencia de keys expresada en un value de to_extract,
    el valor que toma el diccionario es None.
    '''

    data_list = []      
#cada key es la key con la que quedarš¢ registrada cada valor que querramos extraer del json
#cada value es un string con la secuencia de keys a recorrer en el json para extraer el valor deseado
    to_extract = {'ub_calle': 'address.street',
                  'ub_lat': 'geo_point.lat',
                  'ub_lon': 'geo_point.lon',
                  'pr_moneda': 'price.currency',
                  'pr_valor': 'price.amount',
                  'pr_expen': 'maintenance_fees.price.amount',
                  'nu_ambs': 'floor_plan.rooms',
                  'nu_habs': 'floor_plan.bedrooms',
                  'sp_des': 'surface.total',
                  'sp_cub': 'surface.covered',
                  'fe_pub': 'published_on'}
    
    for i, url in enumerate(urls):
#Chequeo si el request sale bien y la publicaciÃ³n estÃ¡ disponible    
        data = {}
        soup = parse_url( url )
        
        try:
            data_json = json.loads( soup.find(name='script', attrs={'id':'__NEXT_DATA__'}).string )        
            d_props = data_json['props']['pageProps']['property']     

            for r, s in to_extract.items():
                data[r] = find_value( s, d_props )
            data['url']=url
            
            print(i, data)
            
            data_list.append(data)                  
            
        except Exception as e:
            print('Exception: ',i, e, url)

    return data_list
    


def save_data(dicts:list, filepath) -> None:

    dirpath = filepath[:filepath.rfind('/')]
    filename = filepath[filepath.rfind('/')+1:]

    if filename in os.listdir(dirpath):   
        mode='a'
    else:               
        mode='x' 
        print(f'No se encontró {filepath}, se creará a continuación.')
    
    with open(filepath, mode) as f:
        writer = csv.DictWriter(f, fieldnames=dicts[0].keys())

        if os.path.getsize(filepath)==0:
            writer.writeheader()
        
        for i, d in enumerate(dicts):
            writer.writerow( d )



#####
#       MAIN
#####

def scrap(url, filename, ni=1, nf=1000):

    for n in range(ni,nf):
        print(f'\tPágina {n}')
        url_page = url + str(n)

        print(f'\t\tSacando links')
        links = get_links(url_page)

        if len(links)==0:
            print('Se alcanzó la última página.')
            break

        print(f'\t\tSacando data')  
        data = get_data(links)  #TARDA 6' POR PÁGINA!!!
        
        print(f'\t\tGuardando data')
        save_data( data, filename ) 
        


if __name__=='__main__':

    DIRECTORY = sys.argv[1]

    URL_SEARCH_PHS  = 'https://www.properati.com.ar/s/capital-federal/ph/alquiler?page='
    URL_SEARCH_CASAS = 'https://www.properati.com.ar/s/capital-federal/casa/alquiler?sort=published_on_desc&page='
    URL_SEARCH_DEPTOS = 'https://www.properati.com.ar/s/capital-federal/departamento/alquiler?sort=published_on_desc&page='

   
    SEARCH = {'phs': URL_SEARCH_PHS,
              'casas': URL_SEARCH_CASAS,
              'deptos': URL_SEARCH_DEPTOS }

    for tipo, url in SEARCH.items():
        TODAY = time.strftime( "%Y-%m-%d", time.localtime() )
        FILEPATH = DIRECTORY + '_'.join([TODAY,tipo,'properati.csv'])

        print(f'Escrapeando {tipo}.\nLos datos se guardarán en {FILEPATH}')
        scrap(url, FILEPATH)
        
    print('Todo OK :)')
