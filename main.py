# REQUIREMENTS:
# pip install colorama==0.4.6
# pip install dnspython==2.7.0
# pip install opencage==3.1.0
# pip install requests==2.32.3
# pip install shodan==1.31.0



#!/usr/bin/python
import requests
import os
import time
from platform import system
from opencage.geocoder import OpenCageGeocode
import json
from datetime import datetime

class colores:
    red="\033[31;1m"

os.system("clear")
logo = colores.red + '''
             ▄▀▀█▀▄    ▄▀▀▄▀▀▀▄                      ▄▀▀▀▀▄   ▄▀▀█▄▄▄▄  ▄▀▀▀▀▄  
            █   █  █  █   █   █                     █        ▐  ▄▀   ▐ █      █ 
            ▐   █  ▐  ▐  █▀▀▀▀                      █    ▀▄▄   █▄▄▄▄▄  █      █ 
                █        █                          █     █ █  █    ▌  ▀▄    ▄▀ 
             ▄▀▀▀▀▀▄   ▄▀      Made By:     LTH     ▐▀▄▄▄▄▀ ▐ ▄▀▄▄▄▄     ▀▀▀▀   
            █       █ █                             ▐         █    ▐            
            ▐       ▐ ▐                                       ▐                 
             ▄▀▀▀▀▄    ▄▀▀▀▀▄   ▄▀▄▄▄▄   ▄▀▀█▄   ▄▀▀▀█▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄   
            █    █    █      █ █ █    ▌ ▐ ▄▀ ▀▄ █    █  ▐ ▐  ▄▀   ▐ █   █   █   
            ▐    █    █      █ ▐ █        █▄▄▄█ ▐   █       █▄▄▄▄▄  ▐  █▀▀█▀    
                █     ▀▄    ▄▀   █       ▄▀   █    █        █    ▌   ▄▀    █    
              ▄▀▄▄▄▄▄▄▀ ▀▀▀▀    ▄▀▄▄▄▄▀ █   ▄▀   ▄▀        ▄▀▄▄▄▄   █     █     
              █                █     ▐  ▐   ▐   █          █    ▐   ▐     ▐     
              ▐                ▐                ▐          ▐                    
  

         '''  

