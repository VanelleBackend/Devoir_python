# Importation de library
from tkinter import ttk, messagebox
import datetime, os

# Fichier de stockage des clients et commandes
FICHIER_CLIENTS = "clients.txt"
FICHIER_COMMANDES = "commandes.txt"

def generer_id(fichier):
    lignes = lire_fichier(fichier)
    if not lignes: return 1
    ids = [int(l.split(";")[0]) for l in lignes if l.strip()]
    return max(ids) + 1

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

def supprimer_client(tree):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un client à supprimer.")
        return
    cid = tree.item(sel[0], "values")[0]
    if messagebox.askyesno("Confirmer", f"Supprimer le client #{cid} ?"):
        supprimer_ligne(FICHIER_CLIENTS, int(cid))
        tree.delete(sel[0])

def selectionner_client(tree, var_nom, var_tel):
    sel = tree.selection()
    if sel:
        vals = tree.item(sel[0], "values")
        var_nom.set(vals[1])
        var_tel.set(vals[2])

def ajouter_commande(var_client_id, var_service, tree):
    cid     = var_client_id.get().strip()
    service = var_service.get().strip()
    if not cid or not service:
        messagebox.showwarning("Erreur", "ID client et service sontobligatoires.")
        return
    if not client_existe(int(cid)):
        messagebox.showerror("Client introuvable", f"Aucun client avec l'ID {cid}.")
        return
    num  = generer_id(FICHIER_COMMANDES)
    date = datetime.date.today().isoformat()
    ecrire_ligne(FICHIER_COMMANDES, f"{num};{cid};{service};{date}")
    tree.insert("", "end", values=(num, cid, service, date))
    messagebox.showinfo("Succès", f"Commande #{num} enregistrée.")

def supprimer_commande(tree):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez une commande à supprimer.")
        return
    num = tree.item(sel[0], "values")[0]
    if messagebox.askyesno("Confirmer", f"Supprimer la commande #{num} ?"):
        supprimer_ligne(FICHIER_COMMANDES, int(num))
        tree.delete(sel[0])

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

# ─── CHARGEMENT INITIAL ────────────────────────────────

def charger_clients(tree):
    for ligne in lire_fichier(FICHIER_CLIENTS):
        p = ligne.split(";")
        if len(p) == 3: tree.insert("", "end", values=tuple(p))

def charger_commandes(tree):
    for ligne in lire_fichier(FICHIER_COMMANDES):
        p = ligne.split(";")
        if len(p) == 4: tree.insert("", "end", values=tuple(p))

def client_existe(cid):
    return any(int(l.split(";")[0]) == cid
                for l in lire_fichier(FICHIER_CLIENTS))