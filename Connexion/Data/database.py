"""import os
import sqlite3

class database():
    def __init__(self,database_name : str):
        self.connection = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.connection.row_factory = sqlite3.Row

    def creerUtilisteurs(self, Nom : str, prenom : str, userName: str, mdp : str):
        cursor = self.connection.cursor()
        query =f"INSERT INTO Utilisateurs (Nom, Prenom, userName, mdp) VALUES ('{Nom}', '{prenom}', '{userName}', '{mdp}');"
        cursor.execute(query)
        cursor.close()
        self.connection.commit()"""
import os
import sqlite3
import threading

class database:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.connection = threading.local()

    def get_connection(self):
        if not hasattr(self.connection, "conn"):
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.database_name)
            self.connection.conn = sqlite3.connect(db_path)
            self.connection.conn.row_factory = sqlite3.Row
        return self.connection.conn

    def creer_utilisateurs(self, nom: str, prenom: str, username: str, mdp: str):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            query = "INSERT INTO Utilisateurs (Nom, Prenom, userName, mdp) VALUES (?, ?, ?, ?);"
            cursor.execute(query, (nom, prenom, username, mdp))
        finally:
            conn.commit()
            
    def ajouter_livre(self, ISBN, titre, auteur, éditeur, Nb_exemplaire, Disponibilité):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Livres (ISBN, titre, auteur, éditeur, Nb_exemplaire, Disponibilité) VALUES (?, ?, ?, ?, ?, ?)',
                           (ISBN, titre, auteur, éditeur, Nb_exemplaire, Disponibilité))
        finally:
            conn.commit()
