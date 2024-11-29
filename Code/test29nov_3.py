"""
BUT: lister tous les titres des entrées de noms de séries Allocine de la page 1 de leur site (avec une boucle sur les numéros de page on peut lister ceux de toutes les pages), et obtenir les URL associées à ces entrées de série, puis charger les pages associées à ces entrées et utiliser le parser pour aller chercher le nombre de saisons de la série dans la page chargée pour une série donnée.
"""

from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup

# On démarre de la page n°1 des séries de Allociné
url = "https://www.fanfr.com/invites/friendsgeneration2.php?n1=&nom=&a1=&acteur=&categorie=Petit%20Ami&lien=Joey&actioninv=Rechercher"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# On cherche toutes les balises "<a>" de classe "meta-title-link"
# job_elements = soup.find_all("a", class_="friendsgeneration2.php")

listeURLaParcourir=[]
listeNOMSerie=[]
for balise_1 in soup.find_all("b"):
    # On affiche le contenu texte de la balise en question avec l'attribut "text"
    listeNOMSerie.append(balise_1)
for balise_2 in balise_1.find_all("a"):
    print(balise_2)

print("\nListe des NOMS des petites-amies de Joey:\n",listeNOMSerie)
print('-------------\n')
print("\nListe des URLs associées:\n",listeURLaParcourir)
print('-------------\n')

nbseries=len(listeNOMSerie)

listeSaisons=[]

# Chargement des URL associées
#for i in range(nbseries):
    #urlSecondaire = ("https://www.allocine.fr"+listeURLaParcourir[i])
    #pageSecondaire = requests.get(urlSecondaire)
    #soupsecondaire = BeautifulSoup(pageSecondaire.content, "html.parser")
    #print(soupsecondaire)