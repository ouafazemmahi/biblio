"""from Data.database import database

database = database("database.db")


def sinscrire():
    print("___Inscription__")
    Nom = input('nom : ')
    prenom = input('Prenom : ')
    userName= input('Choisi ton pseudo : ')
    mdp = input('mot de passe: ')

    database.creerUtilisteurs(Nom , prenom, userName, mdp)




def menu_non_connecté():
    while True:
        print("Bienvenue sur le site de la Bibliotèque du Mirail! (vous etes actuellement non connecté)" )
        print("Choisissez une option")
        print("1. Login")
        print("2.s'inscrire")
        choix = int(input())

        if choix == 2:
            sinscrire()
        
menu_non_connecté()"""