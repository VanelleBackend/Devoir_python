# GraphiStudio — Gestion des Commandes Clients

Application de bureau développée en Python avec Tkinter permettant la gestion complète des clients et de leurs commandes pour une agence d'infographie.

---

## 🚀 Fonctionnalités

### 👤 Gestion des clients
- Ajouter un client
- Modifier un client
- Supprimer un client
- Afficher la liste des clients
- Recherche de clients

### 📦 Gestion des commandes
- Ajouter une commande
- Modifier une commande
- Supprimer une commande
- Suivi du statut (En cours, Terminé, En attente)
- Association client → commande

### 💰 Système de prix automatique
- Prix automatiquement assigné selon le service choisi
- Services disponibles :
  - Logo
  - Flyer
  - Affiche publicitaire
  - Carte de visite
  - Site Web
  - E-commerce
  - UI/UX Design
  - Banderole
  - Réseaux sociaux
  - Montage vidéo

### 📄 Génération de factures
- Génération automatique de factures PDF
- Export des données de commande
- Nom du fichier : `facture_<id_commande>.pdf`

---

## 🧰 Technologies utilisées

- Python 3.12.3
- Tkinter (interface graphique)
- ttk (Treeview, Notebook)
- ReportLab (génération PDF)
- Fichiers texte (.txt) pour stockage

---

## 📁 Structure du projet

```
GraphiStudio/
│
├──__pycache__ /
├── main.py 
├── affichage.py 
├── exportation.py 
├── clients.txt 
├── commandes.txt 
└── README.md
```

---

## ⚙️ Installation

```bash
python -m venv venv
source venv/bin/activate
pip install reportlab
```

---

## 🚀 Lancement de l'application

```bash
python main.py
```

---

## 🤝 Contributeurs

    🙋‍♀️ Auteur : Pouakam Koungmo Brele Vanelle
