import pandas as pd
import sqlite3
import os
from datetime import datetime

def get_latest_csv():
    """Récupère le dernier fichier CSV généré dans le dossier Data_traitee."""
    data_dir = "Data/Data_traitee"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError("Aucun fichier CSV trouvé dans le dossier Data_traitee")
    
    latest_file = max(csv_files, key=lambda x: os.path.getctime(os.path.join(data_dir, x)))
    return os.path.join(data_dir, latest_file)

def import_data():
    # Connexion à la base de données
    db_path = 'Code/src/Back/db/iris.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Lecture du fichier CSV
        csv_path = get_latest_csv()
        print(f"Lecture du fichier : {csv_path}")
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig', low_memory=False)
        
        # Conversion en minuscules
        df.columns = df.columns.str.lower()
        
        print("\nColonnes disponibles dans le CSV :")
        for col in df.columns:
            print(f"- {col}")
        
        # Table Opérateur
        operateurs = df[["nom de l'operateur", "code eic (energy identification code) de l'operateur"]].drop_duplicates()
        operateurs.columns = ['Lib_operateur', 'Id_operateur']
        operateurs.to_sql('Opérateur', conn, if_exists='append', index=False,
                         dtype={'Id_operateur': 'TEXT', 'Lib_operateur': 'TEXT'})
        print("Données importées dans la table Opérateur")

        # Table Filière
        filieres = df[['filiere']].drop_duplicates()
        filieres['Id_filiere'] = range(1, len(filieres) + 1)  # Génère des IDs uniques
        filieres.columns = ['Nom_filiere', 'Id_filiere']
        filieres.to_sql('Filière', conn, if_exists='append', index=False,
                       dtype={'Id_filiere': 'INTEGER', 'Nom_filiere': 'TEXT'})
        print("Données importées dans la table Filière")

        # Table Annee
        annees = df['millesime des donnees'].unique()
        annees_df = pd.DataFrame(annees, columns=['Annee'])
        annees_df.to_sql('Annee', conn, if_exists='append', index=False)
        print("Données importées dans la table Annee")

        # Table Region (à adapter selon vos données - exemple hypothétique)
        # Nous devrons peut-être extraire cette information d'une autre source
        # Pour l'instant, nous créons une région "par défaut"
        regions_df = pd.DataFrame({
            'Id_reg': ['DEFAULT'],
            'Lib_reg': ['Région par défaut']
        })
        regions_df.to_sql('Region', conn, if_exists='append', index=False)
        print("Données importées dans la table Region")

        # Table Departement (à adapter selon vos données)
        # Pour l'instant, nous créons un département "par défaut"
        dept_df = pd.DataFrame({
            'Id_dept': [1],
            'Lib_dept': ['Département par défaut'],
            'Id_reg': ['DEFAULT']
        })
        dept_df.to_sql('Departement', conn, if_exists='append', index=False)
        print("Données importées dans la table Departement")

        # Table Iris
        iris = df[['code_iris', 'code de l\'iris - libelle de la zone']].drop_duplicates()
        iris['Id_dept'] = 1  # Utilise le département par défaut
        iris['Irisee'] = True
        iris.columns = ['Id_iris', 'Lib_iris', 'Id_dept', 'Irisee']
        iris.to_sql('Iris', conn, if_exists='append', index=False,
                   dtype={'Id_iris': 'TEXT', 'Lib_iris': 'TEXT', 'Irisee': 'BOOLEAN', 'Id_dept': 'INTEGER'})
        print("Données importées dans la table Iris")

        # Création d'un mapping pour les filières
        filiere_mapping = dict(zip(filieres['Nom_filiere'], filieres['Id_filiere']))

        # Table Conso
        conso = df[[
            'millesime des donnees',
            'code_iris',
            'filiere',
            "code eic (energy identification code) de l'operateur",
            'nombre de points de livraison',
            'consommation (en mwh)'
        ]].copy()
        
        # Conversion des types et mapping des clés étrangères
        conso['filiere'] = conso['filiere'].map(filiere_mapping)
        conso.columns = ['Annee', 'Id_iris', 'Id_filiere', 'Id_operateur', 'Nb_pdl', 'Conso']
        
        # Conversion des valeurs numériques
        conso['Conso'] = pd.to_numeric(conso['Conso'], errors='coerce')
        conso['Nb_pdl'] = pd.to_numeric(conso['Nb_pdl'], errors='coerce')
        
        # Suppression des lignes avec des valeurs nulles
        conso = conso.dropna()
        
        conso.to_sql('Conso', conn, if_exists='append', index=False)
        print("Données importées dans la table Conso")

        conn.commit()
        print("\nImportation des données terminée avec succès!")

    except Exception as e:
        print(f"Erreur lors de l'importation des données : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    import_data() 