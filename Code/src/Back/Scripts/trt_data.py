import glob
import pandas as pd
from datetime import datetime
import chardet

def detect_encoding(file_path):
    """Détecte automatiquement l'encodage d'un fichier."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def extract_from_csv(file_to_process):
    """Extrait les données d'un fichier CSV avec détection automatique de l'encodage."""
    encoding = detect_encoding(file_to_process)
    print(f"Encoding detected for {file_to_process}: {encoding}")
    try:
        df = pd.read_csv(file_to_process, encoding=encoding, sep=';', low_memory=False)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV {file_to_process}: {e}")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur
    return df

def extract_from_xlsx(file_to_process):
    """Extrait les données d'un fichier Excel."""
    try:
        df = pd.read_excel(file_to_process, engine='openpyxl')
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier Excel {file_to_process}: {e}")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur
    return df

def extract():
    """Extrait et combine les données de tous les fichiers CSV et Excel."""
    nb_csv = 0
    nb_excel = 0
    dataframes = []

    # Traitement des fichiers CSV
    for csv_file in glob.glob("Data_SOURCE/*.csv"):
        print(f"Processing CSV: {csv_file}")
        df = extract_from_csv(csv_file)
        if not df.empty:
            dataframes.append(df)
            nb_csv += 1

    # Traitement des fichiers Excel
    for xlsx_file in glob.glob("Data_SOURCE/*.xlsx"):
        if not xlsx_file.startswith("~$"):  # Ignore les fichiers temporaires
            print(f"Processing Excel: {xlsx_file}")
            df = extract_from_xlsx(xlsx_file)
            if not df.empty:
                dataframes.append(df)
                nb_excel += 1

    print("Number of CSV files processed: ", nb_csv)
    print("Number of Excel files processed: ", nb_excel)

    # Combine tous les DataFrames
    if dataframes:
        df = pd.concat(dataframes, ignore_index=True)

        # Normalise les noms de colonnes pour éviter les doublons dus aux encodages différents
        df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', 'ignore').str.decode('utf-8').str.strip()

        # Supprime les colonnes en double (même après normalisation)
        df = df.loc[:, ~df.columns.duplicated()]
    else:
        print("Aucun fichier valide trouvé.")
        df = pd.DataFrame()  # Retourne un DataFrame vide si aucun fichier n'a été traité

    return df

def export_csv(df):
    """Exporte le DataFrame combiné en un fichier CSV."""
    if df.empty:
        print("Aucune donnée à exporter.")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"Data_OUTPUT/combined_data_{timestamp}.csv"
    df.to_csv(file_name, sep=';', index=False, encoding='utf-8-sig')
    print(f"Exported to {file_name}")

# Exécution du script
df = extract()
export_csv(df)
