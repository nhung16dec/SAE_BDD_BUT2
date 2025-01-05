import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
os.chdir('C:/Users/trann/Documents/IUT/sem 3/SAE/BDD')
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

url = "https://www.fanfr.com/invites/friendsgeneration2.php?importance=Celebrite&actioninv=Rechercher"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

paragraphs = soup.find_all('p')

data = []
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
            data.append([col1, col2, episode_links])
df = pd.DataFrame(data)
df.columns = ['personnage', 'acteur','episode']
df.to_csv("friends_data.csv", index=False, sep=";", encoding='utf-8')
## Récupérer des liens des invités
url = "https://www.fanfr.com/invites/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
list_link = []
links = soup.find_all('a',href=lambda href: href and 'friendsgeneration2.php?importance=' in href)
for link in links:
    result_link = "https://www.fanfr.com/invites/"+link['href']
    list_link.append(result_link)
## Fonction pour récupérer les données
data = []
def collect_data_from_page(html,group):

    soup = BeautifulSoup(html, 'html.parser')
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
                data.append([col1, col2, episode_links,group])

## Parcourir les liens pour récupérer les données

data = []

driver = webdriver.Chrome()

try:
    for url in list_link:
        group = url.split('importance=')[-1].split('&action')[0]
        print(f"On est à: {url}")

        driver.get(url)
        time.sleep(3)

        collect_data_from_page(driver.page_source,group)

        while True:
            try:
                next_button = driver.find_element(By.LINK_TEXT, "les invités suivants")
                next_button.click()
                time.sleep(3)
                collect_data_from_page(driver.page_source,group)
            except:
                print("Done and next:")
                break

finally:
    driver.quit()
df = pd.DataFrame(data)
df.columns = ['personnage', 'acteur','episode','group']
df.to_csv("friends_data.csv", index=False, sep=";", encoding='utf-8')
## Chercher la date de naissance
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Danh sách các tên
names = ["Brad Pitt", "Angelina Jolie", "Leonardo DiCaprio"]

# Khởi tạo trình duyệt
driver = webdriver.Chrome()

# Vòng lặp tìm kiếm và nhấp vào Wikipedia
for name in names:
    try:
        # Mở trang tìm kiếm DuckDuckGo
        driver.get("https://duckduckgo.com/")

        # Tìm ô nhập liệu tìm kiếm
        search_box = driver.find_element(By.NAME, "q")

        # Nhập tên và nhấn Enter
        search_box.send_keys(name + " site:wikipedia.org")
        search_box.send_keys(Keys.RETURN)

        # Chờ kết quả tải
        time.sleep(3)

        # Tìm liên kết đầu tiên chứa "wikipedia.org"
        first_result = driver.find_element(By.XPATH, "(//a[contains(@href, 'wikipedia.org')])[1]")  # Tìm phần tử chứa liên kết Wikipedia
        first_result.click()  # Nhấp vào liên kết đầu tiên
        time.sleep(3)  # Chờ trang Wikipedia tải xong

        # Trích xuất ngày tháng năm sinh từ infobox
        try:
            # Tìm infobox, phần chứa thông tin về ngày tháng năm sinh
            birth_date_element = driver.find_element(By.XPATH, "//table[contains(@class, 'infobox')]//th[contains(text(), 'Born')]//following-sibling::td")
            birth_date = birth_date_element.text
            print(f"{name}: Ngày tháng năm sinh: {birth_date}")
        except Exception as e:
            print(f"Không tìm thấy ngày sinh của {name}: {e}")

    except Exception as e:
        print(f"Lỗi khi xử lý '{name}': {e}")

# Đóng trình duyệt
driver.quit()

