# src/processing/partition_data.py
# Partitionnement des données par année

import pandas as pd
import os
import re

print("="*50)
print("PARTITIONNEMENT DES DONNÉES")
print("="*50)

# 1. Charger les données
print("\n📂 Chargement des données...")
movies = pd.read_csv('data/processed/movies_enriched.csv')
print(f"   {len(movies)} films chargés")
print(f"   Colonnes disponibles: {movies.columns.tolist()}")

# 2. Extraire l'année depuis year_str (format "1995" ou "1995s")
print("\n📅 Extraction des années...")

def extract_year_from_str(year_str):
    """Extrait l'année depuis une chaîne comme '1995' ou '1995s'"""
    if pd.isna(year_str):
        return 0
    match = re.search(r'(\d{4})', str(year_str))
    return int(match.group(1)) if match else 0

movies['year'] = movies['year_str'].apply(extract_year_from_str)

films_avec_annee = movies[movies['year'] > 0].shape[0]
print(f"   {films_avec_annee} films ont une année valide")

# 3. Créer les partitions
print("\n✂️ Création des partitions...")

movies_before_2000 = movies[movies['year'] < 2000]
movies_2000_2010 = movies[(movies['year'] >= 2000) & (movies['year'] < 2010)]
movies_after_2010 = movies[movies['year'] >= 2010]
movies_no_year = movies[movies['year'] == 0]

# 4. Créer le dossier de destination
os.makedirs('data/partitioned', exist_ok=True)

# 5. Sauvegarder
movies_before_2000.to_csv('data/partitioned/movies_before_2000.csv', index=False)
movies_2000_2010.to_csv('data/partitioned/movies_2000_2010.csv', index=False)
movies_after_2010.to_csv('data/partitioned/movies_after_2010.csv', index=False)
movies_no_year.to_csv('data/partitioned/movies_no_year.csv', index=False)

# 6. Afficher les résultats
print("\n📊 RÉSULTATS:")
print(f"   Avant 2000: {len(movies_before_2000)} films")
print(f"   2000-2010: {len(movies_2000_2010)} films")
print(f"   Après 2010: {len(movies_after_2010)} films")
print(f"   Sans année: {len(movies_no_year)} films")
print(f"   Total: {len(movies)} films")

print("\n✅ Partitionnement terminé!")
print("   Fichiers sauvegardés dans data/partitioned/")