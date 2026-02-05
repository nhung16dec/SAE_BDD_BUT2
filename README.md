# Création d’une Base de Données SQL pour la Série Friends
## Présentation du projet

Ce projet a été réalisé en équipe de trois étudiants dans le cadre d’un module de Database.
L’objectif est de collecter, nettoyer et stocker des informations sur la série télévisée Friends — notamment les acteurs, les épisodes et les saisons — à l’aide de BeautifulSoup, Python et PostgreSQL.
Le projet met en place une chaîne ETL complète (Extract – Transform – Load) depuis l’extraction web jusqu’au chargement dans la base de données et la vérification des données.

## Structure du projet

### Création du MCD

### Extraction

Utilisation de BeautifulSoup pour récupérer les informations depuis les sources Internet :

- Acteurs : nom d'acteur, nom de personnage, date de naissance d'acteur, date de naissance de personnage .
- Épisodes : titre, rating, numéro de saison.
- Lieu de tournage

### Transformation

- Nettoyage et harmonisation des données : Suppression des doublons et des valeurs manquantes.
- Uniformisation des formats de date.
- Création de tables relationnelles cohérentes (acteurs, épisodes, saisons).

### Chargement

- Création des tables PostgreSQL.
- Insertion des données nettoyées à l’aide de psycopg2.

### Tests

- Requêtes SQL utilisées pour vérifier la base

### Bilan et apprentissages

- Mise en œuvre d’un pipeline ETL complet en Python.
- Pratique de web scraping avancé avec BeautifulSoup.
- Conception d’une base de données relationnelle sous PostgreSQL.
- Travail collaboratif.

## Journal de bord 

Cette section présente l’historique de nos travaux en équipe.
**Lecture non recommandée en dehors du suivi de projet.**

27/09 : formation du groupe 4 composé de Nhung Tran, Artur Abgarov, Valentin Lopez. Choix de la série : Friends (tiré au hasard). Recherche de sites sources (Wikipedia, Google, Allocine, Annuseries, Senscritique, fanfr).

30/09 : Création d'un MCD.

03/10 : Sauvetage de Valentin qui fait un malaise.

03/10 : Sauvetage de Valentin-Jo qui fait un malaise, il est tombé comme un caca. Heureusement il est encore vivant.

07/10 : Validation du MCD.

15/11 : Partage du travail : Artur : 1 ; Nhung : 2 ; Jo : 3
![image](https://github.com/user-attachments/assets/2ae1cf6b-fa5c-430d-8c04-13de79e1c5e0)

22/11 : Création de codes python permettant de récupérer nos données sur des sites internet.

29/11 : Amélioration des codes python permettant de récupérer nos données sur des sites internet. (Jo)
Création un table des acteurs principaux, ainsi que leurs rôles, leurs dates de naissance. Scrapp from wikipédia (Nhung)

19/12 : Création de notre database sur PgAdmin.
![image](https://github.com/user-attachments/assets/a870845b-c4b3-415c-9bfb-39f89ee9e39f)

https://lesvoyageurscinephiles.com/quels-sont-les-lieux-de-tournage-de-friends-que-lon-peut-visiter/

15/01 : Alimentation des données dans la base de données sur la base Postgre de l'école
    database="2025_SAE_Nhung_Jo_Artur",
    
15/01 : Exécution une requête pour répondre à la question: Chandler a eu combien de petites amies? Résultat: 12
  SELECT COUNT (DISTINCT lier.id_personnage)
		FROM relation
		INNER JOIN lier
		ON lier.id_relation = relation.id_relation
		INNER JOIN personnage
		ON lier.id_personnage_1 = personnage.id_personnage
		WHERE nom_personnage = 'Bing'
		AND type_relation = 'Petit%20Ami'
  
![image](https://github.com/user-attachments/assets/fbb27713-5e61-4c4d-adcd-0ba8b5de3cfd)

![image](https://github.com/user-attachments/assets/889e2052-c68a-4982-a299-469e6a72771d)

