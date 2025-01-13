import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
import pandas as pd
import time

# Fonction pour scraper IMDB

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_imdb():
    imdb_data = []
    for season_number in range(1, 11):
        url = "https://www.imdb.com/title/tt0108778/episodes?season=" + str(season_number)
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            episodes = soup.find_all("span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")
            
            for episode_number, container in enumerate(episodes, 1):
                rating = container.find("span", class_="ipc-rating-star--rating")
                
                vote_element = container.find("span", class_="ipc-rating-star--voteCount")
                votes = vote_element.text.strip() if vote_element else "0"  # Par défaut à "0" si absent
                
                # Nettoyer et convertir les votes
                votes = votes.replace("(", "").replace(")", "").replace(",", "").strip()
                if "K" in votes:
                    votes = float(votes.replace("K", "")) * 1000
                votes = int(votes)
                imdb_data.append({
                    "Source": "IMDB",
                    "Saison": season_number,
                    "Épisode": str(season_number) + "{:02}".format(episode_number),
                    "Note": rating.text.strip() if rating else "Non disponible",
                    "Votes": votes if votes else "0",
                    "Note_Saison": None
                })
    return imdb_data

# Fonction pour scraper SensCritique
def scrape_senscritique():
    driver = webdriver.Chrome(options=webdriver.ChromeOptions().add_argument('--headless'))
    base_url = "https://www.senscritique.com/serie/friends/484823/"
    senscritique_data = []

    for season in range(1, 11):
        driver.get(base_url + "S" + str(season))
        time.sleep(5)  # Temps d'attente pour charger la page
        WebDriverWait(driver, 10).until(
            presence_of_all_elements_located((By.XPATH, '//div[@data-testid="Rating"]'))
        )
        ratings = driver.find_elements(By.XPATH, '//div[@data-testid="Rating"]')
        note_saison = ratings[0].text.strip() if ratings else None
        if ratings:
            # Ajouter la note de la saison entière à senscritique_data
            senscritique_data.append({
                "Source": "SensCritique",
                "Saison": season,
                "Épisode": "Saison entière",
                "Note": None,
                "Votes": None,
                "Note_Saison": note_saison
            })
            # Notes des épisodes (le reste des notes)
            for episode_number, rating in enumerate(ratings[1:], 1):
                senscritique_data.append({
                    "Source": "SensCritique",
                    "Saison": season,
                    "Épisode": str(season) + "{:02}".format(episode_number),
                    "Note": rating.text.strip(),
                    "Votes": None,
                    "Note_Saison": note_saison
                })
    driver.quit()
    return senscritique_data


# Fonction pour scraper Allociné
def scrape_allocine():
    urls = ["https://www.allocine.fr/series/ficheserie-49/critiques/saison-" + str(79 + i) + "/" for i in range(9)]
    urls.append("https://www.allocine.fr/series/ficheserie-49/critiques/saison-440/")  # Dernière saison
    allocine_data = []
    for i, url in enumerate(urls, start=1):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            note = soup.find("span", class_="note")
            voters = soup.find("span", class_="user-note-count")
            allocine_data.append({
                "Source": "Allociné",
                "Saison": (i-1) + 1,
                "Épisode": "Saison entière",
                "Note": None,
                "Votes": voters.text.strip() if voters else "Non disponible",
                "Note_Saison": note.text.strip() if note else "Non disponible"
            })
    return allocine_data


# Fusion des données
def main():
    data = scrape_imdb() + scrape_senscritique() + scrape_allocine()
    
    # Création des feuilles Excel
    site_data = [{"id_site": 1, "nom_site": "IMDB"}, {"id_site": 2, "nom_site": "SensCritique"}, {"id_site": 3, "nom_site": "Allociné"}]
    episodes_data = []
    saisons_data = []

    for row in data:
        site_id = 1 if row["Source"] == "IMDB" else 2 if row["Source"] == "SensCritique" else 3
        if row["Épisode"] == "Saison entière":
            saisons_data.append({
                "id_saison": str(row['Saison']),
                "id_site": site_id,
                "note_saison": row["Note_Saison"],
                "nb_votes": row["Votes"]
            })
        else:
            episodes_data.append({
                "id_episode": row["Épisode"],
                "id_site": site_id,
                "note_episode": row["Note"],
                "nb_votant": row["Votes"]
            })

    # Sauvegarde dans Excel
    with pd.ExcelWriter("test6.xlsx") as writer:
        pd.DataFrame(site_data).to_excel(writer, sheet_name="Feuille1", index=False)
        pd.DataFrame(episodes_data).to_excel(writer, sheet_name="Feuille2", index=False)
        pd.DataFrame(saisons_data).to_excel(writer, sheet_name="Feuille3", index=False)

    print("Données fusionnées sauvegardées dans series_notes_combined.xlsx")

if __name__ == "__main__":
    main()
