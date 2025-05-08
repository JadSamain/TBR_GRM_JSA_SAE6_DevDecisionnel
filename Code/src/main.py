import os
import sys

# Ajouter src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Front"))

from app import run_app

if __name__ == "__main__":
    run_app()
