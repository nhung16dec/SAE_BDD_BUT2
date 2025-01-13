import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Étape 1 : Récupération des titres des épisodes
print("Récupération des titres des épisodes...")
url_titles = "https://fr.wikipedia.org/wiki/Liste_des_%C3%A9pisodes_de_Friends"
response_titles = requests.get(url_titles)

# Vérification de la réponse HTTP
if response_titles.status_code != 200:
    print("Erreur : Impossible de récupérer la liste des titres.")
    exit()

soup_titles = BeautifulSoup(response_titles.text, 'html.parser')
episode_sections = soup_titles.find('div', class_='mw-parser-output')

episode_titles = []
if episode_sections:
    for ol in episode_sections.find_all('ol'):
        for li in ol.find_all('li'):
            title_text = li.get_text(strip=True)
            if title_text:
                episode_titles.append(title_text.split("(")[0].strip())

print(f"Nombre de titres récupérés : {len(episode_titles)}")

# Étape 2 : Récupération des résumés des épisodes
print("Récupération des résumés détaillés...")
all_episodes = []
for season in range(1, 11):  # De la saison 1 à la saison 10
    print(f"Traitement de la saison {season}...")
    url = f"https://fr.wikipedia.org/wiki/Saison_{season}_de_Friends"
    response = requests.get(url)

    # Vérification de la réponse HTTP
    if response.status_code != 200:
        print(f"Erreur : Impossible de récupérer la page pour la saison {season}.")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    summary_headers = soup.find_all('b', string="Résumé détaillé")

    # Réinitialiser le compteur des épisodes dans la saison
    episode_in_season = 1

    for header in summary_headers:
        summary_div = header.find_next('div', style="padding-left:25px")
        if summary_div:
            summary_text = summary_div.get_text(strip=True)
            # Associer le titre correspondant ou un titre par défaut
            title = episode_titles.pop(0) if episode_titles else "Titre inconnu"
            episode_id = season * 100 + episode_in_season  # Générer l'ID de l'épisode
            all_episodes.append({
                "id_episode": episode_id,               # ID combiné saison + numéro épisode
                "num_episode": episode_in_season,
                "id_saison": season,
                "nom_episode": title,
                "resume_episode": summary_text
            })
            episode_in_season += 1  # Incrémente uniquement dans la saison

print(f"Nombre total d'épisodes traités : {len(all_episodes)}")

# Sauvegarde des données
output_excel_path = os.path.join("resumes_friends_complets.xlsx")
print(f"Sauvegarde des résumés dans le fichier Excel : {output_excel_path}...")
df = pd.DataFrame(all_episodes)
df.to_excel(output_excel_path, index=False)

print("Fichier Excel créé avec succès.")
