import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
url = "https://fr.wikipedia.org/wiki/Friends"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', class_='wikitable centre')
table = get_element_text(url,'table','wikitable centre')
liste_act = []
liste_URL_act = []
liste_per = []
liste_URL_per = []
if table:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            col1 = cols[0].get_text()
            a_tag = cols[0].find('a')
            if a_tag:
                link_col1 = a_tag.get('href')
            col2 = cols[1].get_text()
            a_tag2 = cols[1].find('a')
            if a_tag2:
                link_col2 = a_tag2.get('href')
            liste_act.append(col1)
            liste_URL_act.append(link_col1)
            liste_per.append(col2)
            liste_URL_per.append(link_col2)
else:
    print("Erreur")
df_acteur = pd.DataFrame({
    'Act': liste_act,
    'URL_Act': liste_URL_act,
    'Per': liste_per,
    'URL_Per': liste_URL_per
})

urlSecondaire = ("https://fr.wikipedia.org"+"/wiki/Jennifer_Aniston")
pageSecondaire = requests.get(urlSecondaire)
soupsecondaire = BeautifulSoup(pageSecondaire.text, 'html.parser')
elements_info = soupsecondaire.findAll("time", class_ ='nowrap bday')
for element in elements_info:
    print(element.text)

def get_element_text(url, tag, class_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    element = soup.find(tag, class_=class_name)
    if element:
        return element.text
    else:
        return "Erreur"

def extract_birthday_from_url(row):
    url_act = "https://fr.wikipedia.org" + row['URL_Act']
    url_per = "https://fr.wikipedia.org" + row['URL_Per']
    class_name = 'nowrap bday'
    tag = 'time'
    bday_act = get_element_text(url_act, tag, class_name)
    bday_per = get_element_text(url_per, tag, class_name)
    return pd.Series([bday_act, bday_per], index=['bday_act', 'bday_per'])

# Appliquer la fonction pour extraire les dates de naissance
df_acteur[['bday_act', 'bday_per']] = df_acteur.apply(extract_birthday_from_url, axis=1)

# Afficher le DataFrame final avec les dates de naissance
print(df_acteur)























