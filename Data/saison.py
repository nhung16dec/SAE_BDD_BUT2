import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Étape 1 : Extraction des informations des saisons depuis Wikipédia
print("Récupération des informations des saisons depuis Wikipédia...")
wiki_url = "https://fr.wikipedia.org/wiki/Liste_des_%C3%A9pisodes_de_Friends"
response = requests.get(wiki_url)
if response.status_code != 200:
    print("Erreur : Impossible de récupérer la page Wikipédia.")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

season_headers = soup.find_all('h2')  # Trouver toutes les balises <h2>
seasons_data = []
id_saison = 1

for header in season_headers:
    if header.find('span', id=True):  # Vérifie la présence d'un attribut ID
        # Extraire le texte du titre de la saison
        season_name = header.get_text(strip=True)

        # Extraire l'année si elle est dans le titre (format "1994-1995")
        year_range = ""
        if "(" in season_name and ")" in season_name:
            year_range = season_name.split("(")[-1].replace(")", "").strip()

        # Ajouter les données de la saison
        seasons_data.append({
            "id_saison": id_saison,
            "nom_saison": season_name,
            "annee_saison": year_range
        })
        id_saison += 1

# Étape 2 : Récupérer les résumés des saisons depuis Allociné
print("\nRécupération des résumés des saisons depuis Allociné...")
urls = [f"https://www.allocine.fr/series/ficheserie-49/saison-{79 + i}/" for i in range(9)]
urls.append("https://www.allocine.fr/series/ficheserie-49/saison-440/")  # Dernière saison

all_summaries = []
for i, url in enumerate(urls, start=1):
    print(f"Traitement de l'URL : {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        season_synopsis = soup.find('div', class_='season-synopsis')
        if season_synopsis:
            summary = season_synopsis.find('p').get_text(strip=True)
            all_summaries.append(summary)
        else:
            all_summaries.append("Résumé non disponible")
    else:
        all_summaries.append(f"Erreur HTTP {response.status_code}")

# Ajouter les résumés aux données des saisons
for i, summary in enumerate(all_summaries):
    if i < len(seasons_data):  # Éviter les erreurs d'indice
        seasons_data[i]["resume_saison"] = summary
    else:
        seasons_data.append({"id_saison": i + 1, "nom_saison": f"Saison {i + 1}", "annee_saison": "", "resume_saison": summary})

# Étape 3 : Sauvegarder les données dans un fichier Excel
output_path = "saisons_friends_complet.xlsx"
print(f"\nSauvegarde des données dans le fichier Excel : {output_path}...")
df = pd.DataFrame(seasons_data)
df.to_excel(output_path, index=False)

print("Fichier Excel créé avec succès.")
