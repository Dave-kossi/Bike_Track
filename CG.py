import streamlit as st
import requests
import pandas as pd
import numpy as np
import os
from datetime import datetime
import time

# --- CONFIGURATION ---
DATA_FILE = "dataset_complet_mulhouse.csv"

def get_status_label(rate):
    if rate <= 0.15: return "🔴 URGENCE"
    if rate <= 0.35: return "🟠 TENSION"
    return "🟢 OK"

def capture_globale():
    """Capture 100% des stations de l'agglomération instantanément"""
    try:
        # 1. Appel synchrone des deux flux API
        base_url = "https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_af/fr"
        
        resp_info = requests.get(f"{base_url}/station_information.json", timeout=10).json()
        resp_status = requests.get(f"{base_url}/station_status.json", timeout=10).json()
        
        df_info = pd.DataFrame(resp_info['data']['stations'])[['station_id', 'name', 'capacity']]
        df_status = pd.DataFrame(resp_status['data']['stations'])[['station_id', 'num_bikes_available']]
        
        # 2. Fusion instantanée
        df = pd.merge(df_info, df_status, on="station_id")
        
        # 3. Calculs et formatage temporel
        maintenant = datetime.now()
        df['taux_reel'] = (df['num_bikes_available'] / df['capacity']).replace([np.inf, -np.inf], 0).fillna(0)
        df['score_tension'] = ((1 - df['taux_reel']) * 100).round(1)
        df['etat_label'] = df['taux_reel'].apply(get_status_label)
        
        # AJOUT DES COLONNES DEMANDÉES
        df['timestamp'] = maintenant.strftime("%Y-%m-%d %H:%M:%S")
        df['date'] = maintenant.strftime("%Y-%m-%d")
        df['heure'] = maintenant.strftime("%H:%M:%S")

        # Tri par urgence
        df = df.sort_values(by='taux_reel', ascending=True)

        # 4. Sauvegarde sur disque local (format tabulation pour la clarté)
        header = not os.path.exists(DATA_FILE)
        df.to_csv(DATA_FILE, mode='a', index=True, header=header, sep="\t", encoding='utf-8-sig')
        
        return df
    except Exception as e:
        st.error(f"Erreur lors de la capture : {e}")
        return None

# --- INTERFACE DE SUPERVISION ---
st.set_page_config(page_title="Collecteur Global Mulhouse", layout="wide")

st.title("📊 Capture Instantanée & Archivage ML")
st.write("Ce module enregistre l'état complet du réseau avec horodatage précis pour l'analyse prédictive.")

if st.button("📸 Lancer une capture de TOUTES les stations"):
    data = capture_globale()
    if data is not None:
        st.success(f"Succès ! {len(data)} stations enregistrées à {datetime.now().strftime('%H:%M:%S')}")
        
        # Affichage du rendu final structuré incluant Date et Heure
        st.subheader("Aperçu du bloc de données capturé :")
        colonnes_affichage = [
            'date', 'heure', 'station_id', 'name', 
            'num_bikes_available', 'capacity', 'taux_reel', 'score_tension', 'etat_label'
        ]
        st.code(data[colonnes_affichage].to_string(index=False), language="text")

st.divider()

# --- ANALYSE DU STOCKAGE ---
if os.path.exists(DATA_FILE):
    # Remplacez votre ligne 78 par celle-ci :
    full_db = pd.read_csv(DATA_FILE, sep="\t", on_bad_lines='skip')
    nb_captures = full_db['timestamp'].nunique()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total lignes en base", len(full_db))
    c2.metric("Nombre de captures (sessions)", nb_captures)
    c3.metric("Fichier de stockage", DATA_FILE)

    st.subheader("📥 Télécharger le Dataset Historique")
    st.write("Utilisez ce fichier pour entraîner votre modèle de Machine Learning.")
    with open(DATA_FILE, "rb") as f:
        st.download_button(
            label="💾 Télécharger le fichier .CSV",
            data=f,
            file_name=f"dataset_mulhouse_velo_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
else:
    st.info("Le fichier local est vide. Lancez une première capture pour initialiser la base.")