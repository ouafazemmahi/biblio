from flask import Flask, flash, render_template, request, redirect, sessions, url_for, session
from Data.database import database
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)



app.config['SESSION_TYPE'] = 'filesystem'  # Vous pouvez utiliser d'autres options de stockage de session
Session(app)  
db = database("database.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        Nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        userName = request.form.get("userName")
        mdp = request.form.get("mdp")
        # Hachez le mot de passe avant de le stocker
        mdp_hache = generate_password_hash(mdp) # type: ignore

        conn = db.get_connection()
        cursor = conn.cursor()

        # Vérifiez si le nom d'utilisateur existe déjà
        cursor.execute('SELECT id FROM Utilisateurs WHERE userName = ?', (userName,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Le nom d'utilisateur existe déjà, affichez un message d'erreur
            msg = 'Le nom d\'utilisateur existe déjà.'
            return render_template("inscription.html", msg=msg)
        else:
            # Le nom d'utilisateur n'existe pas, ajoutez l'utilisateur à la base de données
            query = "INSERT INTO Utilisateurs (Nom, Prenom, userName, mdp) VALUES (?, ?, ?, ?);"
            cursor.execute(query, (Nom, prenom, userName, mdp_hache))
            conn.commit()
            cursor.close()
            return redirect(url_for("login"))
    else:
        msg = ''  # Message vide si ce n'est pas une soumission POST

    return render_template("inscription.html", msg=msg)

@app.route('/connecter', methods=['GET', 'POST']) # type: ignore
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'mdp' in request.form:
        # Create variables for easy access
        username = request.form.get("username")
        password = request.form.get("mdp")
        # Check if account exists using MySQL
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, userName, mdp FROM Utilisateurs WHERE userName = ?', (username,))
        account = cursor.fetchone()

        if account and check_password_hash(account[2], password): # type: ignore
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            if account[1] == 'admin' and check_password_hash(account[2], '123456789'):
                session['is_admin'] = True
                return redirect(url_for('admin'))
            return redirect(url_for('profil'))
        else:
            msg = 'Incorrect username or password.'
    return render_template('connecter.html', msg=msg)

    

@app.route('/admin')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('is_admin', None)  # Remove 'is_admin' from the session
    # Redirect to login page
    return render_template('admin.html')


@app.route('/profil')
def profil():
    if 'loggedin' in session:
        # Si l'utilisateur est connecté, affichez le contenu de la page de profil
        return render_template('profil.html')
    else:
        # Si l'utilisateur n'est pas connecté, redirigez-le vers la page de connexion
        return redirect(url_for('login'))
    
@app.route('/admin')
def admin():
    if 'loggedin' in session :
        if session.get('is_admin'):
        # If the user is logged in and is an admin, render the admin template
            return render_template('admin.html')
        else:
            return "User is not an admin"
        # If the user is not an admin, redirect to the login page
    else:
        return redirect(url_for('login'))
    
@app.route('/liste_livres')
def liste_livres():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Livres')
    livres = cursor.fetchall()
    conn.close()
    return render_template('liste_livres.html', livres=livres)


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
            return render_template('admin.html')

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
            # Retrieve the book details from the form
            ISBN = request.form.get('ISBN')
            new_title = request.form.get('new_title')
            new_author = request.form.get('new_author')
            new_publisher = request.form.get('new_publisher')

            # Update the book in the database
            conn = db.get_connection()
            cursor = conn.cursor()

            # Assuming ISBN is the primary key
            cursor.execute('UPDATE Livres SET titre = ?, auteur = ?, éditeur = ? WHERE ISBN = ?', (new_title, new_author, new_publisher, ISBN))
            conn.commit()

            cursor.close()
            conn.close()

            msg = 'Le livre a été modifié avec succès.'
            flash(msg)
            return render_template('admin.html')

    @staticmethod
    @app.route('/admin/supprimer_livre', methods=['POST']) # type: ignore
    def supprimer_livre():
        if request.method == 'POST':
            # Retrieve the book details from the form
            ISBN = request.form.get('ISBN')

            # Delete the book from the database
            conn = db.get_connection()
            cursor = conn.cursor()

            # Assuming ISBN is the primary key
            cursor.execute('DELETE FROM Livres WHERE ISBN = ?', (ISBN,))
            conn.commit()

            cursor.close()
            conn.close()

            msg = 'Le livre a été supprimé avec succès.'
            flash(msg)
            return render_template('admin.html')

    def setup_routes(self):
        self.app.add_url_rule('/admin', 'admin_home', self.admin_home)
        self.app.add_url_rule('/admin/ajouter_livre', 'ajouter_livre', self.ajouter_livre, methods=['POST'])
        self.app.add_url_rule('/admin/valider_emprunt', 'valider_emprunt', self.valider_emprunt, methods=['POST'])
        self.app.add_url_rule('/admin/modifier_livre', 'modifier_livre', self.modifier_livre, methods=['POST'])
        self.app.add_url_rule('/admin/supprimer_livre', 'supprimer_livre', self.supprimer_livre, methods=['POST'])



'''@app.route('/ajouter_livre', methods=['GET', 'POST'])
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
        return render_template('ajouter_livre.html')'''

"""else:
    print("User is not an admin")
    return redirect(url_for('login'))"""


if __name__ == "__main__":
    app.run()

"""

from flask import Flask, render_template, request, redirect, url_for, session
from Data.database import database
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
db = database("database.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        Nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        userName = request.form.get("userName")
        mdp = request.form.get("mdp")
        conn = db.get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Utilisateurs (Nom, Prenom, userName, mdp) VALUES (?, ?, ?, ?);"
        cursor.execute(query, (Nom, prenom, userName, mdp))
        cursor.close()
        conn.commit()
        return redirect(url_for("index"))
    return render_template("inscription.html")


@app.route('/connecter/', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'mdp' in request.form:
        # Create variables for easy access
        username = request.form.get("userName")
        password = request.form.get("mdp")
        # Check if account exists using MySQL
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Utilisateurs WHERE userName = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            if check_password_hash(account['password'], password): # type: ignore
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                return 'Logged in successfully!'
            else:
                msg = 'Incorrect password!'
        else:
            msg = 'Account does not exist.'

    return render_template('profil.html', msg=msg)

if __name__ == "__main__":
    app.run()
"""