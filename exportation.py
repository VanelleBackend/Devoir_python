# Importation de library (Tkinter pour l'interface graphique, datetime pour les dates, os pour la gestion des fichiers)
from tkinter import ttk, messagebox
import datetime, os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Fichier de stockage des clients et commandes
FICHIER_CLIENTS = "clients.txt"
FICHIER_COMMANDES = "commandes.txt"

# Function pour générer un nouvel ID unique pour clients et commandes
def generer_id(fichier):
    lignes = lire_fichier(fichier)
    if not lignes: return 1
    ids = [int(l.split(";")[0]) for l in lignes if l.strip()]
    return max(ids) + 1

# Function d'ajout de clients
def ajouter_client(var_nom, var_tel, tree):
    nom = var_nom.get().strip()
    tel = var_tel.get().strip()
    if not nom or not tel:
        messagebox.showwarning("Champ vide", "Veuillez remplir tous les champs.")
        return
    cid = generer_id(FICHIER_CLIENTS)
    ecrire_ligne(FICHIER_CLIENTS, f"{cid};{nom};{tel}")
    tree.insert("", "end", values=(cid, nom, tel))
    var_nom.set(""); var_tel.set("")
    messagebox.showinfo("Succès", f"Client #{cid} ajouté.")

# Function de modification de clients
def modifier_client(var_nom, var_tel, tree):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un client à modifier.")
        return
    cid = tree.item(sel[0], "values")[0]
    nom = var_nom.get().strip()
    tel = var_tel.get().strip()
    if not nom or not tel:
        messagebox.showwarning("Champ vide", "Remplissez les champs avant de modifier.")
        return
    modifier_ligne(FICHIER_CLIENTS, int(cid), nom, tel)
    tree.item(sel[0], values=(cid, nom, tel))
    messagebox.showinfo("Mis à jour", f"Client #{cid} modifié.")

# Function de suppression de clients
def supprimer_client(tree):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un client à supprimer.")
        return
    cid = tree.item(sel[0], "values")[0]
    if messagebox.askyesno("Confirmer", f"Supprimer le client #{cid} ?"):
        supprimer_ligne(FICHIER_CLIENTS, int(cid))
        tree.delete(sel[0])

# Function de sélection d'un client dans le tableau pour pré-remplir les champs du formulaire
def selectionner_client(tree, var_nom, var_tel):
    sel = tree.selection()
    if sel:
        vals = tree.item(sel[0], "values")
        var_nom.set(vals[1])
        var_tel.set(vals[2])

# Function de recherche de clients par mot-clé (ID, nom ou téléphone)
def rechercher_clients(mot_cle, tree):
    mot_cle = mot_cle.strip().lower()

    # vider le tableau
    for item in tree.get_children():
        tree.delete(item)

    # recharger + filtrer
    for ligne in lire_fichier(FICHIER_CLIENTS):
        p = ligne.split(";")
        if len(p) == 3:
            cid, nom, tel = p

            if (mot_cle in cid.lower()
                or mot_cle in nom.lower()
                or mot_cle in tel):

                tree.insert("", "end", values=(cid, nom, tel))

# Function d'ajout de commandes
def ajouter_commande(var_client_id, var_service,var_prix,var_statut, tree):
    cid     = var_client_id.get().strip()
    service = var_service.get().strip()
    prix    = var_prix.get().strip()
    statut    = var_statut.get().strip()
    if not cid or not service or not prix or not statut:
        messagebox.showwarning("Erreur", "ID client, service et prix sont obligatoires.")
        return
    if not client_existe(int(cid)):
        messagebox.showerror("Client introuvable", f"Aucun client avec l'ID {cid}.")
        return
    num  = generer_id(FICHIER_COMMANDES)
    date = datetime.date.today().isoformat()
    ecrire_ligne(FICHIER_COMMANDES, f"{num};{cid};{service};{prix};{statut};{date}")
    tree.insert("", "end", values=(num, cid, service, prix,statut,date))
    messagebox.showinfo("Succès", f"Commande #{num} enregistrée.")

# Function de modification de commandes
def modifier_commande(var_client_id, var_service, var_prix, var_statut, tree):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez une commande à modifier.")
        return
    num = tree.item(sel[0], "values")[0]
    client_id = var_client_id.get().strip()
    service = var_service.get().strip()
    prix = var_prix.get().strip()
    statut = var_statut.get().strip()
    if not client_id or not service or not prix or not statut:
        messagebox.showwarning("Champ vide", "Remplissez les champs avant de modifier.")
        return
    modifier_ligne(FICHIER_COMMANDES, int(num), client_id, service, prix, statut)
    tree.item(sel[0], values=(num, client_id, service, prix, statut, tree.item(sel[0], "values")[5]))
    messagebox.showinfo("Mis à jour", f"Commande #{num} modifiée.")

