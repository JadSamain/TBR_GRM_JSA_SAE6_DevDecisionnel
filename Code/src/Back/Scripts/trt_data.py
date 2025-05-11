import glob
import os
import pandas as pd
import openpyxl
from datetime import datetime
import chardet
from unzip_files import unzip_files
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

def extract_from_csv(file_to_process):
    """Extrait les données d'un fichier CSV avec détection automatique de l'encodage."""
    encoding = detect_encoding(file_to_process)
    print(f"[CSV] Encoding détecté pour {file_to_process}: {encoding}")
    try:
        df = pd.read_csv(file_to_process, encoding=encoding, sep=';', low_memory=False)
    except Exception as e:
        print(f"Erreur lecture CSV {file_to_process}: {e}")
        return pd.DataFrame()
    return df

def extract_from_xlsx(file_to_process):
    """Extrait les données d'un fichier Excel."""
    try:
        df = pd.read_excel(file_to_process, engine='openpyxl')
    except Exception as e:
        print(f"Erreur lecture Excel {file_to_process}: {e}")
        return pd.DataFrame()
    return df

def extract_all_data():
    """Parcourt récursivement le dossier source, lit tous les fichiers CSV/XLSX et les combine."""
    dataframes = []
    nb_csv = nb_excel = 0

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.csv'):
                print(f"Traitement CSV : {file_path}")
                df = extract_from_csv(file_path)
                if not df.empty:
                    dataframes.append(df)
                    nb_csv += 1

            elif file.lower().endswith('.xlsx') and not file.startswith('~$'):
                print(f"Traitement Excel : {file_path}")
                df = extract_from_xlsx(file_path)
                if not df.empty:
                    dataframes.append(df)
                    nb_excel += 1

    print(f"\nFichiers CSV traités : {nb_csv}")
    print(f"Fichiers Excel traités : {nb_excel}")

    if dataframes:
        df_all = pd.concat(dataframes, ignore_index=True)

        # Nettoyage des noms de colonnes
        df_all.columns = (
            df_all.columns
            .str.normalize('NFKD')
            .str.encode('ascii', 'ignore')
            .str.decode('utf-8')
            .str.strip()
        )

        df_all = df_all.loc[:, ~df_all.columns.duplicated()]
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
