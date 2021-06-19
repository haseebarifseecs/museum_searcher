# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:18:32 2020

@author: 19373
"""

import requests
from bs4 import BeautifulSoup
import googlemaps
URL = []
def generate_links(url):
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    htmlContent = requests.get(url,headers={"user-agent":agent}).content
    soup = BeautifulSoup(htmlContent, 'lxml')
    tags = soup.select("i")
    for tag in tags:
        if "Category" not in tag.a['title']:
            URL.append({"title":tag.a['title'], "link":"https://en.wikipedia.org" + tag.a['href']})
        else:
            continue
    URL.append({"title":"pR","link":"https://en.wikipedia.org/wiki/List_of_museums_in_Puerto_Rico"})
    return URL

museum_data = []
def get_data(data):
    API_KEY = "" #Add your API Key Here
    gmaps = googlemaps.Client(key=API_KEY)
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    with open('museum_list_for_elastic.txt', 'w', encoding='utf-8') as f:
        for url in data:
            try:
                link = url.get("link")
                title = url.get("title")
                htmlContent = requests.get(link, headers={"user-agent":agent}).content
                soup = BeautifulSoup(htmlContent, 'lxml')
                table = soup.select(".wikitable.sortable")
                table = table[0]
                rows = table.select("tr")

                for row in rows:
                    try:
                        cell = row.select("td")[0].text
                        cell = cell.strip()
                        places = gmaps.find_place(input=cell,input_type="textquery", fields=['place_id','formatted_address','geometry/location','plus_code'])
                        address = places["candidates"][0]["formatted_address"]
                        geolocation = places["candidates"][0]['geometry']['location']
                        country_ = places['candidates'][0]['plus_code']['compound_code']
                        if(title == "pR"):
                            for i in country_.split(","):
                                if("puerto rico") in i.lower().strip():
                                    museum_json = str({"name":cell,"address":address,"geolocation":geolocation})
                                    print(museum_json)
                                    f.write(museum_json + '\n')
                                    museum_data.append(museum_json)
                                else:
                                    continue
                        else:
                            
                            museum_json = str({"name":cell,"address":address,"geolocation":geolocation})
                            print(museum_json)
                            f.write(museum_json + '\n')
                            museum_data.append(museum_json)

                    except Exception as e:
                        print(str(e))
                        continue
            except Exception as e:
                print(str(e))
                continue
    return museum_data

#print(generate_links("https://en.wikipedia.org/wiki/List_of_museums_in_the_United_States#U.S._territories"))
data = generate_links("https://en.wikipedia.org/wiki/List_of_museums_in_the_United_States#U.S._territories")
#results = get_data([{"title":"pR","link":"https://en.wikipedia.org/wiki/List_of_museums_in_Puerto_Rico"}])
results = get_data(data)
print(results)
#print(data)
print(len(results))


        


