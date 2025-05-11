import zipfile

def unzip_files():
    zip_file_path = 'Data/Data_brute/Data_Iris.zip'  # Chemin des données zip à décompresser
    extract_to = 'Data/Data_brute' 

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Files extracted to {extract_to}")

# Call the function
unzip_files()
