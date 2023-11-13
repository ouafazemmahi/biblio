from flask import Flask, render_template, request, session
from flask_session import Session
from Data.database import database

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
db = database("database.db")

class Admin:

    def __init__(self, app):
        self.app = app
        self.setup_routes()

    @staticmethod
    @app.route('/admin', methods=['GET'])
    def admin_home():
        return render_template('admin.html')

    @staticmethod
    @app.route('/admin/ajouter_livre', methods=['GET', 'POST'])
    def ajouter_livre():
        if request.method == 'POST':
        # Récupérer les données du formulaire
            ISBN = request.form.get('ISBN')
            titre = request.form.get('titre')
            auteur = request.form.get('auteur')
            éditeur = request.form.get('éditeur')
            Nb_exemplaire = int(request.form.get('Nb_exemplaire_copies'))  # type: ignore # Updated to match the input name
        
            disponibilite = "Disponible" if Nb_exemplaire > 0 else "Indisponible"

        # Vérifier si le livre existe déjà
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Livres WHERE ISBN = ? AND auteur = ?', (ISBN, auteur))
            existing_book = cursor.fetchone()

            if existing_book:
            # Le livre existe déjà, augmentez Nb_exemplaire
                if existing_book[4]:
                    new_nb_exemplaire = existing_book[4] + int(Nb_exemplaire)  # assuming index 5 is Nb_exemplaire
                    cursor.execute('UPDATE Livres SET Nb_exemplaire = ? WHERE ISBN = ? AND auteur = ?', (new_nb_exemplaire, ISBN, auteur))
                    conn.commit()
                    msg = f'Le livre existe déjà. Nb_exemplaire augmenté à {new_nb_exemplaire}.'
                else:
                    msg = 'Le livre existe déjà, mais Nb_exemplaire n\'est pas un nombre valide.'
        
            else:
            # Ajouter le livre à la base de données
                query = 'INSERT INTO Livres (ISBN, titre, auteur, éditeur, Nb_exemplaire, Disponibilité) VALUES (?, ?, ?, ?, ?, ?);'
                cursor.execute(query, (ISBN, titre, auteur, éditeur, Nb_exemplaire, disponibilite))
                conn.commit()
                msg = 'Le livre a été ajouté avec succès.'

            cursor.close()
            conn.close()

            return render_template('admin.html', msg=msg)
        else:
            return render_template('ajouter_livre.html')

    @staticmethod
    @app.route('/admin/valider_emprunt', methods=['POST']) # type: ignore
    def valider_emprunt():
        if request.method == 'POST':
            # Add logic to handle loan validation
            msg = 'Le prêt a été validé avec succès.'
            return render_template('admin.html', msg=msg)

    @staticmethod
    @app.route('/admin/modifier_livre', methods=['POST']) # type: ignore
    def modifier_livre():
        if request.method == 'POST':
            # Add logic to handle modifying a book
            msg = 'Le livre a été modifié avec succès.'
            return render_template('admin.html', msg=msg)

    @staticmethod
    @app.route('/admin/supprimer_livre', methods=['POST']) # type: ignore
    def supprimer_livre():
        if request.method == 'POST':
            # Add logic to handle deleting a book
            msg = 'Le livre a été supprimé avec succès.'
            return render_template('admin.html', msg=msg)

    def setup_routes(self):
        self.app.add_url_rule('/admin', 'admin_home', self.admin_home)
        self.app.add_url_rule('/admin/ajouter_livre', 'ajouter_livre', self.ajouter_livre, methods=['POST'])
        self.app.add_url_rule('/admin/valider_emprunt', 'valider_emprunt', self.valider_emprunt, methods=['POST'])
        self.app.add_url_rule('/admin/modifier_livre', 'modifier_livre', self.modifier_livre, methods=['POST'])
        self.app.add_url_rule('/admin/supprimer_livre', 'supprimer_livre', self.supprimer_livre, methods=['POST'])


if __name__ == '__main__':
    admin_instance = Admin(app)
    app.run(debug=True)



'''

from flask import Flask, render_template, request, redirect, sessions, url_for, session
from Data.database import database
from flask_session import Session
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Vous pouvez utiliser d'autres options de stockage de session
Session(app)  
db = database("database.db")
class Admin:
   
    @staticmethod
    @app.route('admin/ajouter_livre', methods=['GET', 'POST'])
    def ajouter_livre():
        if request.method == 'POST':
        # Récupérer les données du formulaire
            ISBN = request.form.get('ISBN')
            titre = request.form.get('titre')
            auteur = request.form.get('auteur')
            éditeur = request.form.get('éditeur')
            Nb_exemplaire = int(request.form.get('Nb_exemplaire_copies'))  # type: ignore # Updated to match the input name
        
            disponibilite = "Disponible" if Nb_exemplaire > 0 else "Indisponible"

        # Vérifier si le livre existe déjà
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Livres WHERE ISBN = ? AND auteur = ?', (ISBN, auteur))
            existing_book = cursor.fetchone()

            if existing_book:
            # Le livre existe déjà, augmentez Nb_exemplaire
                if existing_book[4]:
                    new_nb_exemplaire = existing_book[4] + int(Nb_exemplaire)  # assuming index 5 is Nb_exemplaire
                    cursor.execute('UPDATE Livres SET Nb_exemplaire = ? WHERE ISBN = ? AND auteur = ?', (new_nb_exemplaire, ISBN, auteur))
                    conn.commit()
                    msg = f'Le livre existe déjà. Nb_exemplaire augmenté à {new_nb_exemplaire}.'
                else:
                    msg = 'Le livre existe déjà, mais Nb_exemplaire n\'est pas un nombre valide.'
        
            else:
            # Ajouter le livre à la base de données
                query = 'INSERT INTO Livres (ISBN, titre, auteur, éditeur, Nb_exemplaire, Disponibilité) VALUES (?, ?, ?, ?, ?, ?);'
                cursor.execute(query, (ISBN, titre, auteur, éditeur, Nb_exemplaire, disponibilite))
                conn.commit()
                msg = 'Le livre a été ajouté avec succès.'

            cursor.close()
            conn.close()

            return render_template('admin.html', msg=msg)
        else:
            return render_template('ajouter_livre.html')


    # Ajoutez d'autres méthodes pour gérer les fonctionnalités d'administration

# Assurez-vous d'ajouter les routes dans votre fichier principal (app.py par exemple)
'''