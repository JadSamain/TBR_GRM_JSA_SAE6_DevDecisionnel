import os
import sqlite3

def create_db():
    # Define the path to the database file
    db_path = 'Code\src\Back\db\iris.sqlite'

    # Create directories if they do not exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        conn = sqlite3.connect(db_path)
        print('Connexion réussie')
    except sqlite3.Error as e:
        print(f'Erreur lors de la connexion à la base de données: {e}')
        return

    cursor = conn.cursor()

    # Liste des commandes SQL pour créer les tables
    create_table_queries = [
        '''
        CREATE TABLE Opérateur(
        Id_operateur INT,
        Lib_operateur VARCHAR(50),
        PRIMARY KEY(Id_operateur)
        )
        ''',
        '''
        CREATE TABLE Filière(
        Id_filiere INT,
        Nom_filiere VARCHAR(50),
        PRIMARY KEY(Id_filiere)
        )
        ''',
        '''
        CREATE TABLE Annee(
        Annee INT,
        PRIMARY KEY(Annee)
        )
        ''',
        '''
        CREATE TABLE Region(
        Id_reg VARCHAR(50),
        Lib_reg VARCHAR(50),
        PRIMARY KEY(Id_reg)
        )
        ''',
        '''
        CREATE TABLE Departement(
        Id_dept INT,
        Lib_dept VARCHAR(50),
        Id_reg VARCHAR(50) NOT NULL,
        PRIMARY KEY(Id_dept),
        FOREIGN KEY(Id_reg) REFERENCES Region(Id_reg)
        )
        ''',
        '''
        CREATE TABLE Iris(
        Id_iris INT,
        Lib_iris VARCHAR(50),
        Irisee LOGICAL,
        Id_dept INT NOT NULL,
        PRIMARY KEY(Id_iris),
        FOREIGN KEY(Id_dept) REFERENCES Departement(Id_dept)
        )
        ''',
        '''
        CREATE TABLE Conso(
        Annee INT,
        Id_iris INT,
        Id_filiere INT,
        Id_operateur INT,
        Nb_pdl INT,
        Conso INT,
        PRIMARY KEY(Annee, Id_iris, Id_filiere, Id_operateur),
        FOREIGN KEY(Annee) REFERENCES Annee(Annee),
        FOREIGN KEY(Id_iris) REFERENCES Iris(Id_iris),
        FOREIGN KEY(Id_filiere) REFERENCES Filière(Id_filiere),
        FOREIGN KEY(Id_operateur) REFERENCES Opérateur(Id_operateur)
        )
        '''
    ]

    # Exécution de chaque commande SQL
    for query in create_table_queries:
        cursor.execute(query)

    conn.commit()
    conn.close()
    print("Tables créées avec succès")

create_db()
