# Pour installer le venv, c'est simple : 


## Installer le package env sur python
```cmd
pip install env
```

## Ensuite, créer un venv
### Ici, on va l'installer dans le fichier "Code", qui est le fichier dédié au dev. On va nommer notre env "SAE_venv"

On oublie pas de se mettre dans le bon répertoire de fichier dans son terminal
```
cd Code
```
puis on crée l'environnement de dev
```
python3 -m venv SAE_venv
```

## Quand l'environnement est crée, il faut l'exécuter !

Pour une architecture POSIX (Linux, Apple etc...) :
```
source SAE_venv/bin/activate
```

#### Pour une architecture Windows : 
Dans un terminal :
```
SAE_venv\Scripts\activate.bat
```
Dans un terminal PowerShell :
```
SAE_venv\Scripts\activate.ps1
```

## Maintenant, on va installer les mêmes packages pour tout le monde, pour assurer le bon fonctionnement du projet, et que tout le monde ait les mêmes dépendances de packages :

```
pip install -r '<Chemin/Au/Fichier/requirements.txt>'
```

# C'est tout bon ! Vous pouvez utiliser l'app !

## Mais comment désactiver le venv ?
Il faut exécuter cette ligne dans le terminal
```
deactivate
```