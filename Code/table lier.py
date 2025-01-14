import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
os.chdir('U:/S3/BDD')

## Créer la table lier
data_relation = pd.read_csv("friends_relationships_id_with_relation.csv", sep = ";")
episodes = pd.read_excel('episode.xlsx')
columns = ['ID_ep', 'ID_personnage', 'ID_personnage_1', 'ID_relation']
lier = pd.DataFrame(columns=columns)
for i in range(len(data_relation)):
    list_ep = data_relation.iloc[i,5]
    list_ep = list_ep.strip("[]").replace("'","")
    list_ep = list_ep.replace(" ","").split(',')
    for ep in list_ep:
        lier.loc[len(lier)] = [ep,data_relation.iloc[i,3],data_relation.iloc[i,7],data_relation.iloc[i,6]]

lier.to_csv("lier.csv", index=False, sep=";", encoding='utf-8')
