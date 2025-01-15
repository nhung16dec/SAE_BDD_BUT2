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

15/01 : Alimentation des données dans la base de données sur Pgadmin
    database="2025_SAE_Nhung_Jo_Artur",
    user="admindbetu",
    host='10.11.159.10',
    password="admindbetu",
    port="5432"
15/01 : Exécution une requête pour répondre à la question: Chandler a eu combien de petites amies? Résultat: 12
  SELECT COUNT (DISTINCT lier.id_personnage)
		FROM relation
		INNER JOIN lier
		ON lier.id_relation = relation.id_relation
		INNER JOIN personnage
		ON lier.id_personnage_1 = personnage.id_personnage
		WHERE nom_personnage = 'Bing'
		AND type_relation = 'Petit%20Ami'
  