# Function de suppression de commandes
def supprimer_commande(tree):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez une commande à supprimer.")
        return
    num = tree.item(sel[0], "values")[0]
    if messagebox.askyesno("Confirmer", f"Supprimer la commande #{num} ?"):
        supprimer_ligne(FICHIER_COMMANDES, int(num))
        tree.delete(sel[0])

# Function de sélection d'une commande dans le tableau pour pré-remplir les champs du formulaire
def selectionner_commande(tree, var_client_id, var_service, var_prix, var_statut):
    sel = tree.selection()
    if sel:
        vals = tree.item(sel[0], "values")
        var_client_id.set(vals[1])
        var_service.set(vals[2])
        var_prix.set(vals[3])
        var_statut.set(vals[4])

# ─── FONCTIONS GÉNÉRIQUES DE FICHIER ─────────────────

def lire_fichier(chemin):
    """Retourne toutes les lignes non vides d'un fichier."""
    if not os.path.exists(chemin): return []
    with open(chemin, "r", encoding="utf-8") as f:
        return [l.strip() for l in f.readlines() if l.strip()]

def ecrire_ligne(chemin, ligne):
    """Ajoute une ligne à la fin du fichier (mode append)."""
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")

def reecrire_fichier(chemin, lignes):
    """Réécrit l'intégralité du fichier (pour update/delete)."""
    with open(chemin, "w", encoding="utf-8") as f:
        f.writelines([l + "\n" for l in lignes])

def supprimer_ligne(chemin, identifiant):
    lignes   = lire_fichier(chemin)
    nouvelles = [l for l in lignes if int(l.split(";")[0]) != identifiant]
    reecrire_fichier(chemin, nouvelles)

def modifier_ligne(chemin, identifiant, *champs):
    lignes    = lire_fichier(chemin)
    nouvelles = []
    for l in lignes:
        parties = l.split(";")
        if int(parties[0]) == identifiant:
            nouvelles.append(";".join([parties[0]] + list(champs)))
        else:
            nouvelles.append(l)
    reecrire_fichier(chemin, nouvelles)

# Function pour générer une facture PDF à partir d'une commande sélectionnée dans le tableau
def generer_facture_pdf(tree):
    sel = tree.selection()

    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez une commande.")
        return

    values = tree.item(sel[0], "values")

    num_cmd   = values[0]
    client_id = values[1]
    service   = values[2]
    prix      = values[3]
    statut    = values[4]
    date      = values[5]

    nom_fichier = f"facture_{num_cmd}.pdf"

    c = canvas.Canvas(nom_fichier, pagesize=A4)

    # Titre
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, 800, "FACTURE GRAPHESTUDIO")

    # Contenu
    c.setFont("Helvetica", 12)
    c.drawString(50, 740, f"Numéro Commande : {num_cmd}")
    c.drawString(50, 720, f"ID Client       : {client_id}")
    c.drawString(50, 700, f"Service         : {service}")
    c.drawString(50, 680, f"Prix            : {prix} FCFA")
    c.drawString(50, 660, f"Statut          : {statut}")
    c.drawString(50, 640, f"Date            : {date}")

    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 600, f"TOTAL : {prix} FCFA")

    # Signature
    c.setFont("Helvetica", 10)
    c.drawString(50, 550, "Merci pour votre confiance - GraphiStudio")

    c.save()

    messagebox.showinfo("Succès", f"Facture PDF générée : {nom_fichier}")

# ─── CHARGEMENT INITIAL ────────────────────────────────

def charger_clients(tree):
    # Vider le tableau avant de charger les clients
    for item in tree.get_children():
        tree.delete(item)

    for ligne in lire_fichier(FICHIER_CLIENTS):
        p = ligne.split(";")
        if len(p) == 3:
            tree.insert("", "end", values=tuple(p))
def charger_commandes(tree):
    for ligne in lire_fichier(FICHIER_COMMANDES):
        p = ligne.split(";")
        if len(p) == 6: tree.insert("", "end", values=tuple(p))

def client_existe(cid):
    return any(int(l.split(";")[0]) == cid
                for l in lire_fichier(FICHIER_CLIENTS))

