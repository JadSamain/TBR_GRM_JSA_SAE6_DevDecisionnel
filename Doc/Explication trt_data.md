# 🛠️ Documentation des modifications du script `trt_data.py`

Ce document détaille les **transformations apportées** au script `trt_data.py` afin de corriger des problèmes liés à l'encodage des fichiers et à la structure des données en entrée.

---

## ✅ Objectifs

1. **Forcer l'encodage en UTF-8** pour les fichiers CSV contenant le mot-clé `"electricite"` dans leur nom.
2. **Ignorer systématiquement la première ligne** de tous les fichiers d'import (CSV et Excel).

---

## 🔧 Détail des modifications

### 1. Encodage forcé en UTF-8 pour certains fichiers CSV

#### Contexte
Trois fichiers CSV spécifiques avec `"electricite"` dans leur nom présentaient des problèmes de lecture liés à un encodage incorrect.

#### Solution
- Modification de la fonction `extract_from_csv()` pour accepter un nouveau paramètre `force_utf8`.
- Lors de la lecture des fichiers, une vérification est faite sur le nom du fichier :
  ```python
  force_utf8 = "electricite" in file.lower()
  df = extract_from_csv(file_path, force_utf8=force_utf8)
  ```
- Si le nom contient `"electricite"`, l'encodage est **forcé à `'utf-8'`**.

#### Impact
Les fichiers problématiques sont désormais correctement lus sans erreurs d'encodage.

---

### 2. Ignorer la première ligne de tous les fichiers d'import

#### Contexte
Certains fichiers comportent une première ligne contenant des métadonnées ou des titres non pertinents. Cela peut interférer avec l'analyse des données.

#### Solution
- Ajout du paramètre `skiprows=1` dans :
  - `pd.read_csv()` pour les fichiers CSV
  - `pd.read_excel()` pour les fichiers Excel
- Appliqué de manière **systématique à tous les fichiers** importés.

#### Extrait de code
```python
df = pd.read_csv(file_to_process, encoding=encoding, sep=sep, skiprows=1, engine='python', low_memory=False)
df = pd.read_excel(file_to_process, engine='openpyxl', skiprows=1)
```

---

## 📊 Résumé technique

| Type de fichier     | Encodage              | Première ligne ignorée | Conditions supplémentaires                        |
|---------------------|-----------------------|-------------------------|---------------------------------------------------|
| CSV (général)       | Auto-détection (chardet) | ✅                      | -                                                 |
| CSV avec "electricite" | **Forcé à UTF-8**        | ✅                      | Nom du fichier contient "electricite" (insensible à la casse) |
| Excel (`.xlsx`)     | Géré par `openpyxl`   | ✅                      | Fichiers temporaires exclus (ceux commençant par `~$`)        |

---

## 📁 Emplacements importants

- **SOURCE_DIR** : `Data/Data_brute` (répertoire contenant les fichiers à traiter)
- **OUTPUT_DIR** : `Data/Data_traitee` (répertoire où est exporté le CSV final)

---

## 🧪 Tests recommandés

- Vérifier que les fichiers `"electricite"` sont bien lus sans erreur.
- S'assurer que les premières lignes ne sont jamais présentes dans les données importées.
- Contrôler que le nettoyage des colonnes fonctionne toujours correctement après modifications.
- Confirmer que l’export final contient toutes les données fusionnées et nettoyées.

---

## 🗓️ Historique

- **2025-05-23** : Implémentation des deux correctifs (encodage + saut première ligne).

---
