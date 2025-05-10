# Pour installer le venv, c'est simple : 

## Les prérequis

Pour se soumettre aux besoins spécifiés par la consigne du projet, nous devons vérifier que nous utilisons une version 3.9.X de python :

```cmd 
python3.9 --version
Python 3.9.21
```

## Installer le package env sur python
```cmd
pip3.9 install env
```

## Ensuite, créer un venv
### Ici, on va l'installer dans la racine de notre projet, qui est le dossier dédié au dev. On va nommer notre env ".venv" afin de respecter les habitudes de programmation

On oublie pas de se mettre dans le bon répertoire dans son terminal
```
cd ...\TBR_GRM_JSA_SAE6_DevDecisionnel
```
puis on crée l'environnement de dev
```
python3.9 -m venv .venv
```

## Quand l'environnement est créé, il faut l'exécuter !

#### Pour une architecture POSIX (Linux, Apple etc...) :
```
source .venv/bin/activate
```

#### Pour une architecture Windows : 
Dans un terminal :
```
.venv\Scripts\activate.bat
```
Dans un terminal PowerShell :
```
.venv\Scripts\activate.ps1
```

## Maintenant, on va installer les mêmes packages pour tout le monde, pour assurer le bon fonctionnement du projet, et que tout le monde ait les mêmes dépendances de packages :

```
pip install -r 'Code/src/Back/requirements.txt'
```

# C'est tout bon ! Vous pouvez utiliser l'app !

## Mais comment désactiver le venv ?
Il faut exécuter cette ligne dans le terminal
```
deactivate
```