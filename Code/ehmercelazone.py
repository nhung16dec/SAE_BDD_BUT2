import requests
from bs4 import BeautifulSoup
import pandas as pd

# Liste des personnages principaux et leurs types de relation
characters = [
    {"name": "Joey", "relations": ["Petit%20Ami", "Famille", "Ami", "Voisin", "Collègue"]},
    {"name": "Rachel", "relations": ["Petit%20Ami", "Famille", "Ami", "Voisin", "Collègue"]},
    {"name": "Ross", "relations": ["Petit%20Ami", "Famille", "Ams", "Voisin", "Collègue"]},
    {"name": "Monica", "relations": ["Petit%20Ami", "Famille", "Ami", "Voisin", "Collègue"]},
    {"name": "Chandler", "relations": ["Petit%20Ami", "Famille", "Ami", "Voisin", "Collègue"]},
    {"name": "Phoebe", "relations": ["Petit%20Ami", "Famille", "Ami", "Voisin", "Collègue"]},
]

data = []

for character in characters:
    for relation in character['relations']:
        url = f"https://www.fanfr.com/invites/friendsgeneration2.php?n1=&nom=&a1=&acteur=&categorie={relation}&lien={character['name']}&actioninv=Rechercher"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')

        for p in paragraphs:
            b_tags = p.find_all('b')
            if len(b_tags) >= 2:
                col1 = b_tags[0].get_text(strip=True)
                col2 = b_tags[1].get_text(strip=True)

                episode_links = []
                for a in p.find_all('a', href=True):
                    if 'episode' in a['href']:
                        href_value = a['href'].split('=')[-1]
                        episode_links.append(href_value)

                if "Cliquez" not in col1 and "Cliquez" not in col2:
                    data.append([character['name'], relation, col1, col2, episode_links])

# Convertir les données en DataFrame et enregistrer dans un fichier CSV
df = pd.DataFrame(data, columns=['Personnage', 'Relation', 'Personnage lié', 'Acteur lié', 'Episodes'])
df.to_csv("friends_relationships.csv", index=False, sep=";", encoding='utf-8')

print("Données extraites et sauvegardées dans 'friends_relationships.csv'")
