"""
BUT: lister tous les titres des entrées de noms de séries Allocine de la page 1 de leur site (avec une boucle sur les numéros de page on peut lister ceux de toutes les pages), et obtenir les URL associées à ces entrées de série, puis charger les pages associées à ces entrées et utiliser le parser pour aller chercher le nombre de saisons de la série dans la page chargée pour une série donnée.
"""

from html.parser import HTMLParser
import urllib.request

# On démarre de la page n°1 des séries de Allociné
url = "https://www.allocine.fr/series/ficheserie_gen_cserie=49.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# On cherche toutes les balises "<a>" de classe "meta-title-link"
job_elements = soup.find_all("a", class_="meta-title-link")

listeURLaParcourir=[]
listeNOMSerie=[]
for balise in job_elements:
    # On affiche l'attribut choisi avec des crochets: le "href"
    listeURLaParcourir.append(balise["href"])
    # On affiche le contenu texte de la balise en question avec l'attribut "text"
    listeNOMSerie.append(balise.text)

print("\nListe des NOMS des acteurs:\n",listeNOMSerie)
print('-------------\n')
print("\nListe des URLs associées:\n",listeURLaParcourir)
print('-------------\n')

nbseries=len(listeNOMSerie)

listeSaisons=[]

# Chargement des URL associées
for i in range(nbseries):
    urlSecondaire = ("https://www.allocine.fr"+listeURLaParcourir[i])
    pageSecondaire = requests.get(urlSecondaire)
    soupsecondaire = BeautifulSoup(pageSecondaire.content, "html.parser")
    print(soupsecondaire)
"""
    # On cherche toutes les balises "<div>" de classe "stats-number"
    elements_number = soupsecondaire.find_all("div", class_="stats-number")
    # On cherche toutes les balises "<div>" de classe "stats-info"
    elements_info= soupsecondaire.find_all("div", class_="stats-info")

    # On parcourt chaque balise <div> de classe "stats-nfo" trouvée
    for j in range(len(elements_info)):
        # Si le texte de la balise est "Saisons" ou "Saison"
        if (elements_info[j].text=="Saisons") or (elements_info[j].text=="Saison"):
            # Alors on récupère le texte de la balise number qui est en même position (car il y a plusieurs balises <div> de classe "stats-number", une associée avec chaque type d'information affichée, et on ne veut garder que celle qui va avec la "stats-info" qui parle de Saisons
            lasaison=elements_number[j].text

            # On ajoute à la liste des saisons
            listeSaisons.append(lasaison)
            print(listeNOMSerie[i],":",lasaison,"saison(s)")
