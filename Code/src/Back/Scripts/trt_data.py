import glob
import os
import pandas as pd
import openpyxl
from datetime import datetime
import chardet 
import unicodedata
from unzip_files import unzip_files
from fuzzywuzzy import fuzz

# Dézippe les fichiers avant de les traiter
unzip_files()
# Chemins des dossiers


SOURCE_DIR = r"Data/Data_brute"
OUTPUT_DIR = r"Data/Data_traitee"

def clean_output_directory(path):
    """Vide le dossier de sortie sans le supprimer."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Dossier créé : {path}")
    else:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Impossible de supprimer {file_path}. Raison : {e}")
        print(f"Dossier vidé : {path}")


def detect_encoding(file_path):
    """Détecte automatiquement l'encodage d'un fichier."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def extract_from_csv(file_to_process, force_utf8=False):
    """Extrait les données d'un fichier CSV avec détection automatique ou encodage forcé."""
    encoding = 'utf-8' if force_utf8 else detect_encoding(file_to_process)
    print(f"[CSV] Encoding {'forcé à utf-8' if force_utf8 else 'détecté'} pour {file_to_process}: {encoding}")
    try:
        with open(file_to_process, 'r', encoding=encoding) as f:
            first_line = f.readline()
            if ';' in first_line:
                sep = ';'
            elif ',' in first_line:
                sep = ','
            elif '\t' in first_line:
                sep = '\t'
            else:
                sep = None
        df = pd.read_csv(file_to_process, encoding=encoding, sep=sep, engine='python', low_memory=False, skiprows=1)
    except Exception as e:
        print(f"Erreur lecture CSV {file_to_process}: {e}")
        return pd.DataFrame()
    return df


def extract_from_xlsx(file_to_process):
    """Extrait les données d'un fichier Excel."""
    try:
        df = pd.read_excel(file_to_process, engine='openpyxl', skiprows=1)
    except Exception as e:
        print(f"Erreur lecture Excel {file_to_process}: {e}")
        return pd.DataFrame()
    return df

def merge_similar_columns(df, threshold=90):
    """Fusionne les colonnes similaires selon un seuil de similarité."""
    cols = list(df.columns)
    merged = set()
    for i, col1 in enumerate(cols):
        if col1 not in df.columns:
            continue  # La colonne a déjà été supprimée
        for col2 in cols[i+1:]:
            if col2 not in df.columns or col2 in merged:
                continue
            if fuzz.ratio(col1, col2) > threshold:
                df[col1] = df[col1].combine_first(df[col2])
                df.drop(columns=[col2], inplace=True)
                merged.add(col2)
    return df

def clean_column_name(column_name):
    """Nettoie et normalise un nom de colonne."""
    if not isinstance(column_name, str):
        return str(column_name)
    
    # Normalisation Unicode (décompose les caractères accentués)
    cleaned = unicodedata.normalize('NFKD', column_name)
    # Encode en ASCII en ignorant les caractères non-ASCII
    cleaned = cleaned.encode('ASCII', 'ignore').decode('ASCII')
    # Supprime les espaces en début et fin
    cleaned = cleaned.strip()
    # Remplace les espaces multiples par un seul espace
    cleaned = ' '.join(cleaned.split())
    # Convertit en minuscules pour uniformiser
    cleaned = cleaned.lower()
    # Remplace les caractères spéciaux par des underscores
    cleaned = ''.join(c if c.isalnum() or c.isspace() else '_' for c in cleaned)
    # Remplace les espaces par des underscores
    cleaned = cleaned.replace(' ', '_')
    # Supprime les underscores multiples
    cleaned = '_'.join(filter(None, cleaned.split('_')))
    return cleaned



def extract_all_data():
    """Parcourt récursivement le dossier source, lit tous les fichiers CSV/XLSX et les combine."""
    dataframes = []
    nb_csv = nb_excel = 0

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.csv'):
                print(f"Traitement CSV : {file_path}")
                force_utf8 = "electricite" in file.lower()
                df = extract_from_csv(file_path, force_utf8=force_utf8)

                if not df.empty:
                    # Nettoyage des noms de colonnes pour chaque DataFrame
                    df.columns = [clean_column_name(col) for col in df.columns]
                    dataframes.append(df)
                    nb_csv += 1

            elif file.lower().endswith('.xlsx') and not file.startswith('~$'):
                print(f"Traitement Excel : {file_path}")
                df = extract_from_xlsx(file_path)
                if not df.empty:
                    # Nettoyage des noms de colonnes pour chaque DataFrame
                    df.columns = [clean_column_name(col) for col in df.columns]
                    dataframes.append(df)
                    nb_excel += 1

    print(f"\nFichiers CSV traités : {nb_csv}")
    print(f"Fichiers Excel traités : {nb_excel}")

    if dataframes:
        df_all = pd.concat(dataframes, ignore_index=True)
        
        # Vérification des colonnes dupliquées
        duplicate_cols = df_all.columns[df_all.columns.duplicated()].tolist()
        if duplicate_cols:
            print("\nColonnes dupliquées détectées avant nettoyage :")
            for col in duplicate_cols:
                print(f"- {col}")
        
        # Suppression des colonnes dupliquées après la concaténation
        df_all = df_all.loc[:, ~df_all.columns.duplicated()]
        
        # Fusion des colonnes similaires après nettoyage
        df_all = merge_similar_columns(df_all)
        
        # Vérification finale
        if df_all.columns.duplicated().any():
            print("\nATTENTION : Il reste encore des colonnes dupliquées après nettoyage !")
            print("Colonnes restantes :", df_all.columns.tolist())
        else:
            print("\nToutes les colonnes dupliquées ont été supprimées avec succès.")
            print("Colonnes finales :", df_all.columns.tolist())
            
        return df_all
    else:
        print("Aucun fichier valide trouvé.")
        return pd.DataFrame()

def export_combined_csv(df):
    """Vide le dossier de sortie et exporte le DataFrame final dans un fichier CSV unique."""
    if df.empty:
        print("Aucune donnée à exporter.")
        return

    clean_output_directory(OUTPUT_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"combined_data_{timestamp}.csv")
    df.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')
    print(f"\n✅ Fichier exporté : {output_path}")

# === Exécution principale ===
if __name__ == "__main__":
    df_result = extract_all_data()
    export_combined_csv(df_result)
