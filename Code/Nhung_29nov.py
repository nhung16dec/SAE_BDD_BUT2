import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
url = "https://fr.wikipedia.org/wiki/Friends"

## Acteurs principaux
def get_element(url, tag, class_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    element = soup.find(tag, class_=class_name)
    if element:
        return element
    else:
        return "Erreur"

def extract_birthday_from_url(row):
    url_act = "https://fr.wikipedia.org" + row['URL_Act']
    url_per = "https://fr.wikipedia.org" + row['URL_Per']
    class_name = 'nowrap bday'
    tag = 'time'
    bday_act = get_element(url_act, tag, class_name).text
    bday_per = get_element(url_per, tag, class_name).text
    return pd.Series([bday_act, bday_per], index=['bday_act', 'bday_per'])

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', class_='wikitable centre')
table = get_element(url,'table','wikitable centre')
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


# Appliquer la fonction pour extraire les dates de naissance
df_acteur[['bday_act', 'bday_per']] = df_acteur.apply(extract_birthday_from_url, axis=1)
df_acteur['stt_invite'] = 0
# Afficher le DataFrame final avec les dates de naissance
print(df_acteur)
#Vérifier
print(df_acteur.iloc[1])

## Acteurs secondaires

# URL du site à scraper
url = "https://www.fanfr.com/invites/friendsgeneration2.php?importance=Celebrite&actioninv=Rechercher"



# URL de la page web
url = "https://www.fanfr.com/invites/friendsgeneration2.php?importance=Celebrite&actioninv=Rechercher"

# Envoi de la requête HTTP pour obtenir le contenu de la page
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Listes pour stocker les données
    personnages = []
    acteurs = []
    episodes_list = []

    # Trouver toutes les sections <a> contenant le lien 'invite'
    sections = soup.find_all('a', href=lambda href: href and 'invite' in href)

    # Parcourir les sections
    for i, section in enumerate(sections):
        # Extraire le nom du personnage et de l'acteur (2 balises <b>)
        b_tags = section.find_all_next('b', limit=2)

        # Si la section contient des balises <b>, on les ajoute à la liste
        if len(b_tags) >= 2:
            personnage = b_tags[0].text.strip() if b_tags else 'Inconnu'
            acteur = b_tags[1].text.strip() if b_tags else 'Inconnu'

            personnages.append(personnage)
            acteurs.append(acteur)

            # Extraire les épisodes associés à cet invité
            episodes = [ep['href'].split('=')[-1] for ep in section.find_all_next('a', href=lambda href: href and 'episode' in href)]
            episodes_list.append(", ".join(episodes))

    # Création du DataFrame
    data = {
        "Personnage": personnages,
        "Acteur": acteurs,
        "Episodes": episodes_list
    }

    # Organiser les données en commençant à partir du numéro 5
    df = pd.DataFrame(data)
    df.index = range(5, 5 + len(df))  # Commence à partir de 5

    # Affichage du DataFrame
    print(df)
else:
    print(f"Impossible d'accéder à la page, code erreur : {response.status_code}")

# Supposons que 'df' soit le DataFrame contenant les colonnes 'personnage' et 'acteur'
df = df[~((df['Personnage'].str.contains('fanfr.com', case=False, na=False)) &
          (df['Acteur'].str.contains('Fan Club', case=False, na=False)))]

df.to_csv("friends_data.csv", index=False, sep=";", encoding='utf-8')