try:
    print(logo)
    print('[~] Enter the IP: ')
    ip = input('[~] IP: ')
    print(f'[~] Looking up data for: {ip}')
    time.sleep(2)

    api = f"http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query&lang=es"
    data = requests.get(api).json()

    print("\n[~] Basic Information:")
    print("[~] [IP]:", data['query'])
    print("[~] [ISP]:", data.get('isp', 'Not found'))
    print("[~] [Organization]:", data.get('org', 'Not found'))
    print("[~] [AS Number and Organization]:", data.get('as', 'Not found'))

    print("\n[~] Location Information:")
    print("[~] [City]:", data.get('city', 'Not found'))
    print("[~] [Region / State]:", data.get('regionName', 'Not found'))
    print("[~] [Country]:", data.get('country', 'Not found'))
    print("[~] [Continent]:", data.get('continent', 'Not found'))
    print("[~] [Postal Code]:", data.get('zip', 'Not found'))
    print("[~] [Latitude]:", data.get('lat', 'Not found'))
    print("[~] [Longitude]:", data.get('lon', 'Not found'))
    print("[~] [Timezone]:", data.get('timezone', 'Not found'))

    print("\n[~] Network Information:")
    print("[~] [Mobile Network]:", "Yes" if data.get('mobile', False) else "No")
    print("[~] [Proxy/VPN]:", "Yes" if data.get('proxy', False) else "No")
    print("[~] [Hosting/Datacenter]:", "Yes" if data.get('hosting', False) else "No")
    print("[~] [Reverse DNS]:", data.get('reverse', 'Not found'))

    try:
        additional_data = requests.get(f"https://ipapi.co/{ip}/json/").json()
        print("\n[~] Additional Information:")
        print("[~] [Network]:", additional_data.get('network', 'Not found'))
        print("[~] [Version]:", additional_data.get('version', 'Not found'))
        print("[~] [Region Code]:", additional_data.get('region_code', 'Not found'))
        print("[~] [Country Population]:", additional_data.get('country_population', 'Not found'))
        print("[~] [Country Area]:", additional_data.get('country_area', 'Not found'))
        print("[~] [Country Capital]:", additional_data.get('country_capital', 'Not found'))
        print("[~] [Country TLD]:", additional_data.get('country_tld', 'Not found'))
        print("[~] [Country Calling Code]:", additional_data.get('country_calling_code', 'Not found'))
        print("[~] [Languages]:", additional_data.get('languages', 'Not found'))
    except:
        print("\n[~] Could not fetch additional information")

    try:
        geocoder = OpenCageGeocode("588cee3f6bb849e5b820389669e6c3b9")
        results = geocoder.reverse_geocode(data['lat'], data['lon'])

        admin_url = f"https://nominatim.openstreetmap.org/reverse?lat={data['lat']}&lon={data['lon']}&format=json&addressdetails=1"
        admin_headers = {'User-Agent': 'Spyrod/4.0'}
        admin_response = requests.get(admin_url, headers=admin_headers).json()

        if results and len(results):
            address = results[0]
            components = address.get('components', {})
            admin_details = admin_response.get('address', {})

            print("\n[~] Enhanced Location Information:")
            print(f"[~] [Full Address]: {address['formatted']}")
            print(f"[~] [Building Number]: {components.get('house_number', admin_details.get('house_number', 'Not found'))}")
            print(f"[~] [Street]: {components.get('road', admin_details.get('road', 'Not found'))}")
            print(f"[~] [Building Name]: {components.get('building', admin_details.get('building', 'Not found'))}")
            print(f"[~] [Neighborhood/Suburb]: {components.get('suburb', components.get('neighbourhood', admin_details.get('suburb', 'Not found')))}")
            print(f"[~] [District]: {components.get('district', admin_details.get('district', admin_details.get('city_district', 'Not found')))}")
            print(f"[~] [Quarter]: {components.get('quarter', admin_details.get('quarter', admin_details.get('neighbourhood', 'Not found')))}")
            print(f"[~] [Postcode]: {components.get('postcode', admin_details.get('postcode', 'Not found'))}")
            print(f"[~] [Municipality]: {components.get('municipality', admin_details.get('municipality', admin_details.get('city', 'Not found')))}")
            print(f"[~] [Borough]: {components.get('borough', admin_details.get('borough', 'Not found'))}")
            print(f"[~] [Locality]: {components.get('locality', admin_details.get('locality', 'Not found'))}")
            print(f"[~] [City]: {components.get('city', components.get('town', components.get('village', admin_details.get('city', 'Not found'))))}")
            print(f"[~] [County]: {components.get('county', admin_details.get('county', 'Not found'))}")
            print(f"[~] [State/Province]: {components.get('state', admin_details.get('state', 'Not found'))}")
            print(f"[~] [Country]: {components.get('country', admin_details.get('country', 'Not found'))}")

            if 'annotations' in address:
                annotations = address['annotations']
                print("\n[~] Location Context:")
                print(f"[~] [Type]: {annotations.get('type', 'Not found')}")
                print(f"[~] [What3Words]: {annotations.get('what3words', 'Not found')}")
                if 'OSM' in annotations:
                    print(f"[~] [OSM URL]: https://www.openstreetmap.org/{annotations.get('OSM', {}).get('url', 'Not found')}")

                if 'confidence' in address:
                    print(f"[~] [Location Confidence]: {address['confidence']}/10")

    except Exception as e:
        print("\n[~] Could not fetch detailed location information")

except KeyboardInterrupt:
    print('\nDone.')
    time.sleep(1)
except Exception as e:
    print(f"\n[~] Error occurred: {str(e)}")

while True:
    endchoice = input("\n// Done Tracking, Choose 'r' to rerun script, or choose 'm' to go back to main. : ")
    if endchoice == 'r':
        os.system('cls' if os.name == 'nt' else 'clear')
        os.system('python main.py')
    elif endchoice == 'm':
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()
    else:
        print("Invalid option. Please try again.")
